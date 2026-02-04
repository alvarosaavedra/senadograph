import { register, init, locale, waitLocale } from "svelte-i18n";
import { browser } from "$app/environment";

// Re-export _ from svelte-i18n for convenience
export { _ } from "svelte-i18n";

// Register locales
register("es", () => import("./es.json"));
register("en", () => import("./en.json"));

// Initialize i18n immediately (for SSR)
const defaultLocale = "es";

// Set up i18n with default locale
init({
  fallbackLocale: defaultLocale,
  initialLocale: defaultLocale,
});

// Function to update locale on client side and wait for it to load
export async function setupI18n(): Promise<void> {
  if (browser) {
    const savedLang = localStorage.getItem("language");
    if (savedLang && (savedLang === "es" || savedLang === "en")) {
      locale.set(savedLang);
    }
  }
  await waitLocale();
}

// Set language
export function setLanguage(lang: "es" | "en") {
  if (browser) {
    localStorage.setItem("language", lang);
    locale.set(lang);
  }
}
