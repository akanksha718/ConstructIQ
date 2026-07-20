import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import { getUserRole } from '@/lib/auth'
import DashboardClient from "@/components/admin/dashboard/dashboard-client";

export default async function AdminDashboard() {
  const { userId, sessionClaims } = await auth()

  if (!userId) {
    redirect('/sign-in')
  }

  if (getUserRole(sessionClaims) !== 'admin') {
    redirect('/chat')
  }

  return (

    <div className="space-y-8 p-2">
      <div>
        <h1 className="text-4xl font-bold">
          Welcome Back 👋
        </h1>

        <p className="mt-2 text-slate-400">
          Manage your industrial knowledge platform.
        </p>
      </div>

      <DashboardClient />
    </div>

  );
}
