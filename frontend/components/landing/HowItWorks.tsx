import {
  Upload,
  Database,
  Brain,
  FileSearch,
  FileText,
} from "lucide-react";

const steps = [
  {
    icon: Upload,
    title: "Upload Documents",
    description:
      "PDFs, Drawings, BOQs, SOPs, Excel sheets, Manuals and CAD files.",
  },
  {
    icon: Database,
    title: "AI Indexing",
    description:
      "ConstructIQ builds a searchable knowledge base using embeddings.",
  },
  {
    icon: Brain,
    title: "Ask Questions",
    description:
      "Chat naturally with your engineering knowledge using AI.",
  },
  {
    icon: FileSearch,
    title: "Verified Sources",
    description:
      "Every answer links back to the original document section.",
  },
  {
    icon: FileText,
    title: "Generate Reports",
    description:
      "Export summaries, technical reports and safety documentation.",
  },
];

export default function HowItWorks() {
  return (
    <section className="mx-auto max-w-7xl px-8 py-32">

      <div className="text-center">

        <span className="rounded-full bg-cyan-500/10 px-5 py-2 text-cyan-300">

          Workflow

        </span>

        <h2 className="mt-6 text-5xl font-black">

          How ConstructIQ Works

        </h2>

      </div>

      <div className="mt-24 relative">

        <div className="absolute left-7 top-5 h-full w-[2px] bg-gradient-to-b from-cyan-500 to-transparent" />

        <div className="space-y-16">

          {steps.map((step, index) => (
            <div
              key={index}
              className="relative flex gap-8"
            >
              <div className="z-10 flex h-14 w-14 items-center justify-center rounded-full bg-cyan-500 text-black">

                <step.icon size={26} />

              </div>

              <div>

                <h3 className="text-2xl font-bold">

                  {step.title}

                </h3>

                <p className="mt-3 max-w-2xl text-slate-400 leading-8">

                  {step.description}

                </p>

              </div>

            </div>
          ))}

        </div>

      </div>

    </section>
  );
}