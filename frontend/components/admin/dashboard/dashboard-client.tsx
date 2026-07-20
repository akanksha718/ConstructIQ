"use client";

import { useCallback, useEffect, useState } from "react";
import { Database, FolderTree, HardDrive, Sparkles } from "lucide-react";
import { toast } from "sonner";

import ProcessingQueue from "./processing-queue";
import RecentUploads from "./recent-uploads";
import StatCard from "./stat-card";
import { getProcessingQueue, type ProcessingQueueItem } from "@/services/processing-queue.service";
import { getRecentUploads, type RecentUploadItem } from "@/services/recent-uploads.service";
import { getStats, type KnowledgeStats } from "@/services/stats.service";

function formatNumber(value: number | undefined) {
  return (value ?? 0).toLocaleString("en-US");
}

export default function DashboardClient() {
  const [stats, setStats] = useState<KnowledgeStats | null>(null);
  const [uploads, setUploads] = useState<RecentUploadItem[]>([]);
  const [queue, setQueue] = useState<ProcessingQueueItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadDashboard = useCallback(async (showError = true) => {
    try {
      const [nextStats, nextUploads, nextQueue] = await Promise.all([
        getStats(),
        getRecentUploads(6),
        getProcessingQueue(6),
      ]);
      setStats(nextStats);
      setUploads(nextUploads);
      setQueue(nextQueue);
    } catch (error) {
      if (showError) {
        toast.error(error instanceof Error ? error.message : "Could not load dashboard data.");
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDashboard();
    const interval = window.setInterval(() => void loadDashboard(false), 30_000);
    return () => window.clearInterval(interval);
  }, [loadDashboard]);

  return (
    <>
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Knowledge Assets" value={isLoading ? "…" : formatNumber(stats?.documents_uploaded)} description="Uploaded documents" icon={Database} />
        <StatCard title="Knowledge Entities" value={isLoading ? "…" : formatNumber(stats?.knowledge_entities)} description="Extracted from the corpus" icon={FolderTree} />
        <StatCard title="Equipment Tags" value={isLoading ? "…" : formatNumber(stats?.equipment_tags)} description="Linked equipment records" icon={HardDrive} />
        <StatCard title="Relationships" value={isLoading ? "…" : formatNumber(stats?.relationships_built)} description="Knowledge graph connections" icon={Sparkles} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RecentUploads uploads={uploads} isLoading={isLoading} />
        <ProcessingQueue queue={queue} isLoading={isLoading} />
      </div>
    </>
  );
}
