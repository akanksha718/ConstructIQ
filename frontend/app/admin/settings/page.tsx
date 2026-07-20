import React from 'react'
import { auth } from "@clerk/nextjs/server";
import { redirect } from 'next/navigation'
import { getUserRole } from '@/lib/auth'
export default async function page(){
      const { userId, sessionClaims } = await auth()
    
      if (!userId) {
        redirect('/sign-in')
      }
    
      if (getUserRole(sessionClaims) !== 'admin') {
        redirect('/chat')
      }
  return (
    <div>
      comming soon
    </div>
  )
}