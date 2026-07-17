import SectionHeader from "./section-header";

const queue = [
  {
    file: "Inspection Report",
    progress: 70,
  },
  {
    file: "Maintenance Manual",
    progress: 35,
  },
];

export default function ProcessingQueue() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <SectionHeader
        title="Processing Queue"
        description="OCR & Embeddings"
      />

      <div className="space-y-6">
        {queue.map((job) => (
          <div key={job.file}>
            <div className="mb-2 flex justify-between text-sm">
              <span className="text-white">
                {job.file}
              </span>

              <span className="text-cyan-300">
                {job.progress}%
              </span>
            </div>

            <div className="h-2 rounded-full bg-slate-800">
              <div
                style={{
                  width: `${job.progress}%`,
                }}
                className="h-2 rounded-full bg-cyan-400"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}