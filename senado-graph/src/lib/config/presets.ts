import type { FilterPreset, GraphFilters } from "$lib/types";

export const presets: FilterPreset[] = [
  {
    id: "polarization",
    nameEs: "Polarización Partidista",
    nameEn: "Partisan Polarization",
    descriptionEs:
      "Visualice cómo los partidos votan de manera diferente e identifique los límites entre partidos",
    descriptionEn:
      "Visualize how parties vote differently and identify party boundaries",
    filters: {
      entityTypes: ["senator", "party"],
      relationshipTypes: ["belongs_to", "voted_same"],
      agreementRange: { min: 0, max: 60 },
      activeOnly: true,
    },
  },
  {
    id: "cross-party",
    nameEs: "Alianzas Transpartidistas",
    nameEn: "Cross-Party Allies",
    descriptionEs:
      "Encuentre senadores que colaboran a través de las líneas partidistas a pesar de diferentes afiliaciones",
    descriptionEn:
      "Find senators who collaborate across party lines despite different affiliations",
    filters: {
      entityTypes: ["senator", "party"],
      relationshipTypes: ["belongs_to", "voted_same"],
      agreementRange: { min: 70, max: 100 },
      activeOnly: true,
    },
  },
  {
    id: "power-brokers",
    nameEs: "Mediadores de Poder",
    nameEn: "Power Brokers",
    descriptionEs:
      "Identifique los senadores más influyentes a través de leyes autorizadas, comités y conexiones",
    descriptionEn:
      "Identify most influential senators through authored laws, committees, and connections",
    filters: {
      entityTypes: ["senator", "law", "committee", "party"],
      relationshipTypes: ["authored", "member_of", "belongs_to"],
      lawStatuses: ["approved"],
      activeOnly: true,
    },
  },
  {
    id: "industry-influence",
    nameEs: "Influencia Industrial",
    nameEn: "Industry Influence",
    descriptionEs: "Revele qué industrias/lobistas influyen en qué senadores",
    descriptionEn: "Reveal which industries/lobbyists influence which senators",
    filters: {
      entityTypes: ["senator", "lobbyist"],
      relationshipTypes: ["lobby"],
      activeOnly: true,
    },
  },
  {
    id: "legislative-collaboration",
    nameEs: "Colaboración Legislativa",
    nameEn: "Legislative Collaboration",
    descriptionEs:
      "Muestre patrones de colaboración a través de la autoría de leyes y patrones de votación",
    descriptionEn:
      "Show collaboration patterns through law authorship and voting patterns",
    filters: {
      entityTypes: ["senator", "law", "party"],
      relationshipTypes: ["authored", "voted_on", "voted_same", "belongs_to"],
      agreementRange: { min: 60, max: 100 },
      lawStatuses: ["approved", "in_discussion"],
      activeOnly: true,
    },
  },
];

export function getPreset(id: string): FilterPreset | undefined {
  return presets.find((p) => p.id === id);
}

export function applyPreset(id: string): GraphFilters | undefined {
  const preset = getPreset(id);
  return preset?.filters;
}
