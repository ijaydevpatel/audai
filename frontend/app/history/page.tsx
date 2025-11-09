import Link from "next/link";
import { listJobs } from "../../lib/api";

export default async function HistoryPage() {
  const jobs = await listJobs();

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/60 bg-white/70 p-8 shadow-lg backdrop-blur">
        <h2 className="text-xl font-semibold text-amber-700">Processing history</h2>
        <p className="mt-2 text-sm text-slate-600">
          Each job stores metadata including detected languages, harmonium markers, and LUFS normalization values for your records.
        </p>
      </div>

      <ul className="space-y-4">
        {jobs.map((job) => (
          <li
            key={job.id}
            className="flex flex-col gap-2 rounded-3xl border border-white/50 bg-white/70 p-6 shadow-md backdrop-blur lg:flex-row lg:items-center lg:justify-between"
          >
            <div>
              <p className="text-sm font-semibold text-amber-600">{job.title}</p>
              <p className="text-xs text-slate-500">
                {job.detectedLanguages.join(", ")} • LUFS: {job.lufs} • Harmonium preserved: {job.preserveHarmonium ? "Yes" : "No"}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link className="text-xs font-medium text-amber-600 hover:underline" href={`/status/${job.id}`}>
                View status
              </Link>
              <a
                className="rounded-full bg-amber-500 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-amber-600"
                href={job.downloadUrl}
              >
                Download
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
