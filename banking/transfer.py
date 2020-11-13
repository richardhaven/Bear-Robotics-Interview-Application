from bank_api import Bank_API

from auz import check_access

from sessions import get_session_info, update_session_id

from infrastructure import log_api_exception, log_withdrawl, log_deposit,
                           signal_critical_alert, compose_error_message,
                           InactiveSessionError, InternalError, InvalidAmountError

from cash_box import cash_out

def transfer(session_id, source_account_id, target_account_id, amount):
    if amount <= 0 or (not (amount + 0.0).is_integer()):
        raise InvalidAmountError()

	session_info = get_session_info(session_id)

	if session_info is None or not session_info.active:
		raise InactiveSessionError()

    check_access(session_info, "transfer_out", source_account_id)
    check_access(session_info, "transfer_in", target_account_id)

    bank_api = Bank_API.get_connection()
    try:
        process_transfer(session_info, source_account_id, target_account_id, amount, bank_api)
    finally:
        bank_api.release_connection()

    log_withdrawl(session_info, source_account_id, amount, TRANSFER)
    log_deposit(session_info, target_account_id, amount, TRANSFER)

    session_id = update_session_id(session_id)

    return (session_id, None)

def process_transfer(session_info, source_account_id, target_account_id, amount, bank_api):
    pending_withdrawl_token = get_pending_api_token(session_info, account_id, amount, bank_api)
    try:
        process_cash_in_call(session_info, account_id, amount, bank_api)

        process_transfer_out_confirmation(session_info, pending_withdrawl_token, bank_api)
        pending_withdrawl_token = None
    finally:
        if pending_withdrawl_token is not None:
            bank_api.cancel_cash_out(pending_withdrawl_token)

def get_pending_api_token(session_info, account_id, amount, bank_api):
    try:
        call_response = bank_api.start_cash_out(session_info.api_session_id, account_id, amount)

    except Exception as e:
        log_api_exception("distribute_cash", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if call_response.has_failed():
        log_failure_metrics("start_cash_out", session_info, call_response)

        error_message = compose_error_message("start_cash_out", call_response)
        raise API_Error(error_message)

    if call_response.error is not None:
        raise InvalidAmountError()

    return call_response.withdrawl_authorization_id


def process_cash_out_confirmation(session_info, pending_distribution_token, bank_api)
    try:
        call_response = bank_api.confirm_cash_out(pending_distribution_token)

    except Exception as e:
        log_api_exception("confirm_cash_out", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if call_response.has_failed():
        log_failure_metrics("confirm_cash_out", session_info, call_response)

        error_message = compose_error_message("confirm_cash_out", call_response)
        raise API_Error(error_message)

def process_cash_in_call(session_info, account_id, amount, bank_api)
    try:
        call_response = bank_api.confirm_cash_in(session_info.api_session_id, account_id, amount)

    except Exception as e:
        log_api_exception("confirm_cash_out", session_info, e)
        raise InternalError.from_exception(session_info, e)

    if call_response.has_failed():
        log_failure_metrics("confirm_cash_out", session_info, call_response)

        error_message = compose_error_message("confirm_cash_out", call_response)
        raise API_Error(error_message)

    if call_response.error is not None:
        raise InvalidAmountError()
