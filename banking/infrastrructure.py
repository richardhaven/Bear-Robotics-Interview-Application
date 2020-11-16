
class InternalError(Exception):
    def fromException(api_name, parameters, exception):
        pass

class InvalidAmountError(Exception):
    pass


def log_api_exception(api_name, parameters, exception):
    pass

def log_api_failure(api_name, parameters, response):
    pass

def log_atm_exception(name, parameters, exception):
    pass

def signal_critical_alert(type, session_info, account_id, amount, atm_audit_id):
    pass

def compose_error_message(parameters, response):
    return ""

def log_deposit(session_info, target_account_id, amount, atm_audit_id):
    pass

def log_withdrawl(session_info, target_account_id, amount, atm_audit_id):
    pass
