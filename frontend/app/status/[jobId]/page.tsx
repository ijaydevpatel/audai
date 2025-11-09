import { notFound } from "next/navigation";
import StatusTimeline from "../../../components/StatusTimeline";
import { getJobStatus } from "../../../lib/api";

type StatusPageProps = {
  params: { jobId: string };
};

export default async function StatusPage({ params }: StatusPageProps) {
  let status;
  try {
    status = await getJobStatus(params.jobId);
  } catch (error) {
    status = null;
  }

  if (!status) {
    notFound();
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/60 bg-white/70 p-8 shadow-lg backdrop-blur">
        <h2 className="text-xl font-semibold text-amber-700">Processing status</h2>
        <p className="mt-2 text-sm text-slate-600">
          We are orchestrating GPT-OSS-120B, denoisers, and harmonium-aware enhancement models. Feel free to close this tab—we will notify you once the master is ready.
        </p>
      </div>
      <StatusTimeline status={status} />
    </div>
  );
}
