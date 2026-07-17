import ChatPreview from "./ChatPreview";
import Link from "next/link";
export default function Hero() {
    return (
        <section className="relative mx-auto grid max-w-7xl items-center gap-20 px-8 py-20 lg:grid-cols-2">

            <div>
                <span
                    className="
    inline-flex items-center justify-center
    rounded-full
    border border-cyan-400/20
    bg-cyan-400/10
    px-3 py-1.5
    sm:px-4 sm:py-2
    md:px-5
    text-xs sm:text-sm md:text-base
    text-center
    text-cyan-300
    max-w-full
    break-words
  "
                >
                    AI-powered Industrial Knowledge Intelligence
                </span>

                <h1 className="mt-8 text-6xl font-black leading-tight">
                    Search Every
                    <br />
                    Drawing,
                    <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-violet-400 bg-clip-text text-transparent">
                        {" "}Specification
                    </span>
                    <br />
                    & Manual
                </h1>

                <p className="mt-8 max-w-xl text-lg leading-9 text-slate-400">
                    We transform fragmented industrial documents into a living knowledge graph that powers AI copilots, maintenance intelligence, compliance monitoring, and operational decision-making.
                </p>

                <div className="mt-10 flex gap-5">

                    <button className="rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-500 px-8 py-4 text-lg font-semibold shadow-[0_0_35px_rgba(6,182,212,.35)] transition hover:scale-105">

                        <Link href="/chat">
                            Start Chatting
                        </Link>

                    </button>

                </div>

            </div>

            <ChatPreview />

        </section>
    );
}