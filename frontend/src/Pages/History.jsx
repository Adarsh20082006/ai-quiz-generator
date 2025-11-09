import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import { Link, useNavigate } from "react-router-dom";

export default function History() {
    const [rows, setRows] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        getHistory().then(setRows).catch(() => alert("Failed to load history"));
    }, []);

    return (
        <div className="min-h-screen p-4 max-w-5xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <h2 className="text-2xl font-bold text-slate-50">Quiz History</h2>
                <button
                    onClick={() => navigate("/")}
                    className="bg-slate-700 hover:bg-slate-600 text-slate-100 px-4 py-2 rounded-lg shadow transition"
                >
                    Back to Dashboard
                </button>
            </div>

            {/* Table container */}
            <div className="bg-slate-800 rounded-xl shadow-md border overflow-x-auto">
                <table className="min-w-full text-sm">
                    <thead className="bg-slate-700 text-slate-50 uppercase text-xs font-semibold">
                        <tr>
                            <th className="p-3 text-left">ID</th>
                            <th className="p-3 text-left">Title</th>
                            <th className="p-3 text-left">URL</th>
                            <th className="p-3 text-left">Date</th>
                            <th className="p-3 text-left">Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {rows.length > 0 ? (
                            rows.map((r) => (
                                <tr
                                    key={r.id}
                                    className="border-t hover:bg-slate-700 transition-colors"
                                >
                                    <td className="p-3 font-medium text-slate-50">{r.id}</td>
                                    <td className="p-3 text-slate-50">{r.title}</td>
                                    <td className="p-3 max-w-[220px] truncate text-blue-400 hover:underline">
                                        <a
                                            href={r.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            {r.url}
                                        </a>
                                    </td>
                                    <td className="p-3 text-slate-200">
                                        {new Date(r.date_generated).toLocaleString()}
                                    </td>
                                    <td className="p-3">
                                        <Link
                                            to={`/quiz/${r.id}`}
                                            className="bg-blue-600 hover:bg-blue-700 text-slate-200 px-3 py-1.5 rounded-md shadow-sm transition"
                                        >
                                            Details
                                        </Link>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td
                                    colSpan="5"
                                    className="p-6 text-center text-slate-600 italic"
                                >
                                    No quizzes generated yet. Try creating one!
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
