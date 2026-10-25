import hashlib
import json
from uuid import uuid4

from app.domain.errors import DomainError


class HistoryService:
    def __init__(self, repository, orientation):
        self.repository, self.orientation = repository, orientation

    def save(self, uid, key, payload):
        hashed = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        existing = self.repository.find_key(uid, key)
        if existing:
            if existing.payload_hash != hashed:
                raise DomainError(
                    "La clave ya corresponde a otra comparación", "idempotency_conflict", 409
                )
            return self.repository.serialize(existing)
        result = self.orientation.recommend(payload)
        snapshot = self.orientation.preview(payload["career_ids"])["careers"]
        result["saved"] = True
        row = self.repository.add(
            id=str(uuid4()),
            user_id=uid,
            key=key,
            payload_hash=hashed,
            payload=payload,
            result=result,
            snapshot=snapshot,
        )
        return self.repository.serialize(row)

    def get(self, uid, cid):
        row = self.repository.get(uid, cid)
        if not row:
            raise DomainError("Comparación no encontrada", "not_found", 404)
        return row

    def delete(self, uid, cid):
        self.repository.delete(self.get(uid, cid))
