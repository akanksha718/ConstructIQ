import Link from "next/link";

export default function CTA() {
  return (
    <section className="mx-auto max-w-7xl px-8 py-32">

      <div className="overflow-hidden rounded-[40px] border border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-violet-500/10 p-16 backdrop-blur-3xl">

        <h2 className="text-center text-5xl font-black">

          Ready to Build Smarter?

        </h2>

        <p className="mx-auto mt-8 max-w-3xl text-center text-lg leading-9 text-slate-300">

          Upload your engineering documents,
          connect your company knowledge,
          and let ConstructIQ AI answer every question instantly.

        </p>

        <div className="mt-12 flex justify-center gap-6">

          <button className="rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-500 px-8 py-4 font-semibold shadow-[0_0_40px_rgba(34,211,238,.35)] hover:scale-105 transition">

            <Link href="/chat">
              Start Chatting
            </Link>

          </button>

        </div>

      </div>

    </section>
  );
}