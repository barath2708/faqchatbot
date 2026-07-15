import ChatBox from "../components/ChatBox";
import GraphBackground from "../components/GraphBackground";

const TOPICS = [
  {
    n: "01 — CORE",
    title: "Keras & Model Building",
    desc: "Sequential vs functional API, layers, custom training loops.",
  },
  {
    n: "02 — DATA",
    title: "tf.data Pipelines",
    desc: "Loading, batching, and optimizing input pipelines for training.",
  },
  {
    n: "03 — DEPLOY",
    title: "Deployment & Serving",
    desc: "TensorFlow Lite, TF Serving, and exporting SavedModel formats.",
  },
];

function Home() {
  return (
    <div className="relative">
      <GraphBackground />

      <div className="relative z-[2]">
        <div className="max-w-[900px] mx-auto px-6 pt-16 md:pt-20 pb-6 text-center">
          <span className="inline-flex items-center gap-2 font-mono text-xs tracking-widest uppercase text-edge border border-edge/35 bg-edge/[0.06] px-3.5 py-1.5 rounded-full mb-7">
            <span className="w-1.5 h-1.5 rounded-full bg-edge shadow-[0_0_8px_#2dd4bf]" />
            Answers sourced from tensorflow.org
          </span>

          <h1 className="font-display font-bold text-4xl md:text-[56px] leading-[1.08] tracking-tight mb-4">
            Ask anything about{" "}
            <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent">
              TensorFlow.
            </span>
          </h1>

          <p className="text-[17px] text-muted max-w-[520px] mx-auto mb-10 leading-relaxed">
            Instant, cited answers pulled straight from official docs, guides, and API
            references — no more digging through tabs.
          </p>

          <ChatBox />
        </div>

        <section className="max-w-[1040px] mx-auto px-6 pt-24 pb-24">
          <h2 className="font-display font-bold text-3xl tracking-tight mb-2">
            Explore TensorFlow topics
          </h2>
          <p className="text-muted text-[15px] mb-9">
            Jump into common areas people ask about, sourced from the official docs.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {TOPICS.map((t) => (
              <div
                key={t.title}
                className="bg-surface border border-border rounded-2xl p-6 hover:border-accent hover:-translate-y-1 transition cursor-pointer"
              >
                <div className="font-mono text-accent text-xs mb-3.5">{t.n}</div>
                <h3 className="text-[17px] font-semibold mb-2">{t.title}</h3>
                <p className="text-[13.5px] text-muted leading-relaxed">{t.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <footer className="border-t border-border py-7 text-center text-muted text-xs">
          FAQ Chatbot · powered by your ingested tensorflow.org knowledge base
        </footer>
      </div>
    </div>
  );
}

export default Home;