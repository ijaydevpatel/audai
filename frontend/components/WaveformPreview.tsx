import Image from "next/image";

const placeholders = [
  { label: "Original", src: "/waveforms/original.svg" },
  { label: "Enhanced", src: "/waveforms/enhanced.svg" },
];

export default function WaveformPreview() {
  return (
    <aside className="space-y-4 rounded-3xl border border-white/60 bg-white/70 p-8 shadow-lg backdrop-blur">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-amber-600">Before / After</h2>
      <p className="text-xs text-slate-500">
        Compare the raw upload with the harmonium-aware master. Harmonium passages are enhanced with Bark-inspired timbre profiles while speech clarity is maximized.
      </p>
      <div className="space-y-6">
        {placeholders.map((waveform) => (
          <figure key={waveform.label} className="space-y-2">
            <figcaption className="text-xs font-medium text-slate-600">{waveform.label}</figcaption>
            <div className="relative h-24 w-full overflow-hidden rounded-2xl border border-amber-100 bg-white/80">
              <Image alt={`${waveform.label} waveform`} src={waveform.src} fill className="object-cover" />
            </div>
          </figure>
        ))}
      </div>
    </aside>
  );
}
