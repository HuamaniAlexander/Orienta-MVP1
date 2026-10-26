import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Compass } from "lucide-react";
import { useApp } from "../app/state";
import { api } from "../shared/api";
import { useResource } from "../shared/useResource";
import { Feedback } from "../shared/Feedback";
import type {
  Questionnaire,
  Conditions,
  Recommendation,
  RecommendationInput,
} from "../shared/types";
export function QuestionnairePage() {
  const s = useApp(),
    [params] = useSearchParams(),
    navigate = useNavigate(),
    resource = useResource<Questionnaire>("/cuestionarios/actual");
  const [step, setStep] = useState(0),
    [responses, setResponses] = useState<Record<string, number | null>>(
      s.input?.responses ?? {},
    ),
    [conditions, setConditions] = useState<Conditions>(
      s.input?.conditions ?? {
        modalities: [],
        districts: [],
        monthly_budget: null,
        max_months: null,
        formation: "cualquiera",
      },
    ),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const ids =
    s.input?.career_ids ??
    (params.has("a") && params.has("b")
      ? [Number(params.get("a")), Number(params.get("b"))]
      : s.selection);
  if (ids.length !== 2)
    return (
      <section className="container page empty">
        <h1>Primero elige dos carreras</h1>
        <Link className="button" to="/carreras">
          Ir al catálogo
        </Link>
      </section>
    );
  const analyze = async () => {
    setBusy(true);
    setError("");
    const payload: RecommendationInput = {
      career_ids: ids,
      questionnaire_version: resource.data!.version,
      responses,
      conditions,
    };
    try {
      const result = await api<Recommendation>("/recomendaciones", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      s.setInput({ ...payload, catalog_version: result.catalog_version });
      s.setResult(result);
      navigate("/resultado");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };
  const question = resource.data?.questions[step],
    answered = question
      ? Object.prototype.hasOwnProperty.call(responses, question.id)
      : true;
  const toggle = (key: "modalities" | "districts", value: string) =>
    setConditions({
      ...conditions,
      [key]: conditions[key].includes(value)
        ? conditions[key].filter((x) => x !== value)
        : [...conditions[key], value],
    });
  return (
    <div className="container page">
      <div className="journey">
        <span>✓ Comparación</span>
        <strong>2. Tus intereses</strong>
        <span>3. Resultado</span>
      </div>
      <h1>Conozcamos tus intereses</h1>
      <p className="lead">
        No hay respuestas correctas. Puedes cambiar de opinión.
      </p>
      <Feedback {...resource} />
      {resource.data && (
        <div className="question-layout">
          <section>
            <div className="progress-label">
              <span>Pregunta {step + 1} de 12</span>
              <span>Tu exploración personal</span>
            </div>
            <progress
              value={step + 1}
              max={12}
              aria-label="Progreso del cuestionario"
            />
            <div className="card question-card">
              <span className="badge">
                {step < 8
                  ? "Intereses y actividades"
                  : "Condiciones de estudio"}
              </span>
              <fieldset>
                <legend>
                  {question?.text ??
                    [
                      "¿Qué modalidades podrías estudiar?",
                      "¿Qué distritos te gustaría explorar?",
                      "¿Cuál es tu presupuesto mensual de enseñanza?",
                      "¿Qué duración y tipo de formación prefieres?",
                    ][step - 8]}
                </legend>
                <p>
                  {step < 8
                    ? "Piensa en actividades que te gustaría explorar, aunque todavía no tengas experiencia."
                    : "Estos datos se revisan por institución; no cambian tus intereses."}
                </p>
                {question ? (
                  <>
                    <div className="rating-grid">
                      {["Nada", "Poco", "Intermedio", "Bastante", "Mucho"].map(
                        (label, i) => (
                          <label
                            key={label}
                            className={
                              responses[question.id] === i + 1
                                ? "rating selected"
                                : "rating"
                            }
                          >
                            <span>{i + 1}</span>
                            <strong>{label}</strong>
                            <input
                              type="radio"
                              name={question.id}
                              checked={responses[question.id] === i + 1}
                              onChange={() =>
                                setResponses({
                                  ...responses,
                                  [question.id]: i + 1,
                                })
                              }
                            />
                          </label>
                        ),
                      )}
                    </div>
                    <label className="unknown">
                      <input
                        type="radio"
                        name={question.id}
                        checked={responses[question.id] === null}
                        onChange={() =>
                          setResponses({ ...responses, [question.id]: null })
                        }
                      />
                      Aún no lo sé
                    </label>
                  </>
                ) : step === 8 || step === 9 ? (
                  <div className="choice-list">
                    {(step === 8
                      ? ["Presencial", "Virtual", "Semipresencial"]
                      : [
                          "Los Olivos",
                          "Independencia",
                          "Comas",
                          "Puente Piedra",
                          "San Martín de Porres",
                          "Carabayllo",
                          "Ancón",
                          "Santa Rosa",
                        ]
                    ).map((value) => (
                      <label key={value}>
                        <input
                          type="checkbox"
                          checked={conditions[
                            step === 8 ? "modalities" : "districts"
                          ].includes(value)}
                          onChange={() =>
                            toggle(
                              step === 8 ? "modalities" : "districts",
                              value,
                            )
                          }
                        />
                        {value}
                      </label>
                    ))}
                    <small>
                      Puedes dejar todas sin marcar si no tienes preferencia.
                    </small>
                  </div>
                ) : step === 10 ? (
                  <label>
                    Pensión mensual en soles (opcional)
                    <input
                      type="number"
                      min={0}
                      max={1000000}
                      placeholder="Ejemplo: 800"
                      value={conditions.monthly_budget ?? ""}
                      onChange={(e) =>
                        setConditions({
                          ...conditions,
                          monthly_budget:
                            e.target.value === ""
                              ? null
                              : Number(e.target.value),
                        })
                      }
                    />
                    <small>
                      No incluye matrícula, transporte ni materiales.
                    </small>
                  </label>
                ) : (
                  <div className="form-stack">
                    <label>
                      Duración máxima
                      <select
                        value={conditions.max_months ?? ""}
                        onChange={(e) =>
                          setConditions({
                            ...conditions,
                            max_months: e.target.value
                              ? Number(e.target.value)
                              : null,
                          })
                        }
                      >
                        <option value="">Sin preferencia</option>
                        <option value="36">3 años</option>
                        <option value="60">5 años</option>
                        <option value="84">7 años</option>
                      </select>
                    </label>
                    <label>
                      Tipo de formación
                      <select
                        value={conditions.formation}
                        onChange={(e) =>
                          setConditions({
                            ...conditions,
                            formation: e.target.value,
                          })
                        }
                      >
                        <option value="cualquiera">Cualquiera</option>
                        <option value="tecnica">Técnica</option>
                        <option value="universitaria">Universitaria</option>
                      </select>
                    </label>
                  </div>
                )}
              </fieldset>
              <div className="question-actions">
                <button
                  className="secondary"
                  disabled={step === 0 || busy}
                  onClick={() => setStep((x) => x - 1)}
                >
                  <ArrowLeft size={17} />
                  Anterior
                </button>
                <span className="subtle">
                  {answered ? "Puedes continuar" : "Elige una opción"}
                </span>
                {step < 11 ? (
                  <button
                    disabled={!answered}
                    onClick={() => setStep((x) => x + 1)}
                  >
                    Siguiente
                    <ArrowRight size={17} />
                  </button>
                ) : (
                  <button disabled={busy} onClick={analyze}>
                    {busy ? "Analizando…" : "Ver mi afinidad"}
                  </button>
                )}
              </div>
              <Feedback error={error} />
            </div>
          </section>
          <aside className="card question-help">
            <div className="compass-mini">
              <Compass size={80} />
            </div>
            <h2>Esto es una exploración</h2>
            <p>Relaciona tus intereses con las dos carreras que elegiste.</p>
            <hr />
            <h3>Puedes volver y editar</h3>
            <p>
              Una respuesta no te define. Cambia tus preferencias y explora
              otros caminos.
            </p>
            <h3>Una explicación para ti</h3>
            <p>
              Las respuestas de este cuestionario y tus preferencias pueden
              enviarse a Gemini para redactar tu orientación. No se envían tu
              correo ni tus credenciales.
            </p>
            <h3>La decisión es tuya</h3>
            <p>No es una evaluación psicológica ni una prueba de admisión.</p>
            <Link to="/comparar">Salir del cuestionario</Link>
          </aside>
        </div>
      )}
    </div>
  );
}
