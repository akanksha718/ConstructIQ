import { dark } from "@clerk/themes";
import { SignIn } from '@clerk/nextjs'

export default function Page() {
  return <SignIn appearance={dark} />
}