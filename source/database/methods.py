from core import Session
from source.database.user import User

def add_user(user: User):
    sess = Session()
    sess.add(user)
    try:
        sess.commit()
        return True
    except Exception as e:
        sess.rollback()
        return e

def get_user(id: int) -> User:
    result = [x for x in Session().query(User).filter_by(tg_id=id)]
    return result[0] if result else None