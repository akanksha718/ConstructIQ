"use client";

import Logo from "./logo";
import NavItem from "./nav-item";
import StorageCard from "./storage-card";
import { useUser } from "@clerk/nextjs";
import { consoleNavigation } from "@/lib/admin-navigation";

interface SidebarProps {
    mobile?: boolean;
}

export default function Sidebar({
    mobile = false,
}: SidebarProps) {
    const { user, isLoaded } = useUser();

    return (
        <aside
            className={`
${mobile ? "flex" : "hidden lg:flex"}
w-70
shrink-0
flex-col
border-r
border-white/10
bg-slate-950/80
backdrop-blur-xl
`}
        >
            <div className="border-b border-white/10 p-3">
                <Logo />
            </div>

            <div className="flex-1 overflow-y-auto px-2 py-4">
                {consoleNavigation.map((group) => (
                    <div
                        key={group.title}
                        className="mb-6"
                    >
                        <p className="mb-2 px-2 text-xs font-semibold uppercase tracking-widest text-slate-500">
                            {group.title}
                        </p>

                        <div className="space-y-2">
                            {group.items.map((item) => (
                                <NavItem
                                    key={item.href}
                                    item={item}
                                />
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <div className="space-y-4 border-t border-white/10 p-5">
                <StorageCard />

                <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-full bg-cyan-500/20 font-semibold text-cyan-300">
                        A
                    </div>

                    <div>
                        <p className="font-medium text-white">
                            {user?.firstName}
                        </p>

                        <p className="text-xs text-slate-400">
                            System Administrator
                        </p>
                    </div>
                </div>
            </div>
        </aside>
    );
}