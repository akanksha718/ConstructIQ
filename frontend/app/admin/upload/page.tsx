"use client";

import {
  UploadCloud,
  FileText,
  FileSpreadsheet,
  Mail,
  BrainCircuit,
  Database,
  Network,
  ShieldCheck,
  CheckCircle2,
  Clock3,
} from "lucide-react";
import { useRef } from "react";
import { useState } from "react";
import { X } from "lucide-react";
import { uploadDocuments } from "@/services/upload.service";
import { toast } from "sonner";
import { useAuth } from "@clerk/nextjs";


export default function UploadPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const { getToken } = useAuth();

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const selectedFiles = Array.from(e.target.files);

    setFiles((prev) => {
      const existing = new Set(
        prev.map((f) => `${f.name}-${f.size}-${f.lastModified}`)
      );

      const newFiles = selectedFiles.filter(
        (f) => !existing.has(`${f.name}-${f.size}-${f.lastModified}`)
      );

      return [...prev, ...newFiles];
    });

    // Allows selecting the same file again later
    e.target.value = "";
  };


  const handleSubmit = async () => {
    const token = await getToken();
    if (files.length === 0) {
      toast.error("Please select at least one file.");
      return;
    }

    try {
      setIsUploading(true);

      const result = await uploadDocuments(files, token);

      console.log(result);

      toast.success("Documents uploaded successfully!");

      setFiles([]);
    } catch (err) {
      console.error(err);

      toast.error(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setIsUploading(false);
    }
  };
  const documentTypes = [
    {
      icon: FileText,
      title: "Engineering Drawings",
      desc: "P&IDs, CAD PDFs, Schematics",
    },
    {
      icon: FileSpreadsheet,
      title: "Maintenance Records",
      desc: "Work Orders, Inspection Logs",
    },
    {
      icon: ShieldCheck,
      title: "Safety Procedures",
      desc: "SOPs, HSE Manuals",
    },
    {
      icon: Mail,
      title: "Email Archives",
      desc: "Historical Communication",
    },
  ];

  const pipeline = [
    {
      icon: UploadCloud,
      title: "Upload",
    },
    {
      icon: BrainCircuit,
      title: "AI Extraction",
    },
    {
      icon: Network,
      title: "Knowledge Graph",
    },
    {
      icon: Database,
      title: "Vector Database",
    },
  ];

  return (
    <main className="min-h-screen bg-[#020617] text-white relative overflow-hidden">

      <div className="relative mx-auto max-w-7xl px-4 py-10">

        {/* Hero */}

        <div className="mb-12">

          <span className="rounded-full border border-cyan-400/20 bg-cyan-500/10 px-5 py-2 text-sm text-cyan-300">

            Industrial Knowledge Intelligence

          </span>

          <h1 className="mt-6 text-5xl font-bold">

            Upload Industrial Documents

          </h1>

          <p className="mt-5 max-w-3xl text-slate-400 leading-8">

            Build your organization's AI-powered knowledge graph by uploading
            engineering drawings, maintenance reports, SOPs, inspection
            records, OEM manuals, project files and historical documentation.

          </p>

        </div>

        {/* Upload Area */}

        <section className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl p-10">

          <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-cyan-500/30 bg-cyan-500/5 py-20 transition hover:border-cyan-400">

            <UploadCloud className="h-16 w-16 text-cyan-400" />

            <h2 className="mt-6 text-2xl font-semibold">

              Drag & Drop Documents

            </h2>

            <p className="mt-3 text-slate-400">

              Upload PDFs, DOCX, Images, Spreadsheets or ZIP archives

            </p>

            <input
              ref={inputRef}
              type="file"
              multiple
              hidden
              onChange={handleFiles}
              accept=".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg,.txt,.zip"
            />

            <button
              onClick={() => inputRef.current?.click()}
              className="mt-8 rounded-xl bg-cyan-500 px-8 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              Browse Files
            </button>
            {files.length > 0 && (
              <div className="mt-8 w-full max-w-2xl space-y-3">
                {files.map((file, index) => (
                  <div
                    key={`${file.name}-${file.lastModified}`}
                    className="flex items-center justify-between rounded-xl border border-cyan-500/20 bg-slate-900/60 px-4 py-3"
                  >
                    <div className="overflow-hidden">
                      <p className="truncate font-medium text-white">
                        {file.name}
                      </p>

                      <p className="text-sm text-slate-400">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>

                    <button
                      onClick={() => removeFile(index)}
                      className="rounded-full p-2 text-red-400 transition hover:bg-red-500/10 hover:text-red-300"
                    >
                      <X size={18} />
                    </button>
                  </div>
                ))}
                {files.length > 0 && (
                  <div className="mt-6 flex justify-center">
                    <button
                      onClick={handleSubmit}
                      disabled={isUploading}
                      className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-8 py-3 font-semibold text-slate-950 transition hover:from-cyan-400 hover:to-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      {isUploading
                        ? "Uploading..."
                        : `Submit ${files.length} File${files.length > 1 ? "s" : ""}`}
                    </button>
                  </div>
                )}
              </div>
            )}

          </div>

        </section>

        {/* Stats */}

        <div className="mt-10 grid gap-6 md:grid-cols-4">

          {[
            ["Documents Uploaded", "2,481"],
            ["Knowledge Entities", "58,942"],
            ["Equipment Tags", "8,320"],
            ["Relationships Built", "174K"],
          ].map(([title, value]) => (

            <div
              key={title}
              className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6"
            >
              <p className="text-sm text-slate-400">{title}</p>

              <h2 className="mt-2 text-3xl font-bold text-cyan-300">

                {value}

              </h2>
            </div>
          ))}
        </div>

        {/* Supported Documents */}

        <section className="mt-16">

          <h2 className="text-2xl font-semibold">

            Supported Industrial Documents

          </h2>

          <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-4">

            {documentTypes.map((doc) => (
              <div
                key={doc.title}
                className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 transition hover:border-cyan-400"
              >
                <doc.icon className="h-10 w-10 text-cyan-400" />

                <h3 className="mt-6 text-lg font-semibold">

                  {doc.title}

                </h3>

                <p className="mt-3 text-sm text-slate-400">

                  {doc.desc}

                </p>

              </div>
            ))}
          </div>

        </section>

        {/* AI Processing Pipeline */}

        <section className="mt-20">

          <h2 className="text-2xl font-semibold">

            AI Processing Pipeline

          </h2>

          <div className="mt-10 grid gap-6 md:grid-cols-4">

            {pipeline.map((step) => (
              <div
                key={step.title}
                className="relative rounded-2xl border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-xl p-8"
              >
                <step.icon className="h-12 w-12 text-cyan-400" />

                <h3 className="mt-5 text-lg font-semibold">

                  {step.title}

                </h3>

              </div>
            ))}
          </div>

        </section>

        {/* AI Features */}

        <section className="mt-20 grid gap-8 lg:grid-cols-2">

          <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-8">

            <h2 className="text-xl font-semibold">

              AI Extraction

            </h2>

            <div className="mt-8 space-y-5">

              {[
                "OCR & Handwriting Recognition",
                "Equipment Tag Detection",
                "Process Parameter Extraction",
                "Regulatory Reference Mapping",
                "Knowledge Graph Generation",
                "Automatic Entity Linking",
              ].map((item) => (
                <div key={item} className="flex items-center gap-3">

                  <CheckCircle2 className="h-5 w-5 text-cyan-400" />

                  <span>{item}</span>

                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-8">

            <h2 className="text-xl font-semibold">

              Recent Processing

            </h2>

            <div className="mt-8 space-y-6">

              <div className="flex justify-between">

                <span>Pump_Inspection_Report.pdf</span>

                <Clock3 className="text-cyan-400" />

              </div>

              <div className="flex justify-between">

                <span>P&ID_Unit_04.pdf</span>

                <CheckCircle2 className="text-green-400" />

              </div>

              <div className="flex justify-between">

                <span>Maintenance_Log_March.xlsx</span>

                <CheckCircle2 className="text-green-400" />

              </div>

            </div>

          </div>

        </section>

      </div>

    </main>
  );
}