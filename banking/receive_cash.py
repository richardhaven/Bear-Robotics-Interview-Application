from bank_api import Bank_API

from auz import check_access

from sessions import get_session_info, update_session_id, InactiveSessionError

from infrastructure import log_api_exception, compose_error_message, log_deposit, InternalError

from cash_box import cash_in, abort_cash_in

def receive_cash(session_id, account_id):
    session_info = get_session_info(session_id)

    if session_info is None or not session_info.active:
        raise InactiveSessionError()

    check_access(session_info, "put_cash", account_id)

    bank_api = Bank_API.get_connection()
    try:
        amount, id = process_cash_in(session_info, account_id, amount, bank_api)
    finally:
        bank_api.release_connection()

    if amount > 0:
        log_deposit(session_info, account_id, amount, id)

    session_id = update_session_id(session_id)

    return (session_id, amount)

def process_cash_in(session_info, account_id, bank_api):
    try:
        cash_in_amount, cash_in_audit_id = cash_in()
    except Exception as e:
        log_atm_exception("receive_cash", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if cash_in_amount > 0:
        try:
            if not process_cash_in_call(session_info, account_id, cash_in_amount, bank_api):
                raise InternalError()

        except Exception as e:
            try:
                abort_cash_in()  # return the cash to the customer
            except:
                signal_critical_alert("cannot abort cash in", session_info, account_id,
                                                              cash_in_amount, cash_in_audit_id)

            raise e

    return (cash_in_amount, cash_in_audit_id)


def process_cash_in_call(session_info, account_id, amount, bank_api):
    try:
        call_response = bank_api.confirm_cash_in(session_info.api_session_id, account_id, amount)

    except Exception as e:
        log_api_exception("confirm_cash_in", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if call_response.has_failed:
        log_api_failure("confirm_cash_in", session_info, call_response)

        error_message = compose_error_message("confirm_cash_in", call_response)
        raise InternalError(error_message)

    if call_response.error is not None:
        raise InvalidAmountError(call_response.error)
