export default function QuizQuestionCard({ data, onSelect, selected }) {
    const { question, options, difficulty } = data;
    return (
        <div className="bg-slate-700 rounded-xl shadow p-4 border">
            <div className="flex items-start justify-between gap-3">
                <h3 className="font-semibold text-slate-200">{question}</h3>
                {difficulty && <span className="text-xs border px-2 py-1 rounded">{difficulty}</span>}
            </div>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2">
                {options.map((opt, i) => {
                    const active = selected === opt;
                    return (
                        <button
                            key={i}
                            onClick={() => onSelect(opt)}
                            className={`border border-slate-500 rounded p-2 text-left transition ${active
                                    ? "bg-blue-600 text-white border-blue-700"
                                    : "hover:bg-slate-800 hover:border-slate-400 text-slate-200"
                                }`}
                        >
                            {opt}
                        </button>

                    );
                })}
            </div>
        </div>
    );
}
