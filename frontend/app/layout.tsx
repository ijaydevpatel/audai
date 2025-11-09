import "../styles/globals.css";
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="bg-gradient-to-br from-amber-50 via-white to-yellow-100">
      <body className="min-h-screen font-sans text-slate-800 antialiased">
        <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-6 py-10">
          <header className="rounded-3xl border border-white/40 bg-white/60 p-8 shadow-xl backdrop-blur">
            <h1 className="text-3xl font-semibold tracking-tight text-amber-600">
              Audai – Katha Enhancement Studio
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Upload, enhance, and preserve sacred discourses with harmonium-conscious AI.
            </p>
          </header>
          <main className="flex-1">{children}</main>
          <footer className="rounded-3xl border border-white/40 bg-white/60 p-6 text-center text-xs text-slate-500 backdrop-blur">
            © {new Date().getFullYear()} Audai Labs. All rights reserved.
          </footer>
        </div>
      </body>
    </html>
  );
}
