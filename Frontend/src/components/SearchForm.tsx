// src/components/SearchForm.tsx
interface SearchFormProps {
  topic: string;
  setTopic: (topic: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

function SearchForm({ topic, setTopic, onSubmit, isLoading }: SearchFormProps) {
  return (
    <form onSubmit={onSubmit} className="flex w-full max-w-lg mx-auto my-8">
      <input
        type="text"
        placeholder="Enter a topic (e.g., Quantum Computing)"
        className="flex-grow p-3 text-white bg-zinc-800 border border-zinc-700 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        disabled={isLoading}
      />
      <button
        type="submit"
        className="px-6 py-3 font-bold text-white bg-green-600 rounded-r-lg hover:bg-green-700 transition-colors disabled:bg-zinc-500 disabled:cursor-not-allowed"
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Create My Briefing'}
      </button>
    </form>
  );
}

export default SearchForm;