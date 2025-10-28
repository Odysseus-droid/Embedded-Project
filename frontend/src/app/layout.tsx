import type React from "react"
import type { Metadata, Viewport } from "next"
import { Inter, Space_Grotesk } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const _inter = Inter({ subsets: ["latin"] })
const _spaceGrotesk = Space_Grotesk({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Expressway Dashboard",
  description: "Smart Expressway Management System Dashboard",
  icons: [
    {
      rel: "icon",
      url: "/Highway.svg",
      type: "image/svg+xml",
      sizes: "any"
    },
    {
      rel: "apple-touch-icon",
      url: "/Highway.svg",
      type: "image/svg+xml"
    }
  ]
}

export const viewport: Viewport = {
  themeColor: "#f97316",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" type="image/svg+xml" href="/Highway.svg" sizes="any" />
        <link rel="apple-touch-icon" type="image/svg+xml" href="/Highway.svg" />
      </head>
      <body className={`font-sans antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
