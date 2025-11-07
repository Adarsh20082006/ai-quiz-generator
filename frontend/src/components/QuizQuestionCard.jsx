export default function QuizQuestionCard({ data, onSelect, selected }) {
    const { question, options, difficulty } = data;
    return (
        <div className="bg-white rounded-xl shadow p-4 border">
            <div className="flex items-start justify-between gap-3">
                <h3 className="font-semibold">{question}</h3>
                {difficulty && <span className="text-xs bg-gray-100 border px-2 py-1 rounded">{difficulty}</span>}
            </div>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2">
                {options.map((opt, i) => {
                    const active = selected === opt;
                    return (
                        <button
                            key={i}
                            onClick={() => onSelect(opt)}
                            className={`border rounded p-2 bg-gray-100 text-left ${active ? "bg-blue-600 text-white" : "hover:bg-gray-200"}`}
                        >
                            {opt}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
