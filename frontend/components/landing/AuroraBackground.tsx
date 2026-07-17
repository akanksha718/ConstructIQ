export default function AuroraBackground() {
  return (
    <>
      {/* Grid */}

      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,.03)_1px,transparent_1px)] bg-[size:60px_60px]" />

      {/* Cyan */}

      <div className="absolute -left-48 top-0 h-[650px] w-[650px] rounded-full bg-cyan-500/20 blur-[170px] animate-float" />

      {/* Purple */}

      <div className="absolute right-[-200px] top-20 h-[600px] w-[600px] rounded-full bg-violet-600/20 blur-[180px] animate-float" />

      {/* Blue */}

      <div className="absolute bottom-[-250px] left-1/3 h-[700px] w-[700px] rounded-full bg-blue-500/15 blur-[190px] animate-float" />

      {/* Overlay */}

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent,rgba(5,8,22,.7))]" />
    </>
  );
}