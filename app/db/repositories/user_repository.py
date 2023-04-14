from app.db.models.user import User
from app.db.models.account_access import AccountAccess

class UserRepository(object):
    @staticmethod
    def find_user_by_account(db, user_account):
        return db.query(User).filter(
            User.user_account == user_account
        ).first()

    @staticmethod
    def find_user_by_login_id(db, user_id):
        return db.query(AccountAccess).filter(
            AccountAccess.user_id == user_id
        ).all()