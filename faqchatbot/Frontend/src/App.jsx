import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Admin from "./pages/Admin";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-bg text-[#eef2f5] font-sans">
        <nav className="flex items-center justify-between px-6 md:px-10 py-5 sticky top-0 z-10 backdrop-blur-md bg-bg/60 border-b border-white/5">
          <Link to="/" className="flex items-center gap-2.5 font-display font-bold text-lg tracking-tight">
            <svg viewBox="0 0 32 32" className="w-6 h-6">
              <circle cx="6" cy="16" r="3.4" fill="#ff7a1a" />
              <circle cx="16" cy="6" r="3.4" fill="#ff7a1a" />
              <circle cx="16" cy="26" r="3.4" fill="#ff7a1a" />
              <circle cx="26" cy="16" r="3.4" fill="#2dd4bf" />
              <line x1="6" y1="16" x2="16" y2="6" stroke="#3a4552" strokeWidth="1.6" />
              <line x1="6" y1="16" x2="16" y2="26" stroke="#3a4552" strokeWidth="1.6" />
              <line x1="16" y1="6" x2="26" y2="16" stroke="#3a4552" strokeWidth="1.6" />
              <line x1="16" y1="26" x2="26" y2="16" stroke="#3a4552" strokeWidth="1.6" />
            </svg>
            TensorFlow<span className="text-muted font-medium">FAQ</span>
          </Link>
          <Link
            to="/admin"
            className="text-sm font-semibold bg-accent text-[#0a0e12] px-4 py-2 rounded-lg hover:-translate-y-0.5 hover:shadow-[0_6px_20px_rgba(255,122,26,0.3)] transition"
          >
            Admin
          </Link>
        </nav>

        <main>
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