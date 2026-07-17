import SectionHeader from "./section-header";

const uploads = [
  {
    name: "Pump Manual.pdf",
    type: "PDF",
    status: "Ready",
  },
  {
    name: "Boiler SOP.pdf",
    type: "PDF",
    status: "Processing",
  },
  {
    name: "P&ID Unit-4.pdf",
    type: "Drawing",
    status: "Ready",
  },
];

export default function RecentUploads() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <SectionHeader
        title="Recent Uploads"
        description="Latest knowledge assets"
      />

      <div className="space-y-4">
        {uploads.map((item) => (
          <div
            key={item.name}
            className="flex items-center justify-between rounded-xl border border-white/5 bg-white/5 p-4"
          >
            <div>
              <h4 className="font-medium text-white">
                {item.name}
              </h4>

              <p className="text-sm text-slate-400">
                {item.type}
              </p>
            </div>

            <span className="rounded-full bg-cyan-500/10 px-3 py-1 text-xs text-cyan-300">
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}