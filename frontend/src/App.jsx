import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./Pages/Landing";
import GenerateQuiz from "./Pages/GenerateQuiz";
import History from "./Pages/History";
import QuizDetail from "./Pages/QuizDetail";
import TakeQuiz from "./Pages/TakeQuiz";
import Scorecard from "./Pages/Scorecard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/generate_quiz" element={<GenerateQuiz />} />
        <Route path="/history" element={<History />} />
        <Route path="/quiz/:id" element={<QuizDetail />} />
        <Route path="/take_quiz" element={<TakeQuiz />} />
        <Route path="/scorecard" element={<Scorecard />} />
      </Routes>
    </BrowserRouter>
  );
}
