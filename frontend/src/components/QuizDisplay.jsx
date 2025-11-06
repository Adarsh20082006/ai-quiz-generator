export default function QuizDisplay({ quiz, answers }) {
    if (!quiz) return <p className="p-4 text-gray-600">No quiz data.</p>;
    console.log(answers)
    const checkAns = !!answers;

    return (
        <div className="bg-slate-100 min-h-screen p-4">
            <div className="max-w-3xl mx-auto space-y-6">
                {quiz.quiz?.map((q, idx) => (
                    <div
                        key={idx}
                        className="bg-white border border-slate-200 rounded-xl shadow-md p-5 hover:shadow-lg transition"
                    >
                        {/* Question Header */}
                        <div className="flex justify-between items-start mb-2">
                            <h3 className="font-semibold text-lg text-slate-900">
                                {idx + 1}. {q.question}
                            </h3>

                            {/* Difficulty Badge */}
                            <span
                                className={`text-xs font-semibold px-2 py-1 rounded-full ${q.difficulty === "hard"
                                    ? "bg-red-100 text-red-700"
                                    : q.difficulty === "medium"
                                        ? "bg-yellow-100 text-yellow-700"
                                        : "bg-green-100 text-green-700"
                                    }`}
                            >
                                {q.difficulty}
                            </span>
                        </div>

                        {/* Options */}
                        <ul className="space-y-2 mt-2">
                            {q.options.map((opt, i) => {
                                const isCorrect = q.answer === opt;
                                const isSelected = checkAns && answers[idx] === opt;

                                const correctClass =
                                    isCorrect
                                        ? "bg-green-200 border-green-400"
                                        : "";
                                const wrongClass =
                                    checkAns && isSelected && !isCorrect
                                        ? "bg-red-200 border-red-400"
                                        : "";

                                return (
                                    <li
                                        key={i}
                                        className={`border border-slate-200 rounded-lg px-3 py-2 transition cursor-pointer 
                      hover:bg-blue-50 ${correctClass} ${wrongClass}`}
                                    >
                                        {opt}
                                    </li>
                                );
                            })}
                        </ul>

                        {/* Correct Answer & Explanation */}
                        <p className="mt-3 text-sm text-green-700 font-medium">
                            ✅ Correct: {q.answer}
                        </p>
                        <p className="text-xs text-slate-600 mt-1">{q.explanation}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
