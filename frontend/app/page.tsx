import Link from "next/link";

export default function HomePage() {
  return (
    <section className="grid gap-12 md:grid-cols-[2fr,1fr]">
      <div className="rounded-3xl border border-white/50 bg-white/70 p-10 shadow-lg backdrop-blur">
        <h2 className="text-2xl font-semibold text-amber-700">Start a new enhancement</h2>
        <p className="mt-4 text-slate-600">
          Upload your raw Katha audio and let our harmonium-preserving AI clean, enhance, and master the experience automatically.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link
            className="rounded-full bg-amber-500 px-6 py-3 text-sm font-medium text-white shadow-lg transition hover:bg-amber-600"
            href="/upload"
          >
            Upload audio
          </Link>
          <Link
            className="rounded-full border border-amber-200 px-6 py-3 text-sm font-medium text-amber-600 transition hover:border-amber-400"
            href="/history"
          >
            View history
          </Link>
        </div>
      </div>
      <div className="rounded-3xl border border-white/60 bg-white/70 p-8 shadow-lg backdrop-blur">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-amber-600">
          How it works
        </h3>
        <ol className="mt-4 space-y-4 text-sm text-slate-600">
          <li><strong>Analyze</strong> — GPT-OSS-120B segments music, speech, and noise.</li>
          <li><strong>Enhance</strong> — Targeted denoisers and reverbs preserve harmonium warmth.</li>
          <li><strong>Deliver</strong> — Download crystal-clear discourse with LUFS-normalized levels.</li>
        </ol>
      </div>
    </section>
  );
}
