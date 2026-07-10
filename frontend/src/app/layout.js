import "./globals.css";

export const metadata = {
  title: "Weekly Report Generator & Team Dashboard",
  description: "Submit weekly reports and track team progress.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
