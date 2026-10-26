import { useEffect, useState, type FormEvent } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import {
  Compass,
  Eye,
  EyeOff,
  ShieldCheck,
  Bookmark,
  ArrowRight,
} from "lucide-react";
import { mutate } from "../shared/api";
import { Feedback } from "../shared/Feedback";
import { useApp } from "../app/state";
export function AuthPage({ register = false }: { register?: boolean }) {
  const [email, setEmail] = useState(""),
    [password, setPassword] = useState(""),
    [show, setShow] = useState(false),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [accepted, setAccepted] = useState(false),
    [policy, setPolicy] = useState(false),
    [params] = useSearchParams(),
    navigate = useNavigate(),
    s = useApp();
  useEffect(() => {
    setError("");
    setPassword("");
  }, [register]);
  const next = params.get("next") ?? "/mi-cuenta",
    safeNext =
      next.startsWith("/") && !next.startsWith("//") ? next : "/mi-cuenta";
  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await mutate(register ? "/auth/registro" : "/auth/login", {
        email,
        password,
      });
      if (register) {
        s.setNotice(
          "Cuenta creada. Inicia sesión para guardar tus comparaciones.",
        );
        navigate("/login?next=" + encodeURIComponent(safeNext));
      } else {
        await s.refreshUser();
        navigate(safeNext);
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="container auth-layout">
      <section className="auth-story">
        <p className="eyebrow">TU DECISIÓN, TU CAMINO</p>
        <h2>
          {register ? "Tu exploración, a tu ritmo." : "Retoma tu camino."}
        </h2>
        <p className="lead">
          Guarda tus comparaciones y vuelve a explorar cuando quieras.
        </p>
        <div className="auth-compass">
          <Compass size={160} strokeWidth={0.8} />
        </div>
        <p className="inline">
          <Bookmark />
          Tus opciones, en un solo lugar
        </p>
        <p className="inline">
          <ShieldCheck />
          Tú decides qué conservar
        </p>
      </section>
      <section className="card auth-card">
        <h1>{register ? "Crea tu cuenta" : "Inicia sesión"}</h1>
        <p>
          {register
            ? "Solo necesitamos lo esencial."
            : "Qué bueno tenerte de vuelta."}
        </p>
        <form className="form-stack" onSubmit={submit}>
          <label>
            Correo electrónico
            <input
              type="email"
              autoComplete="email"
              placeholder="tu.correo@ejemplo.com"
              maxLength={254}
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <label>
            Contraseña
            <div className="password-field">
              <input
                type={show ? "text" : "password"}
                aria-label="Contraseña"
                autoComplete={register ? "new-password" : "current-password"}
                minLength={12}
                maxLength={128}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button
                type="button"
                className="icon-button"
                aria-label={show ? "Ocultar contraseña" : "Mostrar contraseña"}
                onClick={() => setShow(!show)}
              >
                {show ? <EyeOff size={19} /> : <Eye size={19} />}
              </button>
            </div>
            {register && (
              <small>Usa una frase de al menos 12 caracteres.</small>
            )}
          </label>
          {register && (
            <>
              <label className="checkbox">
                <input
                  type="checkbox"
                  required
                  checked={accepted}
                  onChange={(e) => setAccepted(e.target.checked)}
                />
                He leído los términos y la política de privacidad.
              </label>
              <button
                type="button"
                className="text-button"
                onClick={() => setPolicy(!policy)}
              >
                Leer términos y privacidad
              </button>
              {policy && (
                <div className="privacy-text">
                  <p>
                    ORIENTA ofrece información orientativa; no garantiza
                    admisión, empleo o éxito. Consulta las fuentes
                    institucionales.
                  </p>
                  <p>
                    Guardamos tu correo, un hash de contraseña y los análisis
                    que decidas conservar. Puedes eliminar tus comparaciones en
                    Mi cuenta. Las respuestas no se usan para investigación sin
                    autorización independiente.
                  </p>
                  <p>
                    MVP académico. No incluyas información sensible. Contacta al
                    administrador del proyecto para eliminar tu cuenta.
                  </p>
                </div>
              )}
              <p className="info-strip">
                Tus respuestas no entrenarán modelos sin tu autorización.
              </p>
            </>
          )}
          <button disabled={busy} type="submit">
            {busy
              ? "Procesando…"
              : register
                ? "Crear cuenta"
                : "Iniciar sesión"}
            <ArrowRight size={18} />
          </button>
          <Feedback error={error} />
        </form>
        <p className="centered">
          {register ? "¿Ya tienes una cuenta?" : "¿Aún no tienes una cuenta?"}{" "}
          <Link
            to={
              (register ? "/login" : "/registro") +
              "?next=" +
              encodeURIComponent(safeNext)
            }
          >
            {register ? "Iniciar sesión" : "Crear cuenta"}
          </Link>
        </p>
        <div className="divider">¿Solo quieres explorar?</div>
        <Link className="button secondary full" to="/carreras">
          Continuar sin una cuenta
        </Link>
      </section>
    </div>
  );
}
