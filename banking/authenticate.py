import uuid
from bank_api import Bank_API

from sessions import persist_session

from infrastructure import log_api_exception, compose_error_message, InternalError

 class LoginError(Exception):
    pass

# @returns a tuple with a dict with a session id and information
                                        #   "session_id"
                                        #   "user_name":
                                        #   "default_locale"
                                        #   "quick_cash_amount"
# or a LoginError

def authenticate(card_information, pin_hash, pin_seed):
    check_for_brute_force_attack(card_information)

    check_card_information(card_information)

    bank_api = Bank_API.get_connection()
    try:
        authentication_response = process_login_call(card_information, pin_hash,
                                                     pin_seed, bank_api)

    finally:
        bank_api.release_connection()

    this_tier_session_id = uuid.uuid4()
    session_info = fill_session_info(this_tier_session_id,
                                     authentication_response.card_user_name)

    persisted_session_info = session_info |
                             {"api_session_id": authentication_response.session_id}
    persist_session(this_tier_session_id, persisted_session_info)

    return (this_tier_session_id, session_info)


def process_login_call(card_information, pin_hash, pin_seed, bank_api):
    try:
        authentication_response = bank_api.authenticate(card_information, pin_hash, pin_seed)

    except Exception as e:
        log_api_exception(card_information, e)

        raise InternalError.from_exception(card_information, e)

    if authentication_response.has_failed():
        log_failure_metrics("authenticate", card_information, authentication_response)

        error_message = compose_error_message("authenticate", authentication_response)
        raise LoginError(error_message)

    return authentication_response

def fill_session_info(session_id, authentication_response):
    return {
            "session_id": session_id,
            "user_name": authentication_response.card_user_name,
            "default_locale": authentication_response.default_locale,
            "quick_cash_amount": authentication_response.quick_cash_amount,
    }


def check_for_brute_force_attack(card_information):
    pass

def check_card_information(card_information):
    pass

def log_authentication_exception(card_information, e):
    pass

def log_failure_metrics(card_information, authentication_response):
    pass

def persist_login_session(session_information):
    """
        this will end any existing sessions for this card
    """
    pass
