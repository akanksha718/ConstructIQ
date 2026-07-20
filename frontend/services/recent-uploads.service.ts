 import API_URL from "@/lib/api-client";
 
 export interface RecentUploadItem {
   id: number;
   filename: string;
   file_type: string;
   uploaded_by: string;
   created_at: string;
   processing_status: string;
   file_size: number;
 }
 
 export async function getRecentUploads(limit: number = 10): Promise<RecentUploadItem[]> {
   const response = await fetch(`${API_URL}/api/dashboard/recent-uploads?limit=${limit}`, {
     method: "GET",
     cache: "no-store",
   });
  if (!response.ok) {
    const error = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(error?.detail || `Could not load recent uploads (HTTP ${response.status}).`);
   }
   const data: RecentUploadItem[] = await response.json();
   return data;
 }
 
