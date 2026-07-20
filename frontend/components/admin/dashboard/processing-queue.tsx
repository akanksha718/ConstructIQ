import type { ProcessingQueueItem } from "@/services/processing-queue.service";
import SectionHeader from "./section-header";

export default function ProcessingQueue({ queue, isLoading }: { queue: ProcessingQueueItem[]; isLoading: boolean }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <SectionHeader title="Processing Queue" description="Documents currently being processed" />
      <div className="space-y-4">
        {isLoading ? <p className="text-sm text-slate-400">Loading queue…</p> : null}
        {!isLoading && queue.length === 0 ? <p className="text-sm text-slate-400">No documents are currently processing.</p> : null}
        {queue.map((job) => (
          <div key={job.id} className="rounded-xl border border-white/5 bg-white/5 p-4">
            <div className="flex justify-between gap-4 text-sm">
              <span className="truncate text-white">{job.filename}</span>
              <span className="shrink-0 text-cyan-300">{job.processing_status}</span>
            </div>
            <p className="mt-2 text-xs text-slate-400">Started {new Date(job.started_at).toLocaleString()}</p>
            <div className="mt-3 h-2 rounded-full bg-slate-800"><div className="h-2 w-1/2 rounded-full bg-cyan-400" /></div>
          </div>
        ))}
      </div>
    </div>
  );
}
