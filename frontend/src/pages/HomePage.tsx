import { Link } from "react-router-dom";
import {
  ArrowRight,
  BookOpen,
  Check,
  Compass,
  GraduationCap,
  HeartHandshake,
  Search,
  Scale,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
export function HomePage() {
  return (
    <div className="container">
      <section className="hero">
        <div>
          <p className="eyebrow">TU FUTURO, CON MÁS CLARIDAD</p>
          <h1>
            Compara opciones.
            <br />
            Encuentra tu <em>camino.</em>
          </h1>
          <p className="lead">
            Explora carreras, comprende sus diferencias y descubre cómo se
            relacionan con lo que te interesa.
          </p>
          <div className="actions">
            <Link className="button" to="/carreras">
              Explorar carreras <ArrowRight size={18} />
            </Link>
            <a className="button secondary" href="#como-funciona">
              Cómo funciona
            </a>
          </div>
          <p className="subtle inline">
            <ShieldCheck size={17} /> Compara sin crear una cuenta
          </p>
        </div>
        <div
          className="hero-art"
          aria-label="Ilustración de caminos académicos"
        >
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="compass-core">
            <Compass size={100} strokeWidth={1.2} />
          </div>
          <div className="float-card interests">
            <HeartHandshake /> Tus intereses
            <small>El inicio de tu exploración</small>
          </div>
          <div className="float-card career">
            <GraduationCap /> Tu próxima etapa
            <small>Conoce tus posibilidades</small>
          </div>
          <div className="float-card choice">
            <Check /> Dos carreras, más claridad
          </div>
          <span className="art-star">
            <Sparkles />
          </span>
          <span className="art-book">
            <BookOpen size={34} />
          </span>
        </div>
      </section>
      <section id="como-funciona" className="steps-grid">
        {[
          [
            Search,
            "1. Explora",
            "Conoce carreras y actividades que despierten tu curiosidad.",
          ],
          [
            Scale,
            "2. Compara",
            "Revisa cursos, habilidades, costos y caminos profesionales.",
          ],
          [
            Compass,
            "3. Descubre tu afinidad",
            "Relaciona tus intereses con las opciones que elegiste.",
          ],
        ].map(([Icon, title, text]) => {
          const Component = Icon as typeof Search;
          return (
            <article className="card step" key={String(title)}>
              <div className="icon-tile">
                <Component />
              </div>
              <div>
                <h2>{String(title)}</h2>
                <p>{String(text)}</p>
              </div>
            </article>
          );
        })}
      </section>
      <section className="trust">
        <ShieldCheck />
        <div>
          <strong>Información con fuentes visibles</strong>
          <p>
            Consulta los planes institucionales y distingue las referencias de
            los datos revisados.
          </p>
        </div>
        <div>
          <strong>Primero la carrera. Después, dónde estudiarla.</strong>
          <p>
            Explora instituciones, mallas y sedes cuando hayas encontrado tus
            opciones.
          </p>
        </div>
      </section>
    </div>
  );
}
