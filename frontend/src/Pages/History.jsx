import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import { Link } from "react-router-dom";

export default function History() {
    const [rows, setRows] = useState([]);

    useEffect(() => {
        getHistory().then(setRows).catch(() => alert("Failed to load history"));
    }, []);

    return (
        <div className="min-h-screen p-4 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-4">History</h2>

            <div className="bg-white rounded-xl shadow border overflow-x-auto">
                <table className="min-w-full text-sm">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="p-3 text-left">ID</th>
                            <th className="p-3 text-left">Title</th>
                            <th className="p-3 text-left">URL</th>
                            <th className="p-3 text-left">Date</th>
                            <th className="p-3 text-left">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((r) => (
                            <tr key={r.id} className="border-t">
                                <td className="p-3">{r.id}</td>
                                <td className="p-3">{r.title}</td>
                                <td className="p-3 max-w-[220px] truncate">{r.url}</td>
                                <td className="p-3">{new Date(r.date_generated).toLocaleString()}</td>
                                <td className="p-3">
                                    <Link to={`/quiz/${r.id}`} className="bg-blue-500 hover:bg-blue-600 text-white p-1.5 rounded hover:underline">
                                        Details
                                    </Link>
                                </td>
                            </tr>
                        ))}
                        {rows.length === 0 && (
                            <tr><td className="p-4 text-gray-600" colSpan="5">No data yet.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
