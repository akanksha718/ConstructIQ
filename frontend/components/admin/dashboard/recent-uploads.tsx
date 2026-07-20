import type { RecentUploadItem } from "@/services/recent-uploads.service";
import SectionHeader from "./section-header";

export default function RecentUploads({ uploads, isLoading }: { uploads: RecentUploadItem[]; isLoading: boolean }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <SectionHeader title="Recent Uploads" description="Latest knowledge assets" />
      <div className="space-y-4">
        {isLoading ? <p className="text-sm text-slate-400">Loading uploads…</p> : null}
        {!isLoading && uploads.length === 0 ? <p className="text-sm text-slate-400">No documents have been uploaded yet.</p> : null}
        {uploads.map((item) => (
          <div key={item.id} className="flex items-center justify-between gap-4 rounded-xl border border-white/5 bg-white/5 p-4">
            <div className="min-w-0">
              <h4 className="truncate font-medium text-white">{item.filename}</h4>
              <p className="text-sm text-slate-400">{item.file_type} · {new Date(item.created_at).toLocaleDateString()}</p>
            </div>
            <span className="shrink-0 rounded-full bg-cyan-500/10 px-3 py-1 text-xs text-cyan-300">{item.processing_status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
