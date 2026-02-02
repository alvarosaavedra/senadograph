import neo4j from "neo4j-driver";
import type { Driver } from "neo4j-driver";

let driver: Driver | null = null;
let connectionFailed = false;

export function getDriver(): Driver | null {
  if (connectionFailed) {
    return null;
  }

  if (!driver) {
    try {
      const NEO4J_URI = process.env.NEO4J_URI || import.meta.env.NEO4J_URI;
      const NEO4J_USERNAME =
        process.env.NEO4J_USERNAME || import.meta.env.NEO4J_USERNAME;
      const NEO4J_PASSWORD =
        process.env.NEO4J_PASSWORD || import.meta.env.NEO4J_PASSWORD;

      if (!NEO4J_URI || !NEO4J_USERNAME || !NEO4J_PASSWORD) {
        console.warn("Neo4j credentials not configured, using mock data");
        connectionFailed = true;
        return null;
      }

      driver = neo4j.driver(
        NEO4J_URI,
        neo4j.auth.basic(NEO4J_USERNAME, NEO4J_PASSWORD),
      );
    } catch (err) {
      console.error("Neo4j: Failed to create driver:", err);
      connectionFailed = true;
      return null;
    }
  }
  return driver;
}

export function isConnectionFailed(): boolean {
  return connectionFailed;
}

export async function closeDriver(): Promise<void> {
  if (driver) {
    await driver.close();
    driver = null;
  }
}
