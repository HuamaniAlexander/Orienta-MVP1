"""Informe reproducible de cobertura; no completa datos ausentes con valores inventados."""

import json
from pathlib import Path


def report():
    def read(file):
        return json.loads(Path("data", file).read_text())

    registry = read("padron_minedu_norte.json")
    institutions = read("instituciones_lima_norte.json")
    programs = read("programas_institucionales.json")
    codes = {i.get("modular_code") for i in institutions}
    expected = {i["code"] for i in registry["institutions"]}
    grouped = {
        i["slug"]: [p for p in programs if p["institution_slug"] == i["slug"]] for i in institutions
    }
    return {
        "registry_date": registry["published_on"],
        "registry_institutions": len(expected),
        "registry_covered": len(codes & expected),
        "registry_missing": sorted(expected - codes),
        "directory_institutions": len(institutions),
        "documented_programs": len(programs),
        "programs_with_published_tuition": sum(bool(p.get("tuition")) for p in programs),
        "public_career_ids": sorted({p["career_id"] for p in programs}),
        "scope": registry["scope"],
        "institutions": [
            {
                "slug": i["slug"],
                "program_records": len(grouped[i["slug"]]),
                "tuition_records": sum(bool(p.get("tuition")) for p in grouped[i["slug"]]),
                "institutional_financial_policy": bool(i.get("financial_policy")),
            }
            for i in institutions
        ],
    }


if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2))
