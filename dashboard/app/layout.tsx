/*
  Root layout for the Balkonsolar Dashboard (Next.js App Router)
  - Applies global styles and Inter font
  - Wraps all pages in the ThemeProvider for dark/light mode
  - Sets up HTML metadata
*/
import type React from "react"
import "@/app/globals.css"
import { Inter } from "next/font/google"

import { ThemeProvider } from "@/components/theme-provider"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "BalkonSolar Dashboard",
  description: "Optimize your balcony solar panel and battery usage",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
