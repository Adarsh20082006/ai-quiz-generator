import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import QuizQuestionCard from "../components/QuizQuestionCard";

export default function TakeQuiz() {
    const { state } = useLocation(); // expects { quiz }
    const navigate = useNavigate();
    const quiz = state?.quiz;
    console.log(quiz);
    const [idx, setIdx] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [score, setScore] = useState(0);

    useEffect(() => {
        if (!quiz) navigate("/");
    }, [quiz, navigate]);

    if (!quiz) return null;
    const questions = quiz.quiz_data.quiz || [];

    const onSelect = (opt) => {
        const correct = questions[idx].answer;
        const isCorrect = opt === correct;

        // Update answers
        const nextAnswers = [...answers];
        nextAnswers[idx] = opt;
        setAnswers(nextAnswers);

        // Update score immediately (calculate final if last)
        const newScore = isCorrect ? score + 1 : score;

        if (idx + 1 < questions.length) {
            setScore(newScore);
            setIdx(idx + 1);
        } else {
            // Navigate to Scorecard with correct final data
            navigate("/scorecard", {
                state: { score: newScore, total: questions.length, quiz, answers: nextAnswers },
            });
        }
    };

    return (
        <div className="min-h-screen p-4 max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-3">
                <h2 className="text-xl font-bold text-slate-900">Take Quiz</h2>
                <span className="text-sm text-gray-600">
                    {idx + 1} / {questions.length}
                </span>
            </div>

            <QuizQuestionCard
                data={questions[idx]}
                onSelect={onSelect}
                selected={answers[idx]}
            />
        </div>
    );
}
