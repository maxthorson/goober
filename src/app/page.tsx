import BubbleMenuClient from '../components/BubbleMenuClient'
import Waves from '../components/Waves'

export default function Home() {
  return (
    <div className="min-h-screen relative">
  <Waves lineColor="rgba(255,255,255,0.18)" backgroundColor="rgba(0,0,0,0.12)" />
      <BubbleMenuClient />
      <div className="pointer-events-auto flex items-center justify-center min-h-screen">
        <h1 className="text-6xl font-bold text-white">The next generation is here.</h1>
      </div>
    </div>
  )
}
