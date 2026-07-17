import API_URL from "@/lib/api-client";

export async function uploadDocuments(
  files: File[],
  token: string|null
) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(`${API_URL}/api/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  const data = await response.json().catch(() => ({
    message: "Upload failed",
  }));

  if (!response.ok) {
    throw new Error(data.message);
  }

  return data;
}