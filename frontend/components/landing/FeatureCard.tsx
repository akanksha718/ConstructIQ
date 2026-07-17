
import { LucideIcon } from "lucide-react";

interface Props {
  icon: LucideIcon;
  title: string;
  description: string;
}

export default function FeatureCard({
  icon: Icon,
  title,
  description,
}: Props) {
  return (
    <div
      className="
      group
      relative
      overflow-hidden
      rounded-3xl
      border
      border-white/10
      bg-white/5
      p-7
      backdrop-blur-2xl
      transition-all
      duration-300
      hover:-translate-y-3
      hover:border-cyan-400/30
      hover:shadow-[0_0_50px_rgba(34,211,238,.2)]
      "
    >
      {/* Glow */}

      <div className="absolute -right-20 -top-20 h-40 w-40 rounded-full bg-cyan-500/10 blur-3xl opacity-0 transition group-hover:opacity-100" />

      <div className="mb-6 inline-flex rounded-2xl bg-cyan-500/10 p-4">

        <Icon className="h-8 w-8 text-cyan-400" />

      </div>

      <h3 className="mb-4 text-2xl font-bold">

        {title}

      </h3>

      <p className="leading-8 text-slate-400">

        {description}

      </p>
    </div>
  );
}