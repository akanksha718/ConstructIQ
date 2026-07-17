import AuroraBackground from "@/components/landing/AuroraBackground";
import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import TrustedCompanies from "@/components/landing/TrustedCompanies";
import Features from "@/components/landing/Features";
import HowItWorks from "@/components/landing/HowItWorks";
import ChatDemo from "@/components/landing/ChatDemo";
import CTA from "@/components/landing/CTA";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <main className="relative overflow-hidden bg-[#050816] text-white">
      <AuroraBackground />

      <div className="relative z-10">
        <Navbar />
        <Hero />
        <TrustedCompanies />
        <Features />
        <HowItWorks />
        <ChatDemo />
        <CTA />
        <Footer />
      </div>
    </main>
  );
}