export default function ChatPreview() {
  return (
    <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-2xl shadow-[0_0_70px_rgba(34,211,238,.15)]">

      <div className="mb-6 flex items-center gap-2">

        <div className="h-3 w-3 rounded-full bg-red-400" />

        <div className="h-3 w-3 rounded-full bg-yellow-400" />

        <div className="h-3 w-3 rounded-full bg-green-400" />

      </div>

      <div className="space-y-6">

        <div className="rounded-xl bg-cyan-500/10 p-4">

          👤 How many fire exits are required for this floor?

        </div>

        <div className="rounded-xl bg-white/5 p-5">

          🤖 According to NBC 2016 Section 4.8,

          buildings over 15m require two independent exits...

        </div>

        <div>

          <p className="mb-3 text-cyan-300">

            Sources

          </p>

          <div className="space-y-2 text-sm text-slate-300">

            <div>✔ NBC2016.pdf</div>

            <div>✔ FireSafety.docx</div>

            <div>✔ Drawing-A102.dwg</div>

          </div>
        </div>

      </div>
    </div>
  );
}