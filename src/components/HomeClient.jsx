"use client";

import BubbleMenuClient from './BubbleMenuClient'
import Waves from './Waves'

export default function HomeClient() {
  return (
    <div className="min-h-screen relative">
      <Waves lineColor="rgba(255,255,255,0.18)" backgroundColor="rgba(0,0,0,0.12)" />
      <BubbleMenuClient />
      <div className="pointer-events-auto flex flex-col items-center justify-center min-h-screen gap-6">
        <h1 className="text-6xl font-bold text-white">The next generation is here.</h1>
        <a
          href="/products"
          className="inline-block rounded-full bg-white text-black font-semibold px-6 py-3 shadow hover:opacity-95"
        >
          View products
        </a>
      </div>
    </div>
  )
}
