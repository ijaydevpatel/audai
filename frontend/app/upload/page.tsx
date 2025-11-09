import UploadCard from "../../components/UploadCard";
import WaveformPreview from "../../components/WaveformPreview";

export default function UploadPage() {
  return (
    <div className="grid gap-8 lg:grid-cols-[1.5fr,1fr]">
      <UploadCard />
      <WaveformPreview />
    </div>
  );
}
