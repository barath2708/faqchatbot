import { useState, useEffect } from "react";

const getAPIBaseURL = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  if (hostname === "localhost" || hostname === "127.0.0.1") return "http://localhost:8000";
  if (hostname.includes("app.github.dev")) return `${protocol}//${hostname.replace(/-5173\./, "-8000.")}`;
  const origin = window.location.origin;
  if (origin.includes(":5173")) return origin.replace(":5173", ":8000");
  return "http://localhost:8000";
};
const API_BASE_URL = getAPIBaseURL();

function Admin() {
  const [urls, setUrls] = useState("");
  const [questionSelector, setQuestionSelector] = useState("");
  const [answerSelector, setAnswerSelector] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [sources, setSources] = useState([]);
  const [sourcesLoading, setSourcesLoading] = useState(true);

  const fetchSources = async () => {
    setSourcesLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/sources/`);
      const data = await response.json();
      setSources(data);
    } catch (err) {
      console.error("Failed to load sources:", err);
    } finally {
      setSourcesLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, []);

  const handleScrape = async (e) => {
    e.preventDefault();
    const urlList = urls
      .split("\n")
      .map((u) => u.trim())
      .filter(Boolean);

    if (urlList.length === 0) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/admin/scrape`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          urls: urlList,
          question_selector: questionSelector || null,
          answer_selector: answerSelector || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      fetchSources();
    } catch (err) {
      setError("Scrape failed. Check the URLs and selectors, then try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 flex flex-col gap-8">
      <div>
        <h1 className="font-display text-2xl font-bold mb-1">Admin</h1>
        <p className="text-muted mb-6 text-sm">
          Scrape FAQ pages to add them to the knowledge base.
        </p>

        <form
          onSubmit={handleScrape}
          className="bg-surface border border-border rounded-2xl p-5 flex flex-col gap-4"
        >
          <div>
            <label className="text-sm font-medium text-[#dfe4e8] block mb-1.5">
              FAQ URLs (one per line)
            </label>
            <textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              placeholder="https://tensorflow.org/faq"
              rows={4}
              className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-sm outline-none focus:border-accent placeholder:text-[#5c6672]"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-[#dfe4e8] block mb-1.5">
                Question CSS selector (optional)
              </label>
              <input
                type="text"
                value={questionSelector}
                onChange={(e) => setQuestionSelector(e.target.value)}
                placeholder="h3.faq-question"
                className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-sm outline-none focus:border-accent placeholder:text-[#5c6672]"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-[#dfe4e8] block mb-1.5">
                Answer CSS selector (optional)
              </label>
              <input
                type="text"
                value={answerSelector}
                onChange={(e) => setAnswerSelector(e.target.value)}
                placeholder="div.faq-answer"
                className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-sm outline-none focus:border-accent placeholder:text-[#5c6672]"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !urls.trim()}
            className="bg-accent text-[#0a0e12] font-semibold px-5 py-2 rounded-lg disabled:opacity-40 hover:-translate-y-0.5 transition self-start text-sm"
          >
            {loading ? "Scraping..." : "Scrape & Index"}
          </button>

          {error && <p className="text-red-400 text-sm">{error}</p>}
          {result && (
            <p className="text-emerald-400 text-sm">
              ✅ Scraped {result.pages_scraped} page(s), created {result.chunks_created} chunk(s).
            </p>
          )}
        </form>
      </div>

      <div>
        <h2 className="font-display text-lg font-semibold mb-3">Ingested sources</h2>
        {sourcesLoading ? (
          <p className="text-muted text-sm">Loading...</p>
        ) : sources.length === 0 ? (
          <p className="text-muted text-sm">No sources ingested yet.</p>
        ) : (
          <div className="bg-surface border border-border rounded-2xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-surface2 text-muted">
                <tr>
                  <th className="text-left px-4 py-2 font-medium">URL</th>
                  <th className="text-left px-4 py-2 font-medium">Status</th>
                  <th className="text-left px-4 py-2 font-medium">Chunks</th>
                </tr>
              </thead>
              <tbody>
                {sources.map((source) => (
                  <tr key={source.id} className="border-t border-border">
                    <td className="px-4 py-2 break-all font-mono text-xs text-[#dfe4e8]">
                      {source.url}
                    </td>
                    <td className="px-4 py-2">
                      <span
                        className={`px-2 py-0.5 rounded text-xs border ${
                          source.status === "success"
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                            : source.status === "failed"
                            ? "bg-red-500/10 text-red-400 border-red-500/30"
                            : "bg-white/5 text-muted border-border"
                        }`}
                      >
                        {source.status}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-muted">{source.chunks_created}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Admin;