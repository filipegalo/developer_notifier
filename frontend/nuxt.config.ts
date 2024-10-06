import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],

  tailwindcss: {
    config: {
      darkMode: "class",
    },
  },

  app: {
    head: {
      title: "Developer Notifier",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          hid: "description",
          name: "description",
          content: "A notification system for developers",
        },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/icon.ico" }],
    },
  },

  compatibilityDate: "2024-10-04",
  alias: {
    "@": ".",
  },
});
