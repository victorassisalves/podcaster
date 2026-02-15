import PodcastWizard from './components/PodcastWizard';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <h1 className="text-4xl font-bold mb-8 text-gray-800">Podcaster AI</h1>
      <PodcastWizard />
    </main>
  )
}
