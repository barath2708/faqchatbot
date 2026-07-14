import { useState } from "react";
import SourceList from "./SourceList";
import FeedbackButton from "./FeedbackButton";

function AnswerCard({ question, answer, sources, fromCache }) {
  const [showSources, setShowSources] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
      <p className="text-sm font-medium text-gray-500 mb-1">You asked</p>
      <p className="text-gray-900 mb-3">{question}</p>

      <p className="text-sm font-medium text-gray-500 mb-1">Answer</p>
      <p className="text-gray-800 whitespace-pre-line">{answer}</p>

      <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
        <div className="flex items-center gap-3">
          {sources?.length > 0 && (
            <button
              onClick={() => setShowSources((prev) => !prev)}
              className="text-sm text-blue-600 hover:underline"
            >
              {showSources ? "Hide sources" : `View sources (${sources.length})`}
            </button>
          )}
          {fromCache && (
            <span className="text-xs text-gray-400 italic">⚡ cached answer</span>
          )}
        </div>

        <FeedbackButton question={question} answer={answer} />
      </div>

      {showSources && <SourceList sources={sources} />}
    </div>
  );
}

export default AnswerCard;