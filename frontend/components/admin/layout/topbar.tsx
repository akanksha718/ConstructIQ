"use client";

import { Bell, Search } from "lucide-react";
import { UserButton } from "@clerk/nextjs";

import MobileSidebar from "./mobile-sidebar";

export default function Topbar() {
    return (
        <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl">
            <div className="flex h-16 items-center justify-between px-6">
                {/* Left */}
                <div className="flex items-center gap-4">
                    <MobileSidebar />

                    <div className="relative hidden md:block">
                        <Search
                            className="
                absolute
                left-3
                top-1/2
                h-4
                w-4
                -translate-y-1/2
                text-slate-500
              "
                        />

                        <input
                            placeholder="Search knowledge..."
                            className="
                w-80
                rounded-xl
                border
                border-white/10
                bg-white/5
                py-2
                pl-10
                pr-4
                text-sm
                text-white
                outline-none
                placeholder:text-slate-500
                focus:border-cyan-400/40
              "
                        />
                    </div>
                </div>

                {/* Right */}
                <div className="flex items-center gap-4">
                    <button
                        className="
              rounded-xl
              border
              border-white/10
              bg-white/5
              p-2
              text-slate-300
              transition
              hover:bg-white/10
            "
                    >
                        <Bell className="h-5 w-5" />
                    </button>

                    <UserButton
                        appearance={{
                            elements: {
                                avatarBox: "h-10 w-10",
                            },
                        }}
                    />
                </div>
            </div>
        </header>
    );
}