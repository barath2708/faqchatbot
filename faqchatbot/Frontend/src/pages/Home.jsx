import ChatBox from "../components/ChatBox";

function Home() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-800 mb-1">Ask a question</h1>
      <p className="text-gray-500 mb-6">
        Get answers based on our FAQ knowledge base.
      </p>
      <ChatBox />
    </div>
  );
}

export default Home;