// src/components/Header.tsx

function Header() {
  return (
    <header className="text-center w-full max-w-2xl mx-auto mb-8">
      <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
        Scout AI Newsletter
      </h1>
      <p className="text-lg text-zinc-400 mt-2">
        Your personal AI-powered research assistant.
      </p>
    </header>
  );
}

export default Header;