// Next.js configuration for the Balkonsolar dashboard frontend
// - Ignores ESLint and TypeScript errors during build (for CI/deployment flexibility)
// - Disables Next.js image optimization (uses unoptimized images)
//
// See https://nextjs.org/docs/app/building-your-application/configuring/ for more info
/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
