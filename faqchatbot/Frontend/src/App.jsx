import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Admin from "./pages/Admin";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white border-b px-6 py-4 flex gap-6 shadow-sm">
          <Link to="/" className="font-semibold text-gray-800 hover:text-blue-600">
            FAQ Chatbot
          </Link>
          <Link to="/admin" className="text-gray-600 hover:text-blue-600">
            Admin
          </Link>
        </nav>

        <main className="max-w-3xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;