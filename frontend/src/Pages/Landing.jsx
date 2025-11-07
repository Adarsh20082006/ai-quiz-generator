import { Link } from "react-router-dom";

export default function Landing() {
    return (
        <div className="min-h-screen   flex flex-col items-center justify-center text-center px-4">
            <h1 className="text-4xl font-extrabold text-slate-900 mb-2">AI Wiki Quiz Generator</h1>
            <p className="text-slate-600 max-w-md mb-8">
                Learn interactively from Wikipedia using AI-powered quizzes. Select a topic, test yourself, and track your learning.
            </p>

            <div className="w-full max-w-sm space-y-3">
                <Link to="/generate_quiz" className="block bg-blue-500 hover:bg-blue-600 text-white rounded-lg py-3 font-medium shadow-sm">
                    Generate Quiz
                </Link>
                <Link to="/history" className="block bg-green-500 hover:bg-green-600 text-white rounded-lg py-3 font-medium shadow-sm">
                    View History
                </Link>
            </div>
        </div>

    );
}
