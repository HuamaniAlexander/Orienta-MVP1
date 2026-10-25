import { Link } from "react-router-dom";
import {
  Check,
  Plus,
  ArrowUpRight,
  Code2,
  BriefcaseBusiness,
  HeartPulse,
  Landmark,
  Brain,
  Building2,
} from "lucide-react";
import type { Career } from "../../shared/types";
import { useApp } from "../../app/state";
const icons: Record<string, typeof Code2> = {
  Ingeniería: Code2,
  Negocios: BriefcaseBusiness,
  Salud: HeartPulse,
  Psicología: Brain,
  Derecho: Landmark,
  Arquitectura: Building2,
};
export function CareerCard({ career }: { career: Career }) {
  const s = useApp(),
    selected = s.selection.includes(career.id),
    Icon = icons[career.area] ?? Code2;
  return (
    <article className={`card career-card ${selected ? "selected" : ""}`}>
      <div className={`career-art area-${career.area_code}`}>
        <Icon size={54} strokeWidth={1.25} />
        <span>{career.area}</span>
      </div>
      <div className="career-body">
        <div className="meta">
          {career.kind === "tecnica"
            ? "Formación técnica"
            : "Formación universitaria"}
        </div>
        <h2>{career.name}</h2>
        <p>{career.content.description}</p>
        <div className="tags">
          <span>{career.area}</span>
          <span>Explora sus especialidades</span>
        </div>
        <div className="card-actions">
          <Link to={`/carreras/${career.id}`}>
            Ver carrera <ArrowUpRight size={15} />
          </Link>
          <button
            className={selected ? "selected-button" : "secondary small"}
            aria-pressed={selected}
            onClick={() => s.toggle(career.id)}
          >
            {selected ? <Check size={16} /> : <Plus size={16} />}{" "}
            {selected ? "Seleccionada" : "Comparar"}
          </button>
        </div>
      </div>
    </article>
  );
}
