import { ArrowUpRight, type LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  description: string;
  icon: LucideIcon;
}

export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: StatCardProps) {
  return (
    <div className="group rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-cyan-400/20 hover:bg-white/10">
      <div className="flex items-center justify-between">
        <div className="rounded-xl bg-cyan-500/10 p-3">
          <Icon className="h-6 w-6 text-cyan-300" />
        </div>

        <ArrowUpRight className="h-5 w-5 text-slate-500 transition group-hover:text-cyan-300" />
      </div>

      <h3 className="mt-6 text-sm text-slate-400">
        {title}
      </h3>

      <p className="mt-2 text-4xl font-bold text-white">
        {value}
      </p>

      <p className="mt-2 text-sm text-cyan-300">
        {description}
      </p>
    </div>
  );
}