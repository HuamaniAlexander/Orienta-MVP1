import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.domain.errors import DomainError


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class AuthService:
    def __init__(self, repository, passwords, hours=8):
        self.repository, self.passwords, self.hours = repository, passwords, hours

    def find_session(self, token):
        if not token:
            return None
        row = self.repository.browser_session(digest(token))
        if not row:
            return None
        expires = row.expires.replace(tzinfo=timezone.utc) if row.expires.tzinfo is None else row.expires
        if expires <= datetime.now(timezone.utc):
            self.repository.remove_session(row)
            return None
        return row

    def issue(self, uid=None, old=None):
        if old:
            self.repository.remove_session(old)
        token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        self.repository.add_session(token_hash=digest(token), user_id=uid, csrf_hash=digest(csrf),
                                    expires=datetime.now(timezone.utc)+timedelta(hours=self.hours))
        return token, csrf

    def csrf(self, token):
        row = self.find_session(token)
        if not row:
            return self.issue()
        csrf = secrets.token_urlsafe(32)
        row.csrf_hash = digest(csrf)
        return token, csrf

    def require_csrf(self, token, csrf):
        row = self.find_session(token)
        if not row or not csrf or not secrets.compare_digest(row.csrf_hash, digest(csrf)):
            raise DomainError("La sesión cambió. Vuelve a intentar.", "csrf_invalid", 403)
        return row

    def current_user(self, token):
        row = self.find_session(token)
        user = self.repository.user(row.user_id) if row and row.user_id else None
        if not user:
            raise DomainError("Inicia sesión para continuar", "unauthorized", 401)
        return {"id": user.id, "email": user.email}

    def register(self, email, password):
        if self.repository.user_by_email(email):
            raise DomainError("No se pudo registrar este correo. Intenta iniciar sesión.", "email_conflict", 409)
        user = self.repository.add_user(id=str(uuid4()), email=email, password_hash=self.passwords.hash(password))
        return {"id": user.id, "email": user.email}

    def login(self, email, password, row):
        user = self.repository.user_by_email(email)
        if not self.passwords.verify(password, user.password_hash if user else None):
            raise DomainError("Correo o contraseña incorrectos", "invalid_credentials", 401)
        token, csrf = self.issue(user.id, old=row)
        return {"user": {"id": user.id, "email": user.email}, "csrf_token": csrf}, token

    def logout(self, token):
        row = self.find_session(token)
        if row:
            self.repository.remove_session(row)
