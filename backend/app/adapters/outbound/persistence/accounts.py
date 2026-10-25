from sqlalchemy import select

from .models import BrowserSession, Comparison, Feedback, User


class SqlAccounts:
    def __init__(self, session):
        self.session = session

    def user_by_email(self, email):
        return self.session.scalar(select(User).where(User.email == email))

    def user(self, uid):
        return self.session.get(User, uid)

    def add_user(self, **values):
        user = User(**values)
        self.session.add(user)
        self.session.flush()
        return user

    def browser_session(self, token_hash):
        return self.session.get(BrowserSession, token_hash)

    def remove_session(self, session):
        self.session.delete(session)

    def add_session(self, **values):
        row = BrowserSession(**values)
        self.session.add(row)
        self.session.flush()
        return row


class SqlHistory:
    def __init__(self, session):
        self.session = session

    def find_key(self, uid, key):
        return self.session.scalar(
            select(Comparison).where(Comparison.user_id == uid, Comparison.key == key)
        )

    def get(self, uid, comparison_id):
        return self.session.scalar(
            select(Comparison).where(Comparison.user_id == uid, Comparison.id == comparison_id)
        )

    def list(self, uid, page, size):
        from sqlalchemy import func

        total = self.session.scalar(
            select(func.count()).select_from(Comparison).where(Comparison.user_id == uid)
        )
        rows = self.session.scalars(
            select(Comparison)
            .where(Comparison.user_id == uid)
            .order_by(Comparison.created.desc(), Comparison.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        return [self.serialize(row) for row in rows], total

    def serialize(self, row):
        return {
            "id": row.id,
            "payload": row.payload,
            "result": row.result,
            "snapshot": row.snapshot,
            "created": row.created.isoformat(),
        }

    def add(self, **values):
        row = Comparison(**values)
        self.session.add(row)
        self.session.flush()
        return row

    def delete(self, row):
        self.session.delete(row)
        self.session.flush()

    def feedback(self, **values):
        self.session.add(Feedback(**values))
        self.session.flush()
