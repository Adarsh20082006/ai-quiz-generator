export default function QuizDisplay({ quiz, answers }) {
    if (!quiz) return <p className="p-4 text-gray-600">No quiz data.</p>;
    console.log(quiz);
    const checkAns = !!answers;

    return (
        <div className="bg-[#1e293b] rounded-2xl min-h-screen p-4">
            <div className="max-w-3xl mx-auto space-y-6">
                {quiz?.quiz_data?.quiz && quiz.quiz_data.quiz.length > 0 ? (
                  quiz.quiz_data.quiz.map((q, idx) => (
                    <div
                        key={idx}
                        className="bg-slate-700 border border-slate-800 rounded-xl shadow-md p-5 hover:shadow-lg transition"
                    >
                        {/* Question Header */}
                        <div className="flex justify-between items-start mb-2">
                            <h3 className="font-semibold text-lg text-slate-200">
                                {idx + 1}. {q.question}
                            </h3>

                            {/* Difficulty Badge */}
                            <span
                                className={`text-xs font-semibold px-2 py-1 rounded-full ${q.difficulty === "hard"
                                    ? "bg-red-500 text-slate-50"
                                    : q.difficulty === "medium"
                                        ? "bg-orange-400 text-slate-50"
                                        : "bg-emerald-600 text-slate-50"
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

                                const correctClass = isCorrect
                                    ? "bg-emerald-600 border-green-400"
                                    : "";
                                const wrongClass =
                                    checkAns && isSelected && !isCorrect
                                        ? "bg-red-500 border-red-400"
                                        : "";

                                return (
                                    <li
                                        key={i}
                                        className={`border border-slate-200 rounded-lg px-3 py-2 transition cursor-pointer 
                      hover:bg-slate-500 ${correctClass} ${wrongClass}`}
                                    >
                                        {opt}
                                    </li>
                                );
                            })}
                        </ul>

                        {/* Correct Answer & Explanation */}
                        <p className="mt-3 text-sm text-emerald-500 font-medium">
                            ✅ Correct: {q.answer}
                        </p>
                        <p className="text-xs text-slate-50 mt-1">{q.explanation}</p>

                        {/* ✅ Related Topics */}
                        {q.section && <p className="mt-3 text-sm text-slate-200 font-medium">
                            Related Topic : {q.section}
                        </p>}
                    </div>
                ))}
            </div>
        </div>
    ): (
          <p className="text-slate-400 text-center py-6">
            ⚠️ No quiz questions found. Please try generating again.
          </p>
        );}
