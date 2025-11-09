import clsx from "clsx";

import type { JobStatus } from "../lib/api";

export type JobStage =
  | "uploaded"
  | "segmenting"
  | "harmonium_protect"
  | "denoising"
  | "voice_enhancement"
  | "mastering"
  | "delivered"
  | "failed";

type StatusTimelineProps = {
  status: JobStatus;
};

const STAGE_LABELS: Record<JobStage, string> = {
  uploaded: "Uploaded",
  segmenting: "Segmenting with Whisper + GPT-OSS-120B",
  harmonium_protect: "Preserving harmonium passages",
  denoising: "Noise removal & gating",
  voice_enhancement: "Main speaker enhancement",
  mastering: "Reverb, EQ, LUFS mastering",
  delivered: "Ready for download",
  failed: "Processing failed",
};

const ORDER: JobStage[] = [
  "uploaded",
  "segmenting",
  "harmonium_protect",
  "denoising",
  "voice_enhancement",
  "mastering",
  "delivered",
];

export default function StatusTimeline({ status }: StatusTimelineProps) {
  return (
    <ol className="rounded-3xl border border-white/60 bg-white/70 p-8 shadow-lg backdrop-blur">
      {ORDER.map((stage) => {
        const currentIndex = ORDER.indexOf(status.stage);
        const stageIndex = ORDER.indexOf(stage);
        const completed = currentIndex !== -1 && stageIndex < currentIndex;
        const active = stage === status.stage;
        return (
          <li key={stage} className="flex items-start gap-4 py-4 first:pt-0 last:pb-0">
            <span
              className={clsx(
                "mt-1 h-3 w-3 rounded-full",
                completed && "bg-emerald-400",
                active && "bg-amber-500 animate-pulse",
                !completed && !active && "bg-slate-200"
              )}
            />
            <div>
              <p className="text-sm font-semibold text-amber-700">{STAGE_LABELS[stage]}</p>
              {active && (
                <p className="mt-1 text-xs text-slate-500">
                  {status.message} • {Math.round(status.progress * 100)}%
                </p>
              )}
            </div>
          </li>
        );
      })}

      {status.stage === "failed" && (
        <li className="mt-6 rounded-2xl border border-red-200 bg-red-50/70 p-4 text-xs text-red-600">
          Processing stopped: {status.message}
        </li>
      )}
    </ol>
  );
}
