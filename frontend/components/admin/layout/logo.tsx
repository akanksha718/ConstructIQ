import Link from "next/link";
import Image from "next/image";
export default function Logo() {
  return (
    <Link
      href="/admin/dashboard"
      className="flex items-center gap-2"
    >
      <div
        className="
          flex h-10 w-10 items-center justify-center
          rounded-xl
          border border-cyan-400/20
          bg-cyan-500/10
          text-cyan-300
        "
      >
        <Image
          src="/favicon.ico"
          alt="Logo"
          width={24}
          height={24}
          className="h-6 w-6"
        />
      </div>

      <div>
        <h2 className="text-lg font-bold tracking-tight text-white">
          ConstructIQ AI
        </h2>

        <p className="text-xs text-slate-400">
          Industrial Knowledge Platform
        </p>
      </div>
    </Link>
  );
}