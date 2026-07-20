export interface RecentDocument {
  id: number;
  filename: string;
  processing_status: string;
  created_at: string;
}

export interface DocumentAsset {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  processing_status: string;
  uploaded_by: string;
  created_at: string;
}
