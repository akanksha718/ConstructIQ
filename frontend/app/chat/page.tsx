import IndustrialChat from "@/components/chat/industrial-chat";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function ChatPage() {
  const { userId } = await auth();
  if (!userId) {
    redirect("/sign-in?redirect_url=/chat");
  }

  return <IndustrialChat />;
}
