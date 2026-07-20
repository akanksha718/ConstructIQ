 import API_URL from "@/lib/api-client";
 
 export interface ProcessingQueueItem {
   id: number;
   filename: string;
   uploaded_by: string;
   started_at: string; // ISO date string
   processing_status: string;
 }
 
 export async function getProcessingQueue(limit: number = 20): Promise<ProcessingQueueItem[]> {
   const response = await fetch(`${API_URL}/api/dashboard/processing-queue?limit=${limit}`, {
     method: "GET",
     cache: "no-store",
   });
  if (!response.ok) {
    const error = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(error?.detail || `Could not load processing queue (HTTP ${response.status}).`);
   }
   const data: ProcessingQueueItem[] = await response.json();
   return data;
 }
 
