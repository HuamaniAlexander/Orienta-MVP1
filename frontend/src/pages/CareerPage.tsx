import { AcademicOptions } from "../features/catalog/AcademicOptions";
import { Link, useParams } from "react-router-dom";
import { ArrowRight, BookOpen, Plus, Check } from "lucide-react";
import type { Career } from "../shared/types";
import { useResource } from "../shared/useResource";
import { Feedback } from "../shared/Feedback";
import { useApp } from "../app/state";
import { InstitutionExplorer } from "../features/catalog/InstitutionExplorer";
const labels: Record<string, string> = {
  description: "¿Qué aprenderás?",
  courses: "Cursos principales",
  skills: "Habilidades a desarrollar",
  duration: "Duración",
  activities: "Actividades profesionales",
  field: "Campo laboral",
  specialties: "Especialidades",
  practice: "Experiencia práctica",
  qualification: "Grado y título",
  cost: "Pensión mensual entre instituciones",
  investment: "Inversión adicional",
  environment: "Entornos de trabajo",
};
export function CareerPage() {
  const { id } = useParams();
  const {
    data: c,
    error,
    loading,
    retry,
  } = useResource<Career>("/carreras/" + id);
  const s = useApp();
  return (
    <div className="container page">
      <div className="breadcrumb">
        <Link to="/carreras">Explorar carreras</Link>
        <span>/</span>
        <span>Ficha de carrera</span>
      </div>
      <Feedback loading={loading} error={error} retry={retry} />
      {c && (
        <>
          <header className="page-heading centered">
            <span className="badge">
              {c.kind === "tecnica" ? "Técnica" : "Universitaria"} · {c.area}
            </span>
            <h1>{c.name}</h1>
            <p className="lead">{c.content.description}</p>
          </header>
          <div className="detail-grid">
            {Object.entries(labels).map(([key, label]) => (
              <article className="card detail-card" key={key}>
                <div className="icon-tile">
                  <BookOpen size={21} />
                </div>
                <div>
                  <h2>{label}</h2>
                  <p>{c.comparison?.[key]}</p>
                </div>
              </article>
            ))}
          </div>
          <p className="info-strip">
            {c.curriculum_note} {c.cost_note}.
          </p>
          <div className="actions balanced">
            <button onClick={() => s.toggle(c.id)}>
              {s.selection.includes(c.id) ? (
                <Check size={18} />
              ) : (
                <Plus size={18} />
              )}{" "}
              {s.selection.includes(c.id)
                ? "Carrera seleccionada"
                : "Añadir carrera a comparación"}
            </button>
            <a href="#instituciones" className="button secondary">
              Ver instituciones y sedes <ArrowRight size={18} />
            </a>
          </div>
          <InstitutionExplorer offers={c.offers ?? []} />
          <AcademicOptions programs={c.institutional_programs ?? []} />
          <details className="sources">
            <summary>Fuentes y trazabilidad</summary>
            {c.sources?.map((url, i) => (
              <p key={url}>
                <a href={url} target="_blank" rel="noopener noreferrer">
                  Ficha institucional {i + 1} ↗
                </a>
              </p>
            ))}
            <p>
              Las descripciones generales son síntesis editoriales. Los costos y
              modalidades conservan el estado declarado en el catálogo original.
            </p>
          </details>
        </>
      )}
    </div>
  );
}
