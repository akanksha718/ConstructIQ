import { HardDrive } from "lucide-react";

export default function StorageCard() {
  const usedStorage = 3.2;
  const totalStorage = 5;

  const percentage = (usedStorage / totalStorage) * 100;

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur-xl">
      <div className="mb-4 flex items-center gap-2">
        <HardDrive className="h-5 w-5 text-cyan-300" />
        <h3 className="font-semibold text-white">
          Storage
        </h3>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-cyan-400 transition-all"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

      <div className="mt-3 flex items-center justify-between text-xs">
        <span className="text-slate-400">
          {usedStorage} GB / {totalStorage} GB
        </span>

        <span className="font-medium text-cyan-300">
          {Math.round(percentage)}%
        </span>
      </div>
    </div>
  );
}