// src/App.tsx
import { useState } from 'react';
import Header from './components/Header';
import SearchForm from './components/SearchForm';
import NewsletterDisplay from './components/NewsletterDisplay';

function App() {
  const [topic, setTopic] = useState('');
  const [newsletterContent, setNewsletterContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerateNewsletter = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic) {
      setError('Please enter a topic.');
      return;
    }

    // Reset state for a new request
    setIsLoading(true);
    setError('');
    setNewsletterContent('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/generate-newsletter`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setNewsletterContent(data.final_newsletter);

    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-4 md:p-8">
      <Header />
      <SearchForm
        topic={topic}
        setTopic={setTopic}
        onSubmit={handleGenerateNewsletter}
        isLoading={isLoading}
      />
      <div className="w-full border-t border-zinc-700 my-8"></div>
      <NewsletterDisplay
        content={newsletterContent}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}

export default App;