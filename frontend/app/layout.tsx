import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SentinelVultr · Blast Radius Zero Agent Platform",
  description: "Autonomous Agent Orchestration with Isolated Sandboxing on Vultr Cloud Compute & Vultr Serverless Inference",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#060b18] text-slate-100 min-h-screen antialiased selection:bg-vultr-blue selection:text-white">
        {children}
      </body>
    </html>
  );
}

