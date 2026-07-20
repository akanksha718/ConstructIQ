import API_URL from "@/lib/api-client";
import { toast } from "sonner";
import type { DocumentAsset } from "@/types/documents";

export async function getRecentDocuments(token: string | null) {
  const response = await fetch(`${API_URL}/api/documents/recent`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    toast.error("Failed to fetch recent documents");
    throw new Error("Failed to fetch recent documents");
  }

  return response.json();
}

export async function getDocuments(token: string | null): Promise<DocumentAsset[]> {
  const response = await fetch(`${API_URL}/api/documents?limit=250`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store",
  });

  if (!response.ok) {
    const error = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(error?.detail || "Failed to fetch uploaded documents.");
  }

  return response.json() as Promise<DocumentAsset[]>;
}

export async function getDocumentAccessUrl(documentId: number): Promise<string> {
  const response = await fetch(`${API_URL}/api/documents/${documentId}/access-url`);
  const payload = (await response.json().catch(() => null)) as { url?: string; detail?: string } | null;
  if (!response.ok || !payload?.url) {
    throw new Error(payload?.detail || "Unable to open this document.");
  }
  return payload.url;
}
