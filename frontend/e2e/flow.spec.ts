import { test, expect } from "@playwright/test";
test("invitado compara, responde y guarda en historial privado", async ({
  page,
}) => {
  await page.goto("/carreras");
  await expect(
    page.getByRole("heading", {
      name: "Explora carreras y descubre tu camino",
    }),
  ).toBeVisible();
  const cards = page.locator(".career-card");
  await cards
    .nth(0)
    .getByRole("button", { name: "Comparar", exact: true })
    .click();
  await cards
    .nth(1)
    .getByRole("button", { name: "Comparar", exact: true })
    .click();
  await page
    .getByRole("link", { name: "Comparar carreras", exact: true })
    .click();
  await expect(page.locator("tbody tr")).toHaveCount(12);
  await page.getByRole("link", { name: "Analizar mi afinidad" }).click();
  for (let i = 0; i < 8; i++) {
    await page.getByRole("radio").nth(3).check();
    await page.getByRole("button", { name: "Siguiente" }).click();
  }
  for (let i = 0; i < 3; i++)
    await page.getByRole("button", { name: "Siguiente" }).click();
  await page.getByRole("button", { name: "Ver mi afinidad" }).click();
  await expect(
    page.getByRole("heading", {
      name: "Así se relacionan estas carreras contigo",
    }),
  ).toBeVisible();
  await expect(page.locator(".result-card")).toHaveCount(2);
  await page.getByRole("button", { name: "Guardar comparación" }).click();
  await expect(
    page.getByRole("heading", { name: "Inicia sesión" }),
  ).toBeVisible();
  await page
    .getByRole("link", { name: "Crear cuenta", exact: true })
    .last()
    .click();
  const email = `e2e-${Date.now()}@example.com`;
  await page.getByLabel("Correo electrónico").fill(email);
  await page
    .getByLabel("Contraseña", { exact: true })
    .fill("una-frase-segura-2026");
  await page.getByRole("checkbox").check();
  await page.getByRole("button", { name: "Crear cuenta", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Inicia sesión" }),
  ).toBeVisible();
  await page.getByLabel("Correo electrónico").fill(email);
  await page
    .getByLabel("Contraseña", { exact: true })
    .fill("una-frase-segura-2026");
  await page
    .getByRole("button", { name: "Iniciar sesión", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Guardar comparación" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Guardar comparación" }).click();
  await expect(
    page.getByRole("button", { name: "Comparación guardada", exact: true }),
  ).toBeDisabled();
  await page.getByRole("link", { name: "Mi cuenta", exact: true }).click();
  await expect(page.locator(".history-item")).toHaveCount(1);
  await page.getByRole("button", { name: "Eliminar", exact: true }).click();
  await page
    .getByRole("button", { name: "Eliminar comparación", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Aún no guardaste comparaciones" }),
  ).toBeVisible();
});
test("vista móvil permite explorar y muestra errores de búsqueda", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/carreras");
  await page
    .getByRole("textbox", { name: "Buscar carrera" })
    .fill("carrera-sin-coincidencias");
  await page.getByRole("button", { name: "Buscar", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "No encontramos coincidencias" }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});

test("programas institucionales, costos y opciones técnicas", async ({
  page,
}) => {
  await page.goto("/carreras/0");
  await expect(page.locator(".academic-card")).toHaveCount(2);
  const cards = page.locator(".academic-card");
  await cards
    .nth(0)
    .getByRole("button", { name: "Comparar programa", exact: true })
    .click();
  await cards
    .nth(1)
    .getByRole("button", { name: "Comparar programa", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Compara los planes institucionales" }),
  ).toBeVisible();
  await page.goto("/instituciones/vesalio");
  await expect(
    page.getByRole("heading", { name: "André Vesalio", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".academic-card")).toHaveCount(2);
  await expect(page.locator(".published-price").first()).toContainText("250");
  await page.goto("/carreras?kind=tecnica");
  await expect(page.locator(".career-card")).toHaveCount(2);
});
