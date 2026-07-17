import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner"
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

export const metadata: Metadata = {
  title: "ConstructIQ-AI",
  description: "Industrial Knowledge Intelligence platform",
  openGraph: {
    title: "ConstructIQ-AI",
    description: "Industrial Knowledge Intelligence platform",
    images: "favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn("h-full antialiased", "font-sans", geist.variable)}
    >
      <body className="min-h-full flex flex-col">
        <ClerkProvider
          signInForceRedirectUrl="/post-sign-in"
          signUpForceRedirectUrl="/post-sign-in"
        >
          {children}
          <Toaster />
        </ClerkProvider>
      </body>
    </html>
  );
}
