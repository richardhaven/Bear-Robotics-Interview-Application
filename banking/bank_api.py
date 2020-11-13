class Bank_API:
    def get_connection():
        pass  # return a persistent connection from a cached pool or other mechanism

    def release_connection(self):
        pass

    def authenticate(self, card_information, pin_hash, pin_seed):
        pass

    def get_accounts(self, session_id):
        pass

    def get_account_balance(self, session_id, account_id):
        pass

    def confirm_cash_in(self, session_id, account_id, amount):
        pass

    def start_cash_out(self, session_id, account_id, amount):
        pass

    def confirm_cash_out(self, token):
        pass

    def cancel_cash_out(self, token):
        pass
