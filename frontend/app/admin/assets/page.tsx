"use client";

import { useEffect, useMemo, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { FileText, FolderOpen, LoaderCircle, Search, SlidersHorizontal, ExternalLink, Database } from "lucide-react";
import { toast } from "sonner";

import { getDocumentAccessUrl, getDocuments } from "@/services/document-service";
import type { DocumentAsset } from "@/types/documents";

function formatSize(bytes: number) {
  if (!bytes) return "—";
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(index ? 1 : 0)} ${units[index]}`;
}

function statusClass(status: string) {
  if (status === "READY") return "border-emerald-400/20 bg-emerald-400/10 text-emerald-200";
  if (status === "FAILED") return "border-rose-400/20 bg-rose-400/10 text-rose-200";
  return "border-amber-400/20 bg-amber-400/10 text-amber-100";
}

export default function AssetsPage() {
  const { getToken } = useAuth();
  const [assets, setAssets] = useState<DocumentAsset[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("ALL");
  const [type, setType] = useState("ALL");

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const token = await getToken();
        const documents = await getDocuments(token);
        if (active) setAssets(documents);
      } catch (error) {
        if (active) toast.error(error instanceof Error ? error.message : "Could not load assets.");
      } finally {
        if (active) setIsLoading(false);
      }
    }
    void load();
    return () => { active = false; };
  }, [getToken]);

  const types = useMemo(() => [...new Set(assets.map((asset) => asset.file_type))].sort(), [assets]);
  const filteredAssets = useMemo(() => assets.filter((asset) => {
    const matchesSearch = asset.filename.toLowerCase().includes(search.trim().toLowerCase());
    const matchesStatus = status === "ALL" || (status === "IN_PROGRESS"
      ? !["READY", "FAILED"].includes(asset.processing_status)
      : asset.processing_status === status);
    return matchesSearch && matchesStatus && (type === "ALL" || asset.file_type === type);
  }), [assets, search, status, type]);

  async function openDocument(asset: DocumentAsset) {
    const documentWindow = window.open("", "_blank");
    if (!documentWindow) {
      toast.error("Your browser blocked the document window. Please allow pop-ups and try again.");
      return;
    }
    try {
      documentWindow.location.href = await getDocumentAccessUrl(asset.id);
    } catch (error) {
      documentWindow.close();
      toast.error(error instanceof Error ? error.message : "Could not open this document.");
    }
  }

  return (
    <div className="mx-auto max-w-7xl space-y-8 p-5 sm:p-8">
      <header className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-400/10 px-3 py-1 text-xs font-medium text-cyan-100"><Database className="size-3.5" /> Knowledge library</div>
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">All uploaded assets</h1>
          <p className="mt-2 text-slate-400">Browse, filter, and open every document in the knowledge base.</p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300"><span className="font-semibold text-white">{assets.length}</span> documents indexed</div>
      </header>

      <section className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-xl sm:p-5">
        <div className="grid gap-3 lg:grid-cols-[1fr_auto_auto]">
          <label className="flex items-center gap-3 rounded-xl border border-white/10 bg-slate-950/40 px-4 py-3 text-slate-400"><Search className="size-4" /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search document names…" className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500" /></label>
          <label className="flex items-center gap-2 rounded-xl border border-white/10 bg-slate-950/40 px-3 text-sm text-slate-300"><SlidersHorizontal className="size-4" /><select value={status} onChange={(event) => setStatus(event.target.value)} className="bg-transparent py-3 outline-none"><option value="ALL">All statuses</option><option value="READY">Ready</option><option value="IN_PROGRESS">In progress</option><option value="FAILED">Failed</option></select></label>
          <select value={type} onChange={(event) => setType(event.target.value)} className="rounded-xl border border-white/10 bg-slate-950/40 px-3 py-3 text-sm text-slate-300 outline-none"><option value="ALL">All file types</option>{types.map((item) => <option key={item} value={item}>{item}</option>)}</select>
        </div>
      </section>

      <section className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl">
        <div className="grid grid-cols-[minmax(0,1fr)_auto] gap-4 border-b border-white/10 px-5 py-4 text-xs font-medium uppercase tracking-wider text-slate-500 sm:grid-cols-[minmax(0,1fr)_100px_120px_120px_auto]"><span>Document</span><span className="hidden sm:block">Type</span><span className="hidden sm:block">Status</span><span className="hidden sm:block">Uploaded</span><span /></div>
        {isLoading ? <div className="flex items-center justify-center gap-3 px-5 py-16 text-slate-400"><LoaderCircle className="size-5 animate-spin" /> Loading assets…</div> : null}
        {!isLoading && filteredAssets.length === 0 ? <div className="px-5 py-16 text-center text-slate-400"><FolderOpen className="mx-auto mb-3 size-8 text-slate-500" />No documents match these filters.</div> : null}
        {filteredAssets.map((asset) => <div key={asset.id} className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 border-b border-white/5 px-5 py-4 last:border-0 sm:grid-cols-[minmax(0,1fr)_100px_120px_120px_auto]">
          <div className="flex min-w-0 items-center gap-3"><div className="flex size-10 shrink-0 items-center justify-center rounded-xl border border-cyan-300/15 bg-cyan-400/10 text-cyan-200"><FileText className="size-5" /></div><div className="min-w-0"><p className="truncate font-medium text-white">{asset.filename}</p><p className="mt-0.5 text-xs text-slate-500">{formatSize(asset.file_size)} · {asset.uploaded_by || "Unknown uploader"}</p></div></div>
          <span className="hidden text-sm text-slate-400 sm:block">{asset.file_type}</span><span className={`hidden w-fit rounded-full border px-2.5 py-1 text-xs sm:block ${statusClass(asset.processing_status)}`}>{asset.processing_status}</span><span className="hidden text-sm text-slate-400 sm:block">{new Date(asset.created_at).toLocaleDateString()}</span>
          <button type="button" onClick={() => void openDocument(asset)} className="inline-flex items-center gap-2 rounded-xl border border-cyan-300/20 bg-cyan-400/10 px-3 py-2 text-xs font-medium text-cyan-100 transition hover:bg-cyan-400/20"><ExternalLink className="size-3.5" /> Open</button>
        </div>)}
      </section>
      {!isLoading ? <p className="text-center text-sm text-slate-500">Showing {filteredAssets.length} of {assets.length} documents</p> : null}
    </div>
  );
}
