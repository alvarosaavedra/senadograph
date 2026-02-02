// Senator types
export interface Senator {
  id: string;
  name: string;
  nameEn?: string;
  party: string;
  region: string;
  regionEn?: string;
  email?: string;
  photoUrl?: string;
  biography?: string;
  biographyEn?: string;
  startDate?: string;
  active: boolean;
}

// Party types
export interface Party {
  id: string;
  name: string;
  nameEn?: string;
  shortName: string;
  color: string;
  ideology?: string;
}

// Law types
export type LawStatus = "approved" | "rejected" | "in_discussion" | "withdrawn";

export interface Law {
  id: string;
  boletin: string;
  title: string;
  titleEn?: string;
  description?: string;
  descriptionEn?: string;
  dateProposed: string;
  status: LawStatus;
  topic?: string;
}

// Vote types
export type VoteType = "favor" | "against" | "abstained" | "absent";

export interface Vote {
  id: string;
  date: string;
  session: string;
  result: string;
}

// Committee types
export interface Committee {
  id: string;
  name: string;
  nameEn?: string;
}

// Lobbyist types
export type LobbyistType = "company" | "union" | "ngo" | "professional_college";

export interface Lobbyist {
  id: string;
  name: string;
  type: LobbyistType;
  industry?: string;
  industryEn?: string;
}

// Graph data types
export interface GraphNode {
  data: {
    id: string;
    label: string;
    type: "senator" | "law" | "party" | "committee" | "lobbyist";
    color?: string;
    size?: number;
    [key: string]: unknown;
  };
}

export interface GraphEdge {
  data: {
    id: string;
    source: string;
    target: string;
    label?: string;
    type: string;
    [key: string]: unknown;
  };
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// Filter types
export interface GraphFilters {
  parties?: string[];
  committees?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  topics?: string[];
  relationshipTypes?: string[];
  activeOnly?: boolean;
}
