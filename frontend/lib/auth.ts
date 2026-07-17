import type { Roles } from '@/types/globals'

export function getUserRole(sessionClaims?: CustomJwtSessionClaims | null): Roles | undefined {
  if (!sessionClaims) {
    return undefined
  }

  return (
    sessionClaims.metadata?.role ??
    sessionClaims.publicMetadata?.role ??
    sessionClaims.unsafeMetadata?.role
  )
}