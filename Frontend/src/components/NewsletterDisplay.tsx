// src/components/NewsletterDisplay.tsx
interface NewsletterDisplayProps {
  content: string;
  isLoading: boolean;
  error: string;
}

function NewsletterDisplay({ content, isLoading, error }: NewsletterDisplayProps) {
  const renderContent = () => {
    if (isLoading) {
      return <p className="text-zinc-400">🧠 Generating your newsletter, please wait...</p>;
    }
    if (error) {
      return <p className="text-red-400">Error: {error}</p>;
    }
    if (content) {
      // Use pre-wrap to respect newlines and formatting from the backend
      return <p className="whitespace-pre-wrap">{content}</p>;
    }
    return <p className="text-zinc-400">The newsletter content will appear here once generated...</p>;
  };

  return (
    <section className="w-full max-w-2xl p-6 bg-zinc-800 border border-zinc-700 rounded-lg text-left">
      <h2 className="text-2xl font-bold mb-4">Your Generated Newsletter</h2>
      <div className="space-y-4 min-h-[100px]">
        {renderContent()}
      </div>
    </section>
  );
}

export default NewsletterDisplay;