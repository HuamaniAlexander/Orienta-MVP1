import { Link, useParams } from "react-router-dom";
import { ExternalLink, MapPin } from "lucide-react";
import { useResource } from "../shared/useResource";
import { Feedback } from "../shared/Feedback";
import { AcademicOptions, money } from "../features/catalog/AcademicOptions";
import type { InstitutionProfile } from "../shared/types";
export function InstitutionPage() {
  const { slug } = useParams();
  const resource = useResource<InstitutionProfile>(
    `/directorio/instituciones/${encodeURIComponent(slug ?? "")}`,
  );
  const i = resource.data;
  return (
    <div className="container page">
      <Link to="/instituciones">← Volver al directorio</Link>
      <Feedback {...resource} />
      {i && (
        <>
          <section className="institution-profile card">
            <p className="eyebrow">{i.kind}</p>
            <h1>{i.name}</h1>
            <p className="lead">{i.description}</p>
            <div className="profile-locations">
              {i.locations.map((l) => (
                <div key={l.district}>
                  <MapPin size={18} />
                  <p>
                    <strong>{l.district}</strong>
                    <br />
                    {l.address}
                  </p>
                </div>
              ))}
            </div>
            {i.contact && (
              <p>
                <strong>Contacto institucional:</strong> {i.contact}
              </p>
            )}
            {i.modular_code && (
              <p>
                Código modular MINEDU: <strong>{i.modular_code}</strong> ·
                Padrón {i.registry_date}
              </p>
            )}
            <a
              className="button secondary"
              href={i.website}
              target="_blank"
              rel="noopener noreferrer"
            >
              Visitar institución <ExternalLink size={16} />
            </a>
          </section>
          {i.financial_policy && (
            <section className="card institution-profile">
              <h2>Cómo se calculan los pagos</h2>
              <strong>
                {money(i.financial_policy.min)} –{" "}
                {money(i.financial_policy.max)}
              </strong>
              <p>{i.financial_policy.scope}</p>
              <p>Periodo {i.financial_policy.period}</p>
              <a
                href={i.financial_policy.source_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Ver política de pagos oficial ↗
              </a>
            </section>
          )}
          {(i.academic_programs?.length ?? 0) > 0 && (
            <section>
              <h2>Programas y planes publicados</h2>
              <AcademicOptions
                programs={i.academic_programs!}
                compare={false}
              />
            </section>
          )}
          {i.programs.length > 0 && (
            <section className="card institution-profile">
              <h2>Otras opciones publicadas por la institución</h2>
              <ul className="program-names">
                {i.programs.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
            </section>
          )}
          {!!i.resources?.length && (
            <section className="card institution-profile">
              <h2>Admisión, pagos y servicios</h2>
              <ul>
                {i.resources.map((r) => (
                  <li key={r.url}>
                    <a href={r.url} target="_blank" rel="noopener noreferrer">
                      {r.label} ↗
                    </a>
                  </li>
                ))}
              </ul>
            </section>
          )}
          <section className="card institution-profile">
            <h2>Fuentes de esta ficha</h2>
            <ul>
              {i.sources.map((s) => (
                <li key={s.url}>
                  <a href={s.url} target="_blank" rel="noopener noreferrer">
                    {s.label} ↗
                  </a>
                </li>
              ))}
            </ul>
            <small>Fuentes consultadas el {i.reviewed_on}</small>
          </section>
        </>
      )}
    </div>
  );
}
