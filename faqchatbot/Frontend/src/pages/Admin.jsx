import { useState, useEffect } from "react";

const API_BASE_URL = "https://ominous-rotary-phone-vj9jgvrxghpg6x-8000.app.github.dev";

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
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-semibold text-gray-800 mb-1">Admin</h1>
        <p className="text-gray-500 mb-6">
          Scrape FAQ pages to add them to the knowledge base.
        </p>

        <form onSubmit={handleScrape} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm flex flex-col gap-4">
          <div>
            <label className="text-sm font-medium text-gray-700 block mb-1">
              FAQ URLs (one per line)
            </label>
            <textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              placeholder="https://example.com/faq"
              rows={4}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1">
                Question CSS selector (optional)
              </label>
              <input
                type="text"
                value={questionSelector}
                onChange={(e) => setQuestionSelector(e.target.value)}
                placeholder="h3.faq-question"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1">
                Answer CSS selector (optional)
              </label>
              <input
                type="text"
                value={answerSelector}
                onChange={(e) => setAnswerSelector(e.target.value)}
                placeholder="div.faq-answer"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !urls.trim()}
            className="bg-blue-600 text-white px-5 py-2 rounded-lg disabled:opacity-50 hover:bg-blue-700 self-start"
          >
            {loading ? "Scraping..." : "Scrape & Index"}
          </button>

          {error && <p className="text-red-600 text-sm">{error}</p>}
          {result && (
            <p className="text-green-700 text-sm">
              ✅ Scraped {result.pages_scraped} page(s), created {result.chunks_created} chunk(s).
            </p>
          )}
        </form>
      </div>

      <div>
        <h2 className="text-lg font-semibold text-gray-800 mb-3">Ingested sources</h2>
        {sourcesLoading ? (
          <p className="text-gray-500 text-sm">Loading...</p>
        ) : sources.length === 0 ? (
          <p className="text-gray-500 text-sm">No sources ingested yet.</p>
        ) : (
          <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-gray-600">
                <tr>
                  <th className="text-left px-4 py-2">URL</th>
                  <th className="text-left px-4 py-2">Status</th>
                  <th className="text-left px-4 py-2">Chunks</th>
                </tr>
              </thead>
              <tbody>
                {sources.map((source) => (
                  <tr key={source.id} className="border-t border-gray-100">
                    <td className="px-4 py-2 break-all">{source.url}</td>
                    <td className="px-4 py-2">
                      <span
                        className={`px-2 py-0.5 rounded text-xs ${
                          source.status === "success"
                            ? "bg-green-100 text-green-700"
                            : source.status === "failed"
                            ? "bg-red-100 text-red-700"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {source.status}
                      </span>
                    </td>
                    <td className="px-4 py-2">{source.chunks_created}</td>
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
