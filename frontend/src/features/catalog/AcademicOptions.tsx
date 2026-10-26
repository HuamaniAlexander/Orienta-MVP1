import { useState } from "react";
import { Link } from "react-router-dom";
import { ExternalLink, Scale } from "lucide-react";
import type { InstitutionalProgram } from "../../shared/types";
export const money = (value: number) =>
  new Intl.NumberFormat("es-PE", {
    style: "currency",
    currency: "PEN",
    maximumFractionDigits: 2,
  }).format(value);
export const tuitionText = (p: InstitutionalProgram) =>
  p.tuition
    ? p.tuition.min === p.tuition.max
      ? money(p.tuition.min)
      : `${money(p.tuition.min)} – ${money(p.tuition.max)}`
    : "";
export function AcademicOptions({
  programs,
  compare = true,
}: {
  programs: InstitutionalProgram[];
  compare?: boolean;
}) {
  const [selected, setSelected] = useState<string[]>([]);
  if (!programs.length) return null;
  const chosen = programs.filter((p) => selected.includes(p.id));
  return (
    <section className="academic-options">
      <div className="offer-grid">
        {programs.map((p) => (
          <article className="card academic-card" key={p.id}>
            <p className="eyebrow">PROGRAMA INSTITUCIONAL</p>
            <h3>{p.name}</h3>
            <Link to={`/instituciones/${p.institution_slug}`}>
              {p.institution_name}
            </Link>
            <p>Ubicación de la institución: {p.districts.join(" · ")}</p>
            {(p.months || p.modality) && (
              <p>
                {p.months && `${p.months} meses`}
                {p.months && p.modality && " · "}
                {p.modality}
              </p>
            )}
            {p.tuition && (
              <section className="published-price">
                <strong>{tuitionText(p)}</strong>
                <span>Por cuota · {p.tuition.period}</span>
                <p>{p.tuition.scope}</p>
                <a
                  href={p.tuition.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Fuente del costo <ExternalLink size={14} />
                </a>
              </section>
            )}
            {p.topics.length > 0 && (
              <ul>
                {p.topics.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            )}
            {p.documents.map((d) => (
              <a
                key={d.url}
                href={d.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {d.label} <ExternalLink size={14} />
              </a>
            ))}
            <a href={p.source_url} target="_blank" rel="noopener noreferrer">
              Programa y condiciones oficiales <ExternalLink size={14} />
            </a>
            {compare && (
              <button
                className="secondary"
                aria-pressed={selected.includes(p.id)}
                disabled={!selected.includes(p.id) && selected.length === 2}
                onClick={() =>
                  setSelected((prev) =>
                    prev.includes(p.id)
                      ? prev.filter((id) => id !== p.id)
                      : [...prev, p.id],
                  )
                }
              >
                <Scale size={16} />
                {selected.includes(p.id)
                  ? "Quitar programa"
                  : "Comparar programa"}
              </button>
            )}
          </article>
        ))}
      </div>
      {chosen.length === 2 && (
        <section className="card">
          <h3>Compara los planes institucionales</h3>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Criterio</th>
                  {chosen.map((p) => (
                    <th key={p.id}>
                      {p.institution_name}
                      <br />
                      {p.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {chosen.every((p) => p.tuition) && (
                  <>
                    <tr>
                      <th>Cuota publicada</th>
                      {chosen.map((p) => (
                        <td key={p.id}>{tuitionText(p)}</td>
                      ))}
                    </tr>
                    <tr>
                      <th>Periodo y alcance</th>
                      {chosen.map((p) => (
                        <td key={p.id}>
                          {p.tuition?.period}
                          <p>{p.tuition?.scope}</p>
                        </td>
                      ))}
                    </tr>
                  </>
                )}
                <tr>
                  <th>Ubicación institucional</th>
                  {chosen.map((p) => (
                    <td key={p.id}>{p.districts.join(" · ")}</td>
                  ))}
                </tr>
                <tr>
                  <th>Documentación publicada</th>
                  {chosen.map((p) => (
                    <td key={p.id}>
                      <a
                        href={p.documents[0]?.url ?? p.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Abrir fuente institucional ↗
                      </a>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      )}
    </section>
  );
}
