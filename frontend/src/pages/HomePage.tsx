import { Link } from "react-router-dom";
import { ArrowRight, Compass, Search, Scale, ShieldCheck } from "lucide-react";
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
        <figure className="hero-visual">
          <img
            src="/images/orienta-explora-1280.webp"
            srcSet="/images/orienta-explora-640.webp 640w, /images/orienta-explora-1280.webp 1280w"
            sizes="(max-width: 760px) 100vw, 50vw"
            width="1280"
            height="720"
            fetchPriority="high"
            alt="Jóvenes compartiendo ideas y explorando caminos de formación"
          />
          <figcaption>Tu curiosidad es el punto de partida.</figcaption>
        </figure>
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
      <section className="institution-callout card">
        <div>
          <p className="eyebrow">CERCA DE TI</p>
          <h2>Encuentra dónde seguir tu camino</h2>
          <p>Universidades, institutos y escuelas organizados por distrito.</p>
        </div>
        <Link className="button" to="/instituciones">
          Conocer instituciones <ArrowRight size={18} />
        </Link>
      </section>
      <section className="trust">
        <ShieldCheck />
        <div>
          <strong>Información con fuentes visibles</strong>
          <p>
            Consulta las fuentes de cada ficha y los planes de estudio
            publicados por las instituciones.
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
