import { useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Bookmark, ArrowRight, Check, Info } from "lucide-react";
import { useApp } from "../app/state";
import { mutate } from "../shared/api";
import { Feedback } from "../shared/Feedback";
import type { SavedComparison } from "../shared/types";
export function ResultPage() {
  const s = useApp(),
    navigate = useNavigate(),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    key = useRef(crypto.randomUUID());
  const result = s.result;
  if (!result)
    return (
      <section className="container page empty">
        <h1>Tu próxima exploración empieza aquí</h1>
        <p>
          El resultado se conserva durante esta sesión. También puedes abrir un
          análisis desde Mi cuenta.
        </p>
        <Link className="button" to="/carreras">
          Elegir dos carreras
        </Link>
      </section>
    );
  const save = async () => {
    if (!s.user) {
      navigate("/login?next=/resultado");
      return;
    }
    if (!s.input) return;
    setBusy(true);
    try {
      const saved = await mutate<SavedComparison>(
        "/comparaciones",
        s.input,
        "POST",
        { "Idempotency-Key": key.current },
      );
      s.setResult(saved.result);
      s.setNotice("Comparación guardada en tu historial privado.");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="container page">
      <div className="section-top">
        <div>
          <h1>Así se relacionan estas carreras contigo</h1>
          <p className="lead">
            Comprende las razones y decide qué opción quieres explorar mejor.
          </p>
        </div>
        <span className="badge warning">
          {result.demo ? "Ejemplo ilustrativo" : "Orientación explicable"}
        </span>
      </div>
      {result.content_preference?.status === "closer_content" && (
        <section className="card recommendation-summary">
          <h2>
            Empieza explorando{" "}
            {
              result.results.find(
                (c) => c.career_id === result.content_preference?.career_id,
              )?.name
            }
          </h2>
          <p>
            Sus temas se acercan más a los intereses que indicaste. Compara las
            razones de ambas opciones y revisa sus planes antes de decidir.
          </p>
        </section>
      )}
      {result.content_preference?.status === "similar_content" && (
        <p className="info-strip">
          Las dos carreras presentan una coincidencia temática cercana. Explora
          sus actividades y planes para distinguirlas.
        </p>
      )}
      <div className="results-grid">
        {result.results.map((c, i) => (
          <article className="card result-card" key={c.career_id}>
            <span className="meta">CAMINO {i + 1}</span>
            <h2>{c.name}</h2>
            {c.content_match && c.content_match.score === null && (
              <p className="info-strip">
                Revisa tus respuestas e indica las actividades que te interesan
                para obtener una comparación temática.
              </p>
            )}
            {c.content_match?.score != null && (
              <section className="content-match">
                <h3>Coincidencia con los temas que te interesan</h3>
                <div className="score">
                  {Math.round(c.content_match.score)}
                  <span>/ 100</span>
                </div>
                <p>
                  Similitud entre tus intereses y el contenido académico. No
                  mide tu capacidad ni garantiza éxito.
                </p>
                {c.content_match.source_url && (
                  <a
                    href={c.content_match.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Explorar el programa que sustenta esta coincidencia ↗
                  </a>
                )}
              </section>
            )}
            {c.affinity.index !== null ? (
              <>
                <div className="score">
                  {Math.round(c.affinity.index)}
                  <span>/ 100</span>
                </div>
                <strong>Índice de afinidad con tus intereses</strong>
                <progress
                  value={c.affinity.index}
                  max={100}
                  aria-label={`Índice de afinidad de ${c.name}`}
                />
                <small>
                  {c.affinity.coverage} de 6 dimensiones con información
                </small>
              </>
            ) : !c.content_match ? (
              <div className="qualitative">
                <Info size={24} />
                <h3>Explora las actividades de esta carrera</h3>
                <p>
                  El índice requiere un perfil académico con revisión
                  especializada. No asignamos puntuaciones sin esa revisión.
                </p>
              </div>
            ) : null}
            {c.narrative && (
              <section className="ai-narrative">
                <h3>Por qué puede interesarte</h3>
                <p>{c.narrative}</p>
                <strong>Tu siguiente paso</strong>
                <p>{c.next_step}</p>
              </section>
            )}
            <div className="reasons">
              {c.reasons.map((r) => (
                <div key={r.id}>
                  <Check size={18} />
                  <p>{r.text}</p>
                </div>
              ))}
            </div>
            <div className="result-facts">
              <span>
                Pensión entre instituciones<strong>{c.comparison.cost}</strong>
              </span>
              <span>
                Inversión adicional<strong>{c.comparison.investment}</strong>
              </span>
            </div>
            <details className="sources">
              <summary>Revisar condiciones por institución</summary>
              {c.institutional_programs?.map((p) => (
                <div className="offer-conditions" key={p.id}>
                  <strong>
                    {p.institution_name} · {p.name}
                  </strong>
                  <p>
                    Presupuesto por cuota publicada:{" "}
                    {
                      (
                        {
                          compatible: "dentro del presupuesto indicado",
                          incompatible: "supera el presupuesto indicado",
                          depends_on_scale: "depende de la escala asignada",
                          no_preference: "sin preferencia de presupuesto",
                          review_source:
                            "consulta las condiciones institucionales",
                        } as Record<string, string>
                      )[p.budget_status]
                    }
                  </p>
                  {p.tuition && (
                    <small>
                      Periodo {p.tuition.period}. {p.tuition.scope}
                    </small>
                  )}
                </div>
              ))}
              {c.offers.map((o) => (
                <div key={o.id} className="offer-conditions">
                  <strong>
                    {o.institution.name} · {o.modality}
                  </strong>
                  <p>
                    {Object.entries(o.feasibility ?? {})
                      .map(
                        ([key, value]) =>
                          `${({ budget: "Presupuesto", modality: "Modalidad", district: "Distrito", duration: "Duración", formation: "Formación" } as Record<string, string>)[key] ?? key}: ${({ compatible: "compatible", incompatible: "fuera de tu preferencia", no_preference: "sin preferencia", review_source: "revisar alcance en fuente", review_institution: "elegir sede" } as Record<string, string>)[value] ?? value}`,
                      )
                      .join(" · ")}
                  </p>
                </div>
              ))}
            </details>
            <Link
              className="button secondary"
              to={`/carreras/${c.career_id}#instituciones`}
            >
              Ver instituciones y sedes
              <ArrowRight size={17} />
            </Link>
          </article>
        ))}
      </div>
      <p className="info-strip">
        <Info size={17} />
        {result.notice} Las condiciones se revisan por institución y distrito.
      </p>
      <section className="card explanation">
        <h2>
          {result.explanation.mode === "gemini_grounded"
            ? "Tu orientación personalizada con IA"
            : "Guía para tu decisión"}
        </h2>
        <p>{result.explanation.text}</p>
      </section>
      {result.preference.status === "similar_affinity" && (
        <p className="info-strip">
          Ambas carreras presentan una afinidad similar.
        </p>
      )}
      {result.preference.status === "explore_more" && (
        <p className="info-strip">
          Conviene explorar más carreras antes de elegir.
        </p>
      )}
      <div className="actions centered">
        <Link className="button secondary" to="/orientacion">
          Editar respuestas
        </Link>
        <button onClick={save} disabled={busy || result.saved}>
          <Bookmark size={18} />
          {result.saved
            ? "Comparación guardada"
            : busy
              ? "Guardando…"
              : "Guardar comparación"}
        </button>
        <Link className="button secondary" to="/carreras">
          Volver a comparar
        </Link>
      </div>
      <Feedback error={error} />
      <p className="subtle centered">
        Motor {result.engine_version} · Cuestionario{" "}
        {result.questionnaire_version} · Tus respuestas no entrenan un modelo
        automáticamente.
      </p>
    </div>
  );
}
