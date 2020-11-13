from bank_api import Bank_API

from auz import check_access

from sessions import get_session_info, update_session_id

from infrastructure import log_api_exception, compose_error_message, log_deposit,
                           InactiveSessionError, InternalError

from cash_box import accept_cheque

def receive_cheque(session_id, account_id):
	session_info = get_session_info(session_id)

	if session_info is None or not session_info.active:
		raise InactiveSessionError()

    check_access(session_info, "put_cheque", account_id)

    bank_api = Bank_API.get_connection()
    try:
        amount, id = process_cheque_in(session_info, account_id, amount, bank_api)
    finally:
        bank_api.release_connection()

    if amount > 0:
        log_deposit(session_info, account_id, amount, id)

    session_id = update_session_id(session_id)

    return (session_id, amount)

def process_cheque_in(session_info, account_id, bank_api):
    try:
        cheque_amount, cheque_in_audit_id = accept_cheque()

    except Exception as e:
        log_atm_exception("accept_check", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if cheque_amount > 0:
        try:
            if not process_cheque_call(session_info, account_id, cheque_amount, bank_api):
                raise InternalError()

        except Exception as e:
            try:
                abort_cheque()  # return the cheque to the customer
            except:
                signal_critical_alert("cannot abort cheque in", session_info, account_id,
                                                                cheque_amount, cheque_in_audit_id)

            raise e

    return (cheque_amount, cheque_in_audit_id)


def process_cheque_call(session_info, account_id, amount, bank_api)
    try:
        call_response = bank_api.confirm_cheque_in(session_info.api_session_id, account_id, amount)

    except Exception as e:
        log_api_exception("confirm_cheque_out", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if call_response.has_failed():
        log_failure_metrics("confirm_cheque_out", session_info, call_response)

        error_message = compose_error_message("confirm_cheque_out", call_response)
        raise API_Error(error_message)

    if call_response.error is not None:
        raise InvalidAmountError()
