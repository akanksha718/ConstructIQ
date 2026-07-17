import API_URL from "@/lib/api-client";

export type ChatCitation = {
  source_index: number;
  document_id: number | null;
  document: string;
  file_url: string | null;
  page: number | null;
  heading: string | null;
  section: string | null;
  excerpt: string | null;
};

export type ChatResponse = {
  answer: string;
  confidence: number;
  citations: ChatCitation[];
  related_equipment: string[];
  agent: string | null;
};

export async function askIndustrialCopilot(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    let message = "Unable to reach the industrial copilot right now.";

    try {
      const errorBody = (await response.json()) as { detail?: string };
      if (errorBody.detail) {
        message = errorBody.detail;
      }
    } catch {
      // Keep the generic fallback if the error body is not JSON.
    }

    throw new Error(message);
  }

  return (await response.json()) as ChatResponse;
}
