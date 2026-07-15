import { useState } from "react";
import SourceList from "./SourceList";
import FeedbackButton from "./FeedbackButton";

function AnswerCard({ chatLogId, question, answer, sources, fromCache }) {
  const [showSources, setShowSources] = useState(false);

  return (
    <div className="bg-surface border border-border rounded-2xl px-6 py-5">
      <p className="text-[11px] uppercase tracking-wider text-muted font-mono mb-1.5">You asked</p>
      <p className="text-[15.5px] text-[#dfe4e8] mb-4 pb-4 border-b border-border">{question}</p>

      <p className="text-[11px] uppercase tracking-wider text-accent2 font-mono mb-1.5">Answer</p>
      <p className="text-[15px] leading-relaxed whitespace-pre-line">{answer}</p>

      <div className="flex items-center justify-between mt-4 pt-3.5 border-t border-border">
        <div className="flex items-center gap-3">
          {sources?.length > 0 && (
            <button
              onClick={() => setShowSources((prev) => !prev)}
              className="text-[13px] text-edge hover:underline"
            >
              {showSources ? "Hide sources" : `View sources (${sources.length})`}
            </button>
          )}
          {fromCache && (
            <span className="text-xs text-muted italic">⚡ cached answer</span>
          )}
        </div>

        <FeedbackButton chatLogId={chatLogId} />
      </div>

      {showSources && <SourceList sources={sources} />}
    </div>
  );
}

export default AnswerCard;