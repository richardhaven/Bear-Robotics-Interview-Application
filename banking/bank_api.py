class Bank_API:
    def get_connection():
        return Bank_API()  # return a persistent connection from a cached pool or other mechanism

    def release_connection(self):
        pass

    def authenticate(self, card_information, pin_hash, pin_seed):
        return {"has_failed": False, "error": None}

    def get_accounts(self, session_id):
        return {"has_failed": False, "error": None}

    def get_account_balance(self, session_id, account_id):
        return {"has_failed": False, "error": None}

    def confirm_cash_in(self, session_id, account_id, amount):
        return {"has_failed": False, "error": None}

    def start_cash_out(self, session_id, account_id, amount):
        return {"has_failed": False, "error": None}

    def confirm_cash_out(self, token):
        return {"has_failed": False, "error": None}

    def cancel_cash_out(self, token):
        return {"has_failed": False, "error": None}
