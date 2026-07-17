"use client";

import React, { useEffect } from "react";
import { Sparkles } from "lucide-react";
import { toast } from "sonner";

const Layout = ({
    children,
}: {
    children: React.ReactNode;
}) => {
    useEffect(() => {
        const handleError = (event: ErrorEvent) => {
            toast.error(event.message || "Something went wrong");
        };

        const handleRejection = (event: PromiseRejectionEvent) => {
            toast.error(
                event.reason?.message ||
                event.reason ||
                "Unexpected error occurred"
            );
        };

        window.addEventListener("error", handleError);
        window.addEventListener("unhandledrejection", handleRejection);

        return () => {
            window.removeEventListener("error", handleError);
            window.removeEventListener(
                "unhandledrejection",
                handleRejection
            );
        };
    }, []);

    return (
        <div className="relative min-h-screen overflow-hidden bg-[#050816] text-white">

            {/* Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,.03)_1px,transparent_1px)] bg-[size:50px_50px]" />

            {/* Neon Orbs */}
            <div className="absolute -left-40 -top-32 h-[500px] w-[500px] rounded-full bg-cyan-500/20 blur-[180px]" />

            <div className="absolute right-[-150px] top-[20%] h-[450px] w-[450px] rounded-full bg-fuchsia-500/20 blur-[180px]" />

            <div className="absolute bottom-[-120px] left-[40%] h-[400px] w-[400px] rounded-full bg-blue-600/20 blur-[180px]" />

            {/* Radial Overlay */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent,rgba(0,0,0,0.55))]" />

            <div className="relative grid min-h-screen lg:grid-cols-2">

                {/* LEFT */}
                <div className="hidden lg:flex flex-col justify-center px-20">

                    <div className="inline-flex w-fit items-center gap-2 rounded-full border border-cyan-400/30 bg-white/5 px-3 py-1 backdrop-blur-xl shadow-[0_0_30px_rgba(6,182,212,.2)]">

                        <Sparkles className="h-4 w-4 text-cyan-400" />

                        <span className="text-sm font-medium text-cyan-200">
                            AI-powered Industrial Knowledge Intelligence
                        </span>

                    </div>

                    <h1 className="mt-7 text-7xl font-black leading-none tracking-tight">

                        <span className="bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-400 bg-clip-text text-transparent">

                            ConstructIQ-AI

                        </span>
                    </h1>

                    <p className="mt-8 max-w-xl text-lg leading-9 text-slate-300">

                        Search engineering documents, project drawings,
                        construction manuals, and company knowledge with an
                        intelligent AI assistant. Get accurate answers instantly
                        and make better project decisions.

                    </p>

                    {/* Stats */}

                    <div className="mt-14 flex gap-12">

                        <div>
                            <h2 className="text-4xl font-bold text-cyan-400">
                                10x
                            </h2>
                            <p className="mt-1 text-slate-400">
                                Faster Knowledge Search
                            </p>
                        </div>

                        <div>
                            <h2 className="text-4xl font-bold text-purple-400">
                                AI
                            </h2>
                            <p className="mt-1 text-slate-400">
                                Powered Responses
                            </p>
                        </div>

                    </div>

                </div>

                {/* RIGHT */}

                <div className="flex items-center justify-center p-6">

                    <div
                        className="
            w-full
            max-w-md
            rounded-[32px]
            border
            border-white/10
            bg-white/5
            p-8
            backdrop-blur-2xl
            shadow-[0_0_60px_rgba(0,255,255,.08)]
            "
                    >

                        {children}

                    </div>

                </div>

            </div>
        </div>
    );
};

export default Layout;