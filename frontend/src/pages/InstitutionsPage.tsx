import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ExternalLink, MapPin, Search, GraduationCap } from "lucide-react";
import { useResource } from "../shared/useResource";
import { Feedback } from "../shared/Feedback";
interface Institution {
  slug: string;
  name: string;
  kind: string;
  website: string;
  description: string;
  locations: { district: string; address: string }[];
  programs: string[];
  contact?: string;
  reviewed_on: string;
  sources: { label: string; url: string }[];
}
const normalize = (text: string) =>
  text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
export function InstitutionsPage() {
  const { data, loading, error, retry } = useResource<{
    items: Institution[];
    total: number;
  }>("/directorio/instituciones");
  const [query, setQuery] = useState(""),
    [district, setDistrict] = useState(""),
    [kind, setKind] = useState("");
  const items = data?.items ?? [];
  const districts = useMemo(
    () =>
      [
        ...new Set(items.flatMap((i) => i.locations.map((l) => l.district))),
      ].sort(),
    [data],
  );
  const filtered = items.filter(
    (i) =>
      (!district || i.locations.some((l) => l.district === district)) &&
      (!kind || i.kind === kind) &&
      normalize([i.name, i.description, ...i.programs].join(" ")).includes(
        normalize(query),
      ),
  );
  return (
    <div className="container page">
      <section className="directory-intro">
        <div>
          <p className="eyebrow">ELIGE DÓNDE DAR EL SIGUIENTE PASO</p>
          <h1>Instituciones cerca de ti</h1>
          <p className="lead">
            Encuentra universidades, institutos y escuelas por distrito. Conoce
            sus ubicaciones y accede a sus canales oficiales.
          </p>
          <Link className="button secondary" to="/carreras">
            Primero, explora qué carrera estudiar
          </Link>
        </div>
        <img
          src="/images/orienta-caminos-640.webp"
          width="640"
          height="360"
          alt="Estudiante explorando caminos de formación"
          loading="lazy"
          srcSet="/images/orienta-caminos-640.webp 640w, /images/orienta-caminos-1280.webp 1280w"
          sizes="(max-width: 760px) 100vw, 50vw"
          decoding="async"
        />
      </section>
      <div className="card directory-filters">
        <label>
          <span>
            <Search size={16} /> Buscar institución o carrera
          </span>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Nombre, tecnología, salud…"
          />
        </label>
        <label>
          Distrito
          <select
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
          >
            <option value="">Todos los distritos</option>
            {districts.map((d) => (
              <option key={d}>{d}</option>
            ))}
          </select>
        </label>
        <label>
          Formación
          <select value={kind} onChange={(e) => setKind(e.target.value)}>
            <option value="">Todas las instituciones</option>
            {[...new Set(items.map((i) => i.kind))].sort().map((k) => (
              <option key={k}>{k}</option>
            ))}
          </select>
        </label>
        <button
          className="secondary"
          onClick={() => {
            setQuery("");
            setDistrict("");
            setKind("");
          }}
        >
          Limpiar filtros
        </button>
      </div>
      <Feedback loading={loading} error={error} retry={retry} />
      {data && (
        <p role="status" aria-live="polite">
          {filtered.length} instituciones encontradas
        </p>
      )}
      {!loading && !error && !filtered.length && (
        <section className="card empty">
          <h2>No encontramos coincidencias</h2>
          <p>Prueba otro nombre o amplía los filtros.</p>
        </section>
      )}
      <div className="directory-grid">
        {filtered.map((i) => (
          <article className="card institution-card" key={i.slug}>
            <div className="institution-heading">
              <span className="icon-tile">
                <GraduationCap aria-hidden="true" />
              </span>
              <span className="badge">{i.kind}</span>
            </div>
            <h2>{i.name}</h2>
            <p>{i.description}</p>
            <ul className="institution-locations">
              {i.locations.map((l) => (
                <li key={l.district}>
                  <MapPin size={18} aria-hidden="true" />
                  <div>
                    <strong>{l.district}</strong>
                    <span>{l.address}</span>
                  </div>
                </li>
              ))}
            </ul>
            {i.contact && (
              <p>
                <strong>Contacto:</strong> {i.contact}
              </p>
            )}
            {i.programs.length > 0 && (
              <details>
                <summary>Explorar programas publicados</summary>
                <ul>
                  {i.programs.map((p) => (
                    <li key={p}>{p}</li>
                  ))}
                </ul>
              </details>
            )}
            <details>
              <summary>Fuentes de esta ficha</summary>
              <ul>
                {i.sources.map((s) => (
                  <li key={s.url}>
                    <a href={s.url} target="_blank" rel="noopener noreferrer">
                      {s.label} <ExternalLink size={13} />
                    </a>
                  </li>
                ))}
              </ul>
              <small>Consulta de fuentes: {i.reviewed_on}</small>
            </details>
            <a
              className="button secondary institution-link"
              href={i.website}
              target="_blank"
              rel="noopener noreferrer"
            >
              Visitar sitio oficial <ExternalLink size={16} />
            </a>
          </article>
        ))}
      </div>
    </div>
  );
}
