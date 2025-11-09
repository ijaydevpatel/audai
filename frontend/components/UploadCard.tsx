"use client";

import { useState } from "react";
import { enqueueJob, getSignedUploadUrl } from "../lib/api";

type UploadState = "idle" | "uploading" | "processing" | "error";

export default function UploadCard() {
  const [state, setState] = useState<UploadState>("idle");
  const [preserveHarmonium, setPreserveHarmonium] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setError(null);
    setState("uploading");

    try {
      const signed = await getSignedUploadUrl(file.name, file.type);
      await fetch(signed.url, {
        method: "PUT",
        headers: { "Content-Type": file.type },
        body: file,
      });

      setState("processing");
      await enqueueJob({
        title: file.name,
        sourceObjectKey: signed.objectKey,
        preserveHarmonium,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
      setState("error");
    }
  }

  return (
    <div className="rounded-3xl border border-white/50 bg-white/70 p-10 shadow-lg backdrop-blur">
      <h2 className="text-xl font-semibold text-amber-700">Upload your Katha</h2>
      <p className="mt-2 text-sm text-slate-600">
        Drag and drop WAV/MP3 files. We automatically trim silence, preserve harmonium, and enhance the main speaker.
      </p>

      <label
        className="mt-8 flex cursor-pointer flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed border-amber-200 bg-white/80 px-6 py-16 text-center transition hover:border-amber-400"
      >
        <input className="hidden" type="file" accept="audio/*" onChange={handleFileChange} />
        <span className="rounded-full bg-amber-500 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-white shadow">
          {state === "uploading" ? "Uploading…" : state === "processing" ? "Processing…" : "Select audio"}
        </span>
        <span className="text-xs text-slate-500">
          Supports English, Hindi, and Gujarati blends with harmonium intros.
        </span>
      </label>

      <div className="mt-6 flex items-center justify-between rounded-2xl border border-white/60 bg-white/80 px-4 py-3">
        <label className="flex items-center gap-2 text-xs font-medium text-slate-600">
          <input
            checked={preserveHarmonium}
            onChange={(event) => setPreserveHarmonium(event.target.checked)}
            type="checkbox"
            className="h-4 w-4 rounded border-amber-200 text-amber-500 focus:ring-amber-400"
          />
          Preserve harmonium & intro vocals
        </label>
        <span className="text-[10px] uppercase tracking-wide text-amber-500">
          GPT-guided filters
        </span>
      </div>

      {error && <p className="mt-4 text-xs text-red-500">{error}</p>}
    </div>
  );
}
