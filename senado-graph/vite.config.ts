import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  define: {
    "process.env.NEO4J_URI": JSON.stringify(
      process.env.NEO4J_URI || "bolt://localhost:7687",
    ),
    "process.env.NEO4J_USERNAME": JSON.stringify(
      process.env.NEO4J_USERNAME || "neo4j",
    ),
    "process.env.NEO4J_PASSWORD": JSON.stringify(
      process.env.NEO4J_PASSWORD || "password",
    ),
  },
});
