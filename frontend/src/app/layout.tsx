export default function RootLayout({ children }: { children: unknown }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}

