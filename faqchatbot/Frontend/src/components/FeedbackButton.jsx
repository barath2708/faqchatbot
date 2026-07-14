import { useState } from "react";

const API_BASE_URL = "https://ominous-rotary-phone-vj9jgvrxghpg6x-8000.app.github.dev";

function FeedbackButton({ question, answer }) {
  const [submitted, setSubmitted] = useState(null); // null | "up" | "down"

  const sendFeedback = async (isHelpful) => {
    setSubmitted(isHelpful ? "up" : "down");
    try {
      await fetch(`${API_BASE_URL}/question/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, is_helpful: isHelpful }),
      });
    } catch (err) {
      console.error("Failed to send feedback:", err);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => sendFeedback(true)}
        disabled={submitted !== null}
        className={`text-sm px-2 py-1 rounded ${
          submitted === "up" ? "bg-green-100 text-green-700" : "hover:bg-gray-100 text-gray-500"
        }`}
        aria-label="Mark answer as helpful"
      >
        👍
      </button>
      <button
        onClick={() => sendFeedback(false)}
        disabled={submitted !== null}
        className={`text-sm px-2 py-1 rounded ${
          submitted === "down" ? "bg-red-100 text-red-700" : "hover:bg-gray-100 text-gray-500"
        }`}
        aria-label="Mark answer as not helpful"
      >
        👎
      </button>
    </div>
  );
}

export default FeedbackButton;
