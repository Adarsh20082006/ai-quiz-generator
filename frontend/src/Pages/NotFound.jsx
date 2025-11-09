import { useNavigate } from "react-router-dom";
import { AlertTriangle } from "lucide-react";

export default function NotFound() {
    const navigate = useNavigate();

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[#0f172a] text-slate-100 text-center px-4">
            <AlertTriangle size={64} className="text-yellow-400 mb-4" />
            <h1 className="text-5xl font-extrabold mb-2">404</h1>
            <p className="text-lg text-slate-300 mb-6">
                Oops! The page you’re looking for doesn’t exist or was moved.
            </p>
            <button
                onClick={() => navigate("/")}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition"
            >
                Back to Dashboard
            </button>
        </div>
    );
}
