import {
  Brain,
  Database,
  Search,
  Languages,
  FileText,
  ShieldCheck,
} from "lucide-react";

import FeatureCard from "./FeatureCard";

export default function Features() {
  return (
    <section className="mx-auto max-w-7xl px-8 py-32">

      <div className="mb-20 text-center">

        <span className="rounded-full bg-cyan-500/10 px-5 py-2 text-cyan-300">

          Platform Features

        </span>

        <h2 className="mt-6 text-5xl font-black">

          Built for Modern

          <span className="text-cyan-400">

            {" "}Engineering Teams

          </span>

        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">

          Search every engineering document,
          drawing, SOP, specification,
          safety manual and project report
          with enterprise-grade AI.

        </p>

      </div>

      <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-3">

        <FeatureCard
          icon={Brain}
          title="AI Chat"
          description="Ask natural language questions and receive accurate answers from your project knowledge base."
        />

        <FeatureCard
          icon={Database}
          title="Knowledge Base"
          description="Index thousands of PDFs, DOCX, Excel sheets, CAD drawings and SOPs."
        />

        <FeatureCard
          icon={Search}
          title="Semantic Search"
          description="Search beyond keywords using vector embeddings and Retrieval-Augmented Generation."
        />

        <FeatureCard
          icon={Languages}
          title="Multi-language"
          description="Understand Hindi, English and many regional languages for field engineers."
        />

        <FeatureCard
          icon={FileText}
          title="Report Generator"
          description="Automatically create reports, summaries and technical documentation."
        />

        <FeatureCard
          icon={ShieldCheck}
          title="Secure"
          description="Enterprise authentication, encrypted storage and role-based permissions."
        />

      </div>

    </section>
  );
}