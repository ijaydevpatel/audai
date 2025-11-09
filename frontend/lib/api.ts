export type SignedUrlResponse = {
  url: string;
  objectKey: string;
};

export type EnqueueJobRequest = {
  title: string;
  sourceObjectKey: string;
  preserveHarmonium: boolean;
};

export type HistoryJob = {
  id: string;
  title: string;
  detectedLanguages: string[];
  lufs: number;
  preserveHarmonium: boolean;
  downloadUrl: string;
};

export type JobStage =
  | "uploaded"
  | "segmenting"
  | "harmonium_protect"
  | "denoising"
  | "voice_enhancement"
  | "mastering"
  | "delivered"
  | "failed";

export type JobStatus = {
  id: string;
  stage: JobStage;
  progress: number;
  message: string;
  updatedAt: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {}),
    },
    cache: "no-store",
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  return response.json() as Promise<T>;
}

export function getSignedUploadUrl(filename: string, contentType: string) {
  return request<SignedUrlResponse>(`/api/v1/files/sign-upload`, {
    method: "POST",
    body: JSON.stringify({ filename, contentType }),
  });
}

export function enqueueJob(payload: EnqueueJobRequest) {
  return request(`/api/v1/jobs`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getJobStatus(jobId: string) {
  return request<JobStatus>(`/api/v1/jobs/${jobId}`);
}

export function listJobs() {
  return request<HistoryJob[]>(`/api/v1/jobs`);
}
