class UserControl:
    user = ""
    logged_in = False

    def __init__(self, username):
        self.user = username

    def validate_login(self, password):
        if self.user in 'teste':
            if password == '12345':
                self.logged_in = True
                return True

        return False
