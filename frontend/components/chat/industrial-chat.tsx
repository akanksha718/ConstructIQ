"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowUp,
  Bot,
  CircleAlert,
  FileText,
  Gauge,
  Link2,
  LoaderCircle,
  ShieldCheck,
  Sparkles,
  User,
  Wrench,
} from "lucide-react";

import { askIndustrialCopilot, type ChatResponse } from "@/services/chat.service";
import { cn } from "@/lib/utils";

const SUGGESTED_PROMPTS = [
  "Why did pump P-204 trip repeatedly last month?",
  "Summarize the latest inspection findings for boiler B-12 with sources.",
  "Which procedures and reports mention PSV-17 and what risk pattern do they show?",
  "List compliance gaps linked to OISD evidence for the compressor house.",
];

type Message = {
  id: string;
  role: "assistant" | "user";
  content: string;
  response?: ChatResponse;
  pending?: boolean;
  error?: boolean;
};

const INITIAL_MESSAGE: Message = {
  id: "welcome",
  role: "assistant",
  content:
    "Ask about equipment history, maintenance RCA, compliance evidence, or operating procedures. I will answer from the uploaded industrial knowledge base and attach source citations for every grounded reply.",
};

function getAgentLabel(agent: string | null | undefined) {
  switch (agent) {
    case "maintenance":
      return "Maintenance Agent";
    case "compliance":
      return "Compliance Agent";
    case "lessons":
      return "Lessons Agent";
    default:
      return "Knowledge Copilot";
  }
}

function getConfidenceTone(confidence: number) {
  if (confidence >= 0.8) {
    return {
      label: "High confidence",
      barClass: "from-emerald-400 via-cyan-400 to-sky-500",
      textClass: "text-emerald-200",
    };
  }

  if (confidence >= 0.5) {
    return {
      label: "Medium confidence",
      barClass: "from-amber-300 via-cyan-400 to-sky-500",
      textClass: "text-amber-100",
    };
  }

  return {
    label: "Low confidence",
    barClass: "from-rose-300 via-fuchsia-400 to-cyan-400",
    textClass: "text-rose-100",
  };
}

function AnswerText({ content }: { content: string }) {
  const paragraphs = content
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  return (
    <div className="space-y-3 text-sm leading-7 text-slate-100 sm:text-[15px]">
      {paragraphs.length ? (
        paragraphs.map((paragraph, index) => (
          <p key={`${index}-${paragraph.slice(0, 24)}`}>{paragraph}</p>
        ))
      ) : (
        <p>{content}</p>
      )}
    </div>
  );
}

