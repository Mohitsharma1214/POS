import '../globals.css';
import type { ReactNode } from 'react';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Podcast Intelligence AI | Research Command Center',
  description: 'Automated guest research pipeline for top-tier podcasters. Generate virality briefs, analyze YouTube comments, and extract narrative patterns.',
  keywords: 'Podcast, AI, Guest Intelligence, Research, OpenRouter, YouTube Analytics',
};

export const viewport = {
  themeColor: '#090a0f',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-primary text-white min-h-screen antialiased`}>
        {children}
      </body>
    </html>
  );
}
