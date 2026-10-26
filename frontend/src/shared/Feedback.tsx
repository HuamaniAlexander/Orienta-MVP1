import { AlertCircle, LoaderCircle } from "lucide-react";
export function Feedback({
  loading,
  error,
  retry,
}: {
  loading?: boolean;
  error?: string;
  retry?: () => void;
}) {
  if (loading)
    return (
      <div className="feedback" role="status">
        <LoaderCircle className="spin" /> Cargando información…
      </div>
    );
  if (error)
    return (
      <div className="feedback error" role="alert">
        <AlertCircle />
        <span>{error}</span>
        {retry && <button onClick={retry}>Reintentar</button>}
      </div>
    );
  return null;
}
export function Money({
  offer,
}: {
  offer: {
    cost: string | null;
    cost_min?: string | null;
    cost_max?: string | null;
    cost_status: string;
  };
}) {
  const money = (n: string) =>
    new Intl.NumberFormat("es-PE", {
      style: "currency",
      currency: "PEN",
      maximumFractionDigits: 0,
    }).format(Number(n));
  return (
    <>
      <strong>
        {offer.cost_status === "estimado"
          ? "Consultar tarifa institucional"
          : offer.cost_min && offer.cost_max
            ? `${money(offer.cost_min)}–${money(offer.cost_max)}`
            : offer.cost !== null
              ? money(offer.cost)
              : "Ver tarifario institucional"}
      </strong>
      <small>
        {offer.cost_status === "estimado"
          ? "El costo se determina por programa y modalidad"
          : "Enseñanza mensual · condiciones en fuente"}
      </small>
    </>
  );
}
