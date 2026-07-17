export default function ChatDemo() {
  return (
    <section className="mx-auto max-w-7xl px-8 py-28">

      <div className="grid gap-16 lg:grid-cols-2">

        <div>

          <span className="rounded-full bg-cyan-500/10 px-5 py-2 text-cyan-300">

            AI Assistant

          </span>

          <h2 className="mt-6 text-5xl font-black">

            Chat with Your Entire
            Knowledge Base
          </h2>

          <p className="mt-8 text-lg leading-9 text-slate-400">

            Ask engineering questions exactly like talking to
            an experienced site engineer.

          </p>

        </div>

        <div className="rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-2xl p-8 shadow-[0_0_60px_rgba(34,211,238,.12)]">

          <div className="space-y-8">

            <div className="ml-auto max-w-sm rounded-2xl bg-cyan-500/15 p-5">

              How many expansion joints are required?

            </div>

            <div className="max-w-md rounded-2xl bg-white/5 p-5">

              According to IS 3414 and project drawing C-201,
              expansion joints should be provided every 45 meters.

            </div>

            <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">

              <p className="text-cyan-300">

                Sources

              </p>

              <ul className="mt-3 space-y-2 text-slate-300">

                <li>✔ IS3414.pdf</li>

                <li>✔ Structural_Drawing_C201.pdf</li>

                <li>✔ Project_Specification.docx</li>

              </ul>

            </div>

          </div>

        </div>

      </div>

    </section>
  );
}