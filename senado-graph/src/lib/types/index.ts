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
export type NodeType = "senator" | "law" | "party" | "committee" | "lobbyist";

export type EdgeType =
  | "authored"
  | "member_of"
  | "belongs_to"
  | "lobby"
  | "voted_same"
  | "voted_on";

export interface GraphNode {
  data: {
    id: string;
    label: string;
    type: NodeType;
    color?: string;
    size?: number;
    status?: LawStatus;
    ideology?: string;
    lobbyistType?: LobbyistType;
    party?: string;
    region?: string;
    agreement?: number;
    memberCount?: number;
    [key: string]: unknown;
  };
}

export interface GraphEdge {
  data: {
    id: string;
    source: string;
    target: string;
    label?: string;
    type: EdgeType;
    agreement?: number;
    strength?: number;
    vote?: VoteType;
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
  relationshipTypes?: EdgeType[];
  activeOnly?: boolean;
  entityTypes?: NodeType[];
  lawStatuses?: LawStatus[];
  agreementRange?: {
    min: number;
    max: number;
  };
  lobbyistTypes?: LobbyistType[];
}

export interface FilterPreset {
  id: string;
  nameEs: string;
  nameEn: string;
  descriptionEs: string;
  descriptionEn: string;
  filters: GraphFilters;
}
