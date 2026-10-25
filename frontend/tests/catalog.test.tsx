import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, it, vi } from "vitest";
import { CareerCard } from "../src/features/catalog/CareerCard";
const toggle = vi.fn();
vi.mock("../src/app/state", () => ({
  useApp: () => ({ selection: [0], toggle }),
}));
it("muestra selección con texto y estado accesible, no solo color", () => {
  render(
    <MemoryRouter>
      <CareerCard
        career={{
          id: 0,
          slug: "sistemas",
          name: "Ingeniería de Sistemas",
          area: "Ingeniería",
          area_code: 0,
          kind: "universitaria",
          content: { description: "Soluciones digitales" },
          version: "1",
        }}
      />
    </MemoryRouter>,
  );
  const selected = screen.getByRole("button", { name: /Seleccionada/ });
  expect(selected).toHaveAttribute("aria-pressed", "true");
  fireEvent.click(selected);
  expect(toggle).toHaveBeenCalledWith(0);
  expect(screen.getByRole("link", { name: /Ver carrera/ })).toHaveAttribute(
    "href",
    "/carreras/0",
  );
});
