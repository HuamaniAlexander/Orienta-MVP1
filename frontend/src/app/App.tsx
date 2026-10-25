import { NavLink, Route, Routes, useLocation, Link } from "react-router-dom";
import { Compass, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useApp } from "./state";
import { HomePage } from "../pages/HomePage";
import { CatalogPage } from "../pages/CatalogPage";
import { CareerPage } from "../pages/CareerPage";
import { ComparePage } from "../pages/ComparePage";
import { QuestionnairePage } from "../pages/QuestionnairePage";
import { ResultPage } from "../pages/ResultPage";
import { AuthPage } from "../pages/AuthPage";
import { AccountPage } from "../pages/AccountPage";
export function App() {
  const s = useApp(),
    location = useLocation();
  const [open, setOpen] = useState(false);
  useEffect(() => {
    window.scrollTo(0, 0);
    setOpen(false);
    document.getElementById("main")?.focus();
  }, [location.pathname]);
  return (
    <>
      <a className="skip" href="#main">
        Saltar al contenido
      </a>
      <header className="header">
        <div className="nav-wrap">
          <Link to="/" className="brand" aria-label="ORIENTA, inicio">
            ORIENTA<span>_</span>
          </Link>
          <button
            className="menu-toggle"
            aria-label="Abrir navegación"
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            <Menu />
          </button>
          <nav aria-label="Principal" className={open ? "open" : ""}>
            <NavLink to="/" end>
              Inicio
            </NavLink>
            <NavLink to="/carreras">Explorar carreras</NavLink>
            <NavLink
              to={`/comparar${s.selection.length === 2 ? `?a=${s.selection[0]}&b=${s.selection[1]}` : ""}`}
            >
              Comparar
            </NavLink>
          </nav>
          <div className="auth-nav">
            {s.user ? (
              <>
                <NavLink to="/mi-cuenta">Mi cuenta</NavLink>
                <button
                  className="text-button"
                  onClick={() =>
                    s.logout().catch((e) => s.setNotice(e.message))
                  }
                >
                  Cerrar sesión
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login">Iniciar sesión</NavLink>
                <Link className="button small" to="/registro">
                  Crear cuenta
                </Link>
              </>
            )}
          </div>
        </div>
      </header>
      {s.notice && (
        <div className="toast" role="status">
          {s.notice}
          <button aria-label="Cerrar aviso" onClick={() => s.setNotice("")}>
            <X size={18} />
          </button>
        </div>
      )}
      <main id="main" tabIndex={-1}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/carreras" element={<CatalogPage />} />
          <Route path="/carreras/:id" element={<CareerPage />} />
          <Route path="/comparar" element={<ComparePage />} />
          <Route path="/orientacion" element={<QuestionnairePage />} />
          <Route path="/resultado" element={<ResultPage />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/registro" element={<AuthPage register />} />
          <Route path="/mi-cuenta" element={<AccountPage />} />
          <Route
            path="*"
            element={
              <section className="container empty">
                <Compass />
                <h1>Este camino no existe</h1>
                <Link className="button" to="/carreras">
                  Volver a explorar
                </Link>
              </section>
            }
          />
        </Routes>
      </main>
      <footer className="footer">
        <span className="brand">
          ORIENTA<span>_</span>
        </span>
        <p>Información para explorar. La decisión final siempre es tuya.</p>
        <Link to="/carreras">Explorar carreras →</Link>
      </footer>
    </>
  );
}
