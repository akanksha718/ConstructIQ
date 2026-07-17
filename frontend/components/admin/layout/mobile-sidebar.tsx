"use client";

import {
  Menu,
} from "lucide-react";

import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";

import Sidebar from "./sidebar";

export default function MobileSidebar() {
  return (
    <div className="lg:hidden">
      <Sheet>
        <SheetTrigger className="rounded-xl border border-white/10 bg-white/5 p-2 text-white">
          <Menu className="h-5 w-5" />
        </SheetTrigger>

        <SheetContent
          side="left"
          className="w-72 border-white/10 bg-slate-950 p-0"
        >
          <Sidebar mobile />
        </SheetContent>
      </Sheet>
    </div>
  );
}