function CitationCard({ response }: { response: ChatResponse }) {
  const tone = getConfidenceTone(response.confidence);

  return (
    <div className="space-y-4 rounded-[28px] border border-cyan-400/20 bg-slate-950/45 p-4 shadow-[0_0_40px_rgba(34,211,238,0.08)] backdrop-blur-xl">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-sm text-cyan-200">
          <ShieldCheck className="size-4" />
          <span>{getAgentLabel(response.agent)}</span>
        </div>

        <div className={cn("text-xs font-medium", tone.textClass)}>
          {tone.label}
        </div>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-white/10">
        <div
          className={cn("h-full rounded-full bg-gradient-to-r", tone.barClass)}
          style={{ width: `${Math.max(response.confidence * 100, 6)}%` }}
        />
      </div>

      {response.related_equipment.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {response.related_equipment.map((equipment) => (
            <span
              key={equipment}
              className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-100"
            >
              {equipment}
            </span>
          ))}
        </div>
      ) : null}

      {response.citations.length > 0 ? (
        <div className="space-y-3">
          {response.citations.map((citation) => (
            <div
              key={`${citation.source_index}-${citation.document}-${citation.page ?? "na"}`}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex min-w-0 items-center gap-3">
                  <div className="flex size-8 shrink-0 items-center justify-center rounded-full border border-cyan-300/30 bg-cyan-400/10 text-xs font-semibold text-cyan-100">
                    [{citation.source_index}]
                  </div>
                  <div className="min-w-0">
                    <div className="truncate text-sm font-semibold text-white">
                      {citation.document}
                    </div>
                    <div className="text-xs text-slate-400">
                      {[
                        citation.page ? `Page ${citation.page}` : null,
                        citation.heading,
                        citation.section,
                      ]
                        .filter(Boolean)
                        .join(" • ") || "Source excerpt"}
                    </div>
                  </div>
                </div>

                {citation.file_url ? (
                  <a
                    href={citation.file_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-400/10 px-3 py-1.5 text-xs text-cyan-100 transition hover:border-cyan-200/40 hover:bg-cyan-400/15"
                  >
                    <Link2 className="size-3.5" />
                    Open document
                  </a>
                ) : null}
              </div>

              {citation.excerpt ? (
                <p className="mt-3 text-sm leading-6 text-slate-300">
                  {citation.excerpt}
                </p>
              ) : null}
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-amber-300/15 bg-amber-300/8 p-4 text-sm text-amber-100">
          No supporting citations were returned for this reply.
        </div>
      )}
    </div>
  );
}

export default function IndustrialChat() {
  const [messages, setMessages] = useState<Message[]>([INITIAL_MESSAGE]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollerRef = useRef<HTMLDivElement>(null);
  const messageCounterRef = useRef(0);

  useEffect(() => {
    const node = scrollerRef.current;
    if (!node) {
      return;
    }

    node.scrollTo({
      top: node.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const canSubmit = input.trim().length > 0 && !isLoading;

  const quickStats = useMemo(
    () => [
      {
        icon: FileText,
        label: "Corpus aware",
        value: "Drawings, SOPs, work orders, reports",
      },
      {
        icon: Wrench,
        label: "Ops ready",
        value: "Maintenance, RCA, quality, compliance",
      },
      {
        icon: Gauge,
        label: "Grounded output",
        value: "Confidence and traceable citations",
      },
    ],
    [],
  );

  async function submitQuestion(rawQuestion?: string) {
    const question = (rawQuestion ?? input).trim();
    if (!question || isLoading) {
      return;
    }

    messageCounterRef.current += 1;
    const baseId = messageCounterRef.current;

    const userMessage: Message = {
      id: `${baseId}-user`,
      role: "user",
      content: question,
    };

    const pendingMessage: Message = {
      id: `${baseId}-assistant`,
      role: "assistant",
      content: "Scanning the knowledge graph, retrieval index, and document evidence...",
      pending: true,
    };

    setMessages((current) => [...current, userMessage, pendingMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await askIndustrialCopilot(question);

      setMessages((current) =>
        current.map((message) =>
          message.id === pendingMessage.id
            ? {
                ...message,
                content: response.answer,
                response,
                pending: false,
              }
            : message,
        ),
      );
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "The assistant could not process this request.";

      setMessages((current) =>
        current.map((entry) =>
          entry.id === pendingMessage.id
            ? {
                ...entry,
                content: message,
                pending: false,
                error: true,
              }
            : entry,
        ),
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#050816] text-white">
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.16),transparent_28%),radial-gradient(circle_at_top_right,rgba(168,85,247,0.14),transparent_22%),radial-gradient(circle_at_bottom,rgba(14,165,233,0.12),transparent_28%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] opacity-20" />
        <div className="absolute left-1/4 top-24 size-60 rounded-full bg-cyan-400/10 blur-3xl" />
        <div className="absolute right-0 top-0 size-80 rounded-full bg-fuchsia-500/10 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <div className="grid flex-1 gap-6 lg:grid-cols-[1.05fr_1.35fr]">
          <section className="flex flex-col justify-between rounded-[32px] border border-white/10 bg-white/6 p-6 shadow-[0_0_80px_rgba(34,211,238,0.08)] backdrop-blur-2xl sm:p-8">
            <div className="space-y-6">
              <div className="inline-flex w-fit items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-100">
                <Sparkles className="size-4" />
                Industrial Knowledge Intelligence
              </div>

              <div className="space-y-4">
                <h1 className="max-w-xl text-4xl font-semibold tracking-tight sm:text-5xl">
                  Neon-glass copilot for industrial operations, maintenance, and compliance.
                </h1>
                <p className="max-w-2xl text-base leading-8 text-slate-300 sm:text-lg">
                  Query engineering drawings, maintenance history, inspection records,
                  safety procedures, and regulatory evidence from one conversational
                  workspace built for both control-room teams and field technicians.
                </p>
              </div>

              <div className="grid gap-3">
                {quickStats.map(({ icon: Icon, label, value }) => (
                  <div
                    key={label}
                    className="rounded-2xl border border-white/10 bg-slate-950/35 p-4"
                  >
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 flex size-10 items-center justify-center rounded-2xl bg-white/8 text-cyan-200">
                        <Icon className="size-5" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-slate-100">{label}</p>
                        <p className="mt-1 text-sm leading-6 text-slate-400">{value}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-8 rounded-[28px] border border-fuchsia-400/15 bg-gradient-to-br from-white/8 to-white/4 p-5">
              <div className="flex items-center gap-3 text-sm text-fuchsia-100">
                <CircleAlert className="size-4" />
                Response policy
              </div>
              <p className="mt-3 text-sm leading-7 text-slate-300">
                Answers are grounded in retrieved documents only. Each reply surfaces
                confidence, linked evidence, and equipment references so teams can act
                without losing traceability.
              </p>
            </div>
          </section>

          <section className="flex min-h-[75vh] flex-col overflow-hidden rounded-[32px] border border-white/10 bg-white/7 shadow-[0_0_90px_rgba(56,189,248,0.08)] backdrop-blur-2xl">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 px-5 py-4 sm:px-6">
              <div>
                <div className="flex items-center gap-3">
                  <div className="flex size-10 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-400/10">
                    <Bot className="size-5 text-cyan-100" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-white">Industrial Copilot</h2>
                    <p className="text-sm text-slate-400">
                      Query live knowledge with grounded citations
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 rounded-full border border-emerald-300/15 bg-emerald-400/10 px-3 py-1.5 text-xs text-emerald-100">
                <span className="size-2 rounded-full bg-emerald-300 shadow-[0_0_16px_rgba(110,231,183,0.9)]" />
                Backend connected
              </div>
            </div>

            <div ref={scrollerRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-5 sm:px-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex",
                    message.role === "user" ? "justify-end" : "justify-start",
                  )}
                >
                  <div
                    className={cn(
                      "max-w-3xl rounded-[28px] border px-4 py-4 shadow-[0_0_40px_rgba(15,23,42,0.22)] sm:px-5",
                      message.role === "user"
                        ? "border-cyan-300/20 bg-cyan-400/15 text-white"
                        : "border-white/10 bg-slate-950/45",
                    )}
                  >
                    <div className="mb-3 flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-slate-400">
                      <span
                        className={cn(
                          "flex size-7 items-center justify-center rounded-full border",
                          message.role === "user"
                            ? "border-cyan-300/20 bg-cyan-400/10 text-cyan-100"
                            : "border-white/10 bg-white/5 text-slate-200",
                        )}
                      >
                        {message.role === "user" ? (
                          <User className="size-3.5" />
                        ) : message.pending ? (
                          <LoaderCircle className="size-3.5 animate-spin" />
                        ) : (
                          <Bot className="size-3.5" />
                        )}
                      </span>
                      {message.role === "user" ? "Operator" : "Copilot"}
                    </div>

                    <AnswerText content={message.content} />

                    {message.response ? (
                      <div className="mt-4">
                        <CitationCard response={message.response} />
                      </div>
                    ) : null}

                    {message.error ? (
                      <div className="mt-4 rounded-2xl border border-rose-300/15 bg-rose-400/10 px-4 py-3 text-sm text-rose-100">
                        The backend returned an error. Check API configuration and retrieval data.
                      </div>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-white/10 bg-slate-950/35 px-4 py-4 sm:px-6">
              <div className="mb-3 flex flex-wrap gap-2">
                {SUGGESTED_PROMPTS.map((prompt) => (
                  <button
                    key={prompt}
                    type="button"
                    onClick={() => void submitQuestion(prompt)}
                    disabled={isLoading}
                    className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-left text-xs text-slate-300 transition hover:border-cyan-300/25 hover:bg-cyan-400/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  void submitQuestion();
                }}
                className="rounded-[28px] border border-white/10 bg-white/6 p-3 shadow-[0_0_30px_rgba(34,211,238,0.08)]"
              >
                <label htmlFor="chat-question" className="sr-only">
                  Ask the industrial copilot
                </label>
                <textarea
                  id="chat-question"
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && !event.shiftKey) {
                      event.preventDefault();
                      if (canSubmit) {
                        void submitQuestion();
                      }
                    }
                  }}
                  rows={3}
                  placeholder="Ask about failures, SOP deviations, compliance evidence, or equipment history..."
                  className="w-full resize-none border-0 bg-transparent px-2 py-2 text-sm leading-7 text-white outline-none placeholder:text-slate-500"
                />

                <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <FileText className="size-4" />
                    Returns grounded replies with citation cards
                  </div>

                  <button
                    type="submit"
                    disabled={!canSubmit}
                    className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-gradient-to-r from-cyan-400/80 to-sky-500/80 px-4 py-2 text-sm font-medium text-slate-950 transition hover:shadow-[0_0_26px_rgba(56,189,248,0.45)] disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isLoading ? (
                      <LoaderCircle className="size-4 animate-spin" />
                    ) : (
                      <ArrowUp className="size-4" />
                    )}
                    Ask Copilot
                  </button>
                </div>
              </form>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
