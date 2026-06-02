# Shadow migration module.
# Admin routes remain in main.py until final cutover.

class AdminApi:

    @staticmethod
    def login_logic():
        return 'Copied from main.py during migration phase'

    @staticmethod
    def purchases_logic():
        return 'Copied from main.py during migration phase'

    @staticmethod
    def stats_logic():
        return 'Copied from main.py during migration phase'