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

    @staticmethod
    def delete_user_by_sid_user_id(db, sid, user_id):
        db.query(AccountAccess).filter(
            AccountAccess.user_id == user_id,
            AccountAccess.sid == sid
        ).delete(synchronize_session='fetch')

    @staticmethod
    def delete_user_by_access_id(db, access_id):
        db.query(AccountAccess).filter(
            AccountAccess.access_id == access_id
        ).delete(synchronize_session='fetch')