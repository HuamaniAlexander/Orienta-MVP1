from app.domain.errors import DomainError
from sqlalchemy import func, select

from .models import Career, Institution, Offer


class SqlCatalogRepository:
    def __init__(self, session):
        self.session = session

    def _career(self, career):
        return {
            "id": career.code,
            "slug": career.slug,
            "name": career.name,
            "area": career.area,
            "area_code": career.area_code,
            "kind": career.kind,
            "content": career.content,
            "profile": career.profile,
            "profile_reviewed": career.profile_reviewed,
            "version": career.version,
        }

    def list_careers(self, q="", area="", kind="", district="", page=1, page_size=12):
        stmt = select(Career).where(Career.active.is_(True))
        if q:
            pattern = "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
            stmt = stmt.where(Career.name.ilike(pattern, escape="\\"))
        if area:
            stmt = stmt.where(Career.area == area)
        if kind:
            stmt = stmt.where(Career.kind == kind)
        if district:
            stmt = stmt.where(
                Career.code.in_(
                    select(Offer.career_code).where(
                        Offer.district == district, Offer.active.is_(True)
                    )
                )
            )
        count = self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        values = self.session.scalars(
            stmt.order_by(Career.code).offset((page - 1) * page_size).limit(page_size)
        )
        return [self._career(c) for c in values], count

    def get_career(self, code):
        career = self.session.get(Career, code)
        if not career or not career.active:
            raise DomainError("La carrera no está disponible", "not_found", 404)
        return self._career(career)

    def list_offers(self, career_code=None, district=""):
        stmt = select(Offer, Institution).join(Institution).where(Offer.active.is_(True))
        if career_code is not None:
            stmt = stmt.where(Offer.career_code == career_code)
        if district:
            stmt = stmt.where(Offer.district == district)
        return [
            {
                "id": o.id,
                "legacy_code": o.legacy_code,
                "career_id": o.career_code,
                "institution": {"id": i.code, "name": i.name, "kind": i.kind},
                "modality": o.modality,
                "district": o.district,
                "months": o.months,
                "cost": str(o.cost) if o.cost is not None else None,
                "cost_min": str(o.cost_min) if o.cost_min is not None else None,
                "cost_max": str(o.cost_max) if o.cost_max is not None else None,
                "cost_status": o.cost_status,
                "detail": o.detail,
            }
            for o, i in self.session.execute(stmt.order_by(Offer.id))
        ]

    def institutions(self):
        return [
            {"id": i.code, "name": i.name, "kind": i.kind}
            for i in self.session.scalars(select(Institution).order_by(Institution.code))
        ]
