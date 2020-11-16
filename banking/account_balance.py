from bank_api import Bank_API

from auz import check_access

from sessions import get_session_info, update_session_id

from infrastructure import log_api_exception, compose_error_message, InactiveSessionError, InternalError

def get_account_balance(session_id, account_id):
    session_info = get_session_info(session_id)

    if session_info is None or (not session_info.active):
        raise InactiveSessionError()

    check_access(session_info, "get_account_balance", account_id)

    bank_api = Bank_API.get_connection()
    try:
        call_response = process_account_balance_call(session_info, account_id, bank_api)
    finally:
        bank_api.release_connection()

    result = fill_account_balance(call_response)

    session_id = update_session_id(session_id)

    return (session_id, result)


def process_account_balance_call(session_info, account_id, bank_api):
    try:
        call_response = bank_api.get_account_balance(session_info.api_session_id, account_id)

    except Exception as e:
        log_api_exception("get_account_balance", session_info, e)
        raise InternalError.from_exception("get_account_balance", session_info, e)

    if call_response.has_failed:
        log_api_failure("get_account_balance", session_info, call_response)

        error_message = compose_error_message("get_account_balance", call_response)
        raise InternalError(error_message)

    return call_response


def fill_account_balance(call_response):
    return {}
