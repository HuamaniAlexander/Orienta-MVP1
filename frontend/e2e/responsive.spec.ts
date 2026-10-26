import { test, expect } from "@playwright/test";
for (const width of [320, 390, 768, 1024, 1440, 1920]) {
  test(`inicio y directorio sin desbordamiento a ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 900 });
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    for (const path of ["/", "/instituciones"]) {
      await page.goto(path);
      await expect(page.locator("main h1")).toBeVisible();
      if (path === "/instituciones")
        await expect(page.locator(".institution-card")).toHaveCount(17);
      const image = page.locator("main img");
      await expect(image).toBeVisible();
      await expect
        .poll(() =>
          image.evaluate(
            (node: HTMLImageElement) => node.complete && node.naturalWidth > 0,
          ),
        )
        .toBe(true);
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
    }
    await page
      .getByRole("combobox", { name: "Distrito", exact: true })
      .selectOption("Comas");
    await expect(page.locator(".institution-card")).toHaveCount(3);
    await page.getByRole("button", { name: "Limpiar filtros" }).click();
    await expect(page.locator(".institution-card")).toHaveCount(17);
    for (const path of [
      "/carreras",
      "/carreras/0",
      "/comparar?a=0&b=1",
      "/orientacion?a=0&b=1",
      "/resultado",
      "/login",
      "/registro",
      "/mi-cuenta",
    ]) {
      await page.goto(path);
      await expect(page.locator("main h1")).toBeVisible();
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
        path,
      ).toBe(true);
    }
    if (process.env.E2E_SCREENSHOT_DIR) {
      await page.goto("/");
      await page.screenshot({
        path: `${process.env.E2E_SCREENSHOT_DIR}/inicio-${width}.png`,
        fullPage: true,
      });
      await page.goto("/instituciones");
      await expect(page.locator(".institution-card")).toHaveCount(17);
      await page.screenshot({
        path: `${process.env.E2E_SCREENSHOT_DIR}/instituciones-${width}.png`,
        fullPage: true,
      });
    }
    expect(errors).toEqual([]);
  });
}
