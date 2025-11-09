# Audai Frontend

Next.js 14 + Tailwind CSS UI for uploading, tracking, and downloading enhanced Katha audio.

## Key Screens
- **Home** – CTA for new upload, overview of processing pipeline.
- **Upload** – Drag-and-drop card with harmonium preservation toggle and waveform preview.
- **Status** – Polls backend for pipeline progress and shows stage timeline.
- **History** – Lists processed files with LUFS + language metadata.

## Development
1. Install deps: `npm install`
2. Create `.env.local` with `NEXT_PUBLIC_API_BASE=http://localhost:8000`
3. Run dev server: `npm run dev`

## Styling
- Tailwind with glassmorphism surfaces.
- Custom gradients in `styles/globals.css`.
