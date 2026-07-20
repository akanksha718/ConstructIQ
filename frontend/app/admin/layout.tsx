import type { ReactNode } from "react";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

import Sidebar from "@/components/admin/layout/sidebar";
import Topbar from "@/components/admin/layout/topbar";
import { getUserRole } from "@/lib/auth";

interface ConsoleLayoutProps {
  children: ReactNode;
}

export default async function ConsoleLayout({
  children,
}: ConsoleLayoutProps) {
  const { userId, sessionClaims } = await auth();
  if (!userId) {
    redirect("/sign-in?redirect_url=/admin/dashboard");
  }
  if (getUserRole(sessionClaims) !== "admin") {
    redirect("/chat");
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-white">
      {/* Background Glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-40 -top-40 h-[450px] w-[450px] rounded-full bg-cyan-500/10 blur-[150px]" />

        <div className="absolute bottom-0 right-0 h-[500px] w-[500px] rounded-full bg-blue-500/10 blur-[180px]" />
      </div>

      <Sidebar />

      <div className="relative flex flex-1 flex-col">
        <Topbar />

        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
