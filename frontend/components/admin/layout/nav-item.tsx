"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

import type { NavItem as Item } from "@/lib/admin-navigation";

interface Props {
  item: Item;
}

export default function NavItem({ item }: Props) {
  const pathname = usePathname();

  const isActive =
    pathname === item.href ||
    pathname.startsWith(`${item.href}/`);

  const Icon = item.icon;

  return (
    <Link
      href={item.href}
      className={clsx(
        "group flex items-center gap-3 rounded-xl px-4 py-3 transition-all duration-200",
        isActive
          ? "border border-cyan-500/20 bg-cyan-500/10 text-cyan-300 shadow-lg shadow-cyan-500/10"
          : "text-slate-400 hover:bg-white/5 hover:text-white"
      )}
    >
      <Icon
        className={clsx(
          "h-5 w-5 transition-colors",
          isActive
            ? "text-cyan-300"
            : "text-slate-500 group-hover:text-white"
        )}
      />

      <span className="font-medium">
        {item.title}
      </span>
    </Link>
  );
}