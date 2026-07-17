import API_URL from "@/lib/api-client";

export interface KnowledgeStats {
  documents_uploaded: number;
  knowledge_entities: number;
  equipment_tags: number;
  relationships_built: number;
}

export async function getStats(): Promise<KnowledgeStats> {
  const response = await fetch(`${API_URL}/api/stats`, {
    method: "GET",
    cache: "no-store",
  });

  const data = await response.json().catch(() => null);

  if (!response.ok || !data) {
    throw new Error("Failed to load stats");
  }

  return data as KnowledgeStats;
}
