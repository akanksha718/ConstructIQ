import { auth } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'
import { getUserRole } from '@/lib/auth'

export default async function PostSignInPage() {
  const { userId, sessionClaims } = await auth()

  if (!userId) {
    redirect('/sign-in')
  }

  if (getUserRole(sessionClaims) === 'admin') {
    redirect('/admin/dashboard')
  }

  redirect('/chat')
}