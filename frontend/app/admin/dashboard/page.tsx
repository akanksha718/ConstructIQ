import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import { getUserRole } from '@/lib/auth'
import {
  Database,
  FolderTree,
  HardDrive,
  Sparkles,
} from "lucide-react";
import StatCard from "@/components/admin/dashboard/stat-card";
import RecentUploads from "@/components/admin/dashboard/recent-uploads";
import ProcessingQueue from "@/components/admin/dashboard/processing-queue";

export default async function AdminDashboard() {
  const { userId, sessionClaims } = await auth()

  if (!userId) {
    redirect('/sign-in')
  }

  if (getUserRole(sessionClaims) !== 'admin') {
    redirect('/chat')
  }

  return (

    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold">
          Welcome Back 👋
        </h1>

        <p className="mt-2 text-slate-400">
          Manage your industrial knowledge platform.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Knowledge Assets"
          value="1,284"
          description="+24 uploaded today"
          icon={Database}
        />

        <StatCard
          title="Collections"
          value="18"
          description="Across departments"
          icon={FolderTree}
        />

        <StatCard
          title="Storage"
          value="3.2 GB"
          description="64% utilized"
          icon={HardDrive}
        />

        <StatCard
          title="AI Ready"
          value="96%"
          description="Embeddings complete"
          icon={Sparkles}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RecentUploads />
        <ProcessingQueue />
      </div>
    </div>

  );
}

function DashboardCard({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string;
  subtitle: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <p className="text-sm text-slate-400">
        {title}
      </p>

      <h2 className="mt-3 text-4xl font-bold">
        {value}
      </h2>

      <p className="mt-3 text-sm text-cyan-300">
        {subtitle}
      </p>
    </div>
  );
}