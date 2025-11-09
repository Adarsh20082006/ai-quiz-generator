import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./Pages/Landing";
import GenerateQuiz from "./Pages/GenerateQuiz";
import History from "./Pages/History";
import QuizDetail from "./Pages/QuizDetail";
import TakeQuiz from "./Pages/TakeQuiz";
import Scorecard from "./Pages/Scorecard";
import NotFound from "./Pages/NotFound";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} /> {/*Landing Page Route*/}
        <Route path="/generate_quiz" element={<GenerateQuiz />} /> {/*Generate quiz page Route*/}
        <Route path="/history" element={<History />} /> {/*History page Route*/}
        <Route path="/quiz/:id" element={<QuizDetail />} /> {/*Quiz details page Route*/}
        <Route path="/take_quiz" element={<TakeQuiz />} /> {/*Take quiz page Route*/}
        <Route path="/scorecard" element={<Scorecard />} /> {/*Scorecard page Route*/}
        <Route path="*" element={<NotFound />} /> {/*Not Found Route*/}

      </Routes>
    </BrowserRouter>
  );
}
