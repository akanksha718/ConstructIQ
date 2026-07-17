"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Menu, X } from "lucide-react";
import { Show, UserButton, useUser } from "@clerk/nextjs";

export default function Navbar() {
    const [open, setOpen] = useState(false);
    const { user, isLoaded } = useUser();

    const role = user?.publicMetadata?.role;
    return (
        <header className="sticky top-0 z-50">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl">
                    <div className="flex h-16 items-center justify-between px-5">
                        {/* Logo */}
                        <Link href="/" className="flex items-center gap-3">

                            <div className="rounded-xl bg-cyan-500/20 p-2 backdrop-blur">
                                <Image
                                    src="/favicon.ico"
                                    alt="Logo"
                                    width={24}
                                    height={24}
                                    className="h-6 w-6"
                                />
                            </div>

                            <span className="text-xl font-bold sm:text-2xl">
                                ConstructIQ-
                                <span className="text-cyan-400">AI</span>
                            </span>

                        </Link>

                        {/* Desktop Buttons */}
                        <div className="hidden items-center gap-4 md:flex">
                            <Show when="signed-out">
                                <button
                                    onClick={() => setOpen(false)}
                                    className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 font-semibold shadow-[0_0_35px_rgba(6,182,212,.45)] transition duration-300 hover:scale-105">
                                    <Link href="/sign-in">
                                        Sign In
                                    </Link>
                                </button>
                            </Show>
                            <Show when="signed-in">
                                <button
                                    onClick={() =>
                                        setOpen(false)}
                                    className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-3 py-1.5 font-semibold shadow-[0_0_35px_rgba(6,182,212,.45)] transition duration-300 hover:scale-105">
                                    <Link href={role === "admin" ? "/admin/dashboard" : "/chat"}>
                                        {role === "admin" ? "Dashboard" : "Chat"}
                                    </Link>
                                </button>
                                <UserButton />
                            </Show>
                        </div>

                        {/* Mobile Toggle */}
                        <button
                            onClick={() => setOpen(!open)}
                            className="rounded-lg border border-white/10 bg-white/5 p-2 text-white transition hover:bg-white/10 md:hidden"
                        >
                            {open ? <X size={22} /> : <Menu size={22} />}
                        </button>
                    </div>

                    {/* Mobile Menu */}
                    <div
                        className={`overflow-hidden transition-all duration-300 md:hidden ${open ? "max-h-60 opacity-100" : "max-h-0 opacity-0"
                            }`}
                    >
                        <div className="border-t border-white/10 px-5 py-5">
                            <div className="flex flex-col gap-4 items-center justify-center">
                                <Show when="signed-out">
                                    <button
                                        onClick={() => setOpen(false)}
                                        className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-3 py-3 font-semibold shadow-[0_0_35px_rgba(6,182,212,.45)] transition duration-300 hover:scale-105">
                                        <Link href="/sign-in">
                                            Sign In
                                        </Link>
                                    </button>
                                </Show>
                                <Show when="signed-in">
                                    <button className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-3 py-1.5 font-semibold shadow-[0_0_35px_rgba(6,182,212,.45)] transition duration-300 hover:scale-105">
                                        <Link href={role === "admin" ? "/admin/dashboard" : "/chat"}>
                                            {role === "admin" ? "Dashboard" : "Chat"}
                                        </Link>
                                    </button>
                                    <UserButton />
                                </Show>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}