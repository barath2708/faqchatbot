import { useState } from "react";
import AnswerCard from "./AnswerCard";

// Determine API base URL based on environment
const getAPIBaseURL = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // For localhost development
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    return "http://localhost:8000";
  }
  
  // For GitHub Codespaces: replace the port number in the domain
  // Example: ominous-rotary-phone-vj9jgvrxghpg6x-5173.app.github.dev -> ominous-rotary-phone-vj9jgvrxghpg6x-8000.app.github.dev
  if (hostname.includes("app.github.dev")) {
    return `${protocol}//${hostname.replace(/-5173\./, "-8000.")}`;
  }
  
  // Generic fallback: replace port in URL
  const origin = window.location.origin;
  if (origin.includes(":5173")) {
    return origin.replace(":5173", ":8000");
  }
  
  // Last resort: just return localhost
  return "http://localhost:8000";
};

const API_BASE_URL = getAPIBaseURL();

function ChatBox() {
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setError(null);

    try {
      const url = `${API_BASE_URL}/question/ask`;
      console.log("Sending request to:", url);
      
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
      });

      console.log("Response status:", response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", errorText);
        throw new Error(`Request failed with status ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log("Response data:", data);

      setConversation((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          question: trimmed,
          answer: data.answer,
          sources: data.sources,
          fromCache: data.from_cache,
        },
      ]);
      setQuestion("");
    } catch (err) {
      console.error("Error details:", err);
      setError("Something went wrong getting an answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-4">
        {conversation.map((entry) => (
          <AnswerCard
            key={entry.id}
            question={entry.question}
            answer={entry.answer}
            sources={entry.sources}
            fromCache={entry.fromCache}
          />
        ))}
      </div>

      {error && <p className="text-red-600 text-sm">{error}</p>}

      <form onSubmit={handleSubmit} className="flex gap-2 sticky bottom-0 bg-gray-50 py-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="bg-blue-600 text-white px-5 py-2 rounded-lg disabled:opacity-50 hover:bg-blue-700"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>
    </div>
  );
}

export default ChatBox;
