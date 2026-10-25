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
      <div className="results-grid">
        {result.results.map((c, i) => (
          <article className="card result-card" key={c.career_id}>
            <span className="meta">CAMINO {i + 1}</span>
            <h2>{c.name}</h2>
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
            ) : (
              <div className="qualitative">
                <Info size={24} />
                <h3>Explora las actividades de esta carrera</h3>
                <p>
                  El índice requiere un perfil académico con revisión
                  especializada. No asignamos puntuaciones sin esa revisión.
                </p>
              </div>
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
      <p className="explanation">{result.explanation.text}</p>
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
