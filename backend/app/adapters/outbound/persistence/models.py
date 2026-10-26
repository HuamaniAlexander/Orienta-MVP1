from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    metadata = MetaData(schema="orienta")


class LegacyCode(Base):
    __tablename__ = "legacy_code"
    field: Mapped[str] = mapped_column(String(64), primary_key=True)
    code: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(Text)
    __table_args__ = (UniqueConstraint("field", "value"),)


class Institution(Base):
    __tablename__ = "institution"
    code: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    kind: Mapped[str] = mapped_column(String(30), default="universidad")


class Career(Base):
    __tablename__ = "career"
    code: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    area: Mapped[str] = mapped_column(String(100), index=True)
    area_code: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(30), default="universitaria")
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    profile: Mapped[list | None] = mapped_column(JSON, nullable=True)
    profile_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[str] = mapped_column(String(64), default="catalogo-1")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Offer(Base):
    __tablename__ = "offer"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    legacy_code: Mapped[int] = mapped_column(Integer, unique=True)
    career_code: Mapped[int] = mapped_column(ForeignKey("orienta.career.code"), index=True)
    institution_code: Mapped[int] = mapped_column(
        ForeignKey("orienta.institution.code"), index=True
    )
    modality: Mapped[str] = mapped_column(String(30), index=True)
    modality_code: Mapped[int] = mapped_column(Integer)
    district: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    location_legacy: Mapped[str] = mapped_column(String(150))
    months: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    cost_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    cost_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    cost_status: Mapped[str] = mapped_column(String(30))
    detail: Mapped[dict] = mapped_column(JSON)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    __table_args__ = (
        CheckConstraint("months > 0"),
        CheckConstraint("cost >= 0"),
        CheckConstraint("cost_min >= 0 AND cost_max >= cost_min"),
    )


class ImportBatch(Base):
    __tablename__ = "import_batch"
    digest: Mapped[str] = mapped_column(String(64), primary_key=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    counts: Mapped[dict] = mapped_column(JSON)


class User(Base):
    __tablename__ = "app_user"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class BrowserSession(Base):
    __tablename__ = "browser_session"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("orienta.app_user.id", ondelete="CASCADE"), nullable=True
    )
    csrf_hash: Mapped[str] = mapped_column(String(64))
    expires: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Comparison(Base):
    __tablename__ = "comparison"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("orienta.app_user.id", ondelete="CASCADE"), index=True
    )
    key: Mapped[str] = mapped_column(String(36))
    payload_hash: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON)
    result: Mapped[dict] = mapped_column(JSON)
    snapshot: Mapped[list] = mapped_column(JSON)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    __table_args__ = (UniqueConstraint("user_id", "key"),)


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    comparison_id: Mapped[str] = mapped_column(
        ForeignKey("orienta.comparison.id", ondelete="CASCADE"), index=True
    )
    score: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(500))
    research_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    __table_args__ = (CheckConstraint("score BETWEEN 1 AND 5"),)


class DirectoryInstitution(Base):
    """Directorio geográfico; no crea ofertas académicas implícitas."""

    __tablename__ = "institution_directory"
    slug: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    kind: Mapped[str] = mapped_column(String(40), index=True)
    data: Mapped[dict] = mapped_column(JSON)
