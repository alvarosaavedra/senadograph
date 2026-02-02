import neo4j from "neo4j-driver";
import { NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD } from "$env/static/private";
import type { Driver } from "neo4j-driver";

let driver: Driver | null = null;
let connectionFailed = false;

export function getDriver(): Driver | null {
  if (connectionFailed) {
    return null;
  }
  
  if (!driver) {
    try {
      driver = neo4j.driver(
        NEO4J_URI,
        neo4j.auth.basic(NEO4J_USERNAME, NEO4J_PASSWORD),
      );
    } catch (err) {
      console.error("Failed to create Neo4j driver:", err);
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
    driver = undefined as unknown as Driver;
  }
}
