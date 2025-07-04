import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

// ✅ 타이머 컴포넌트 (상단 고정)
function CountdownTimer({ duration, onTimeOver }) {
    const [timeLeft, setTimeLeft] = useState(duration * 60);

    useEffect(() => {
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    onTimeOver();
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    return (
        <div className="text-right text-sm text-gray-700 font-medium mb-4">
            <div className="border rounded px-3 py-1 inline-block">
                Time Remaining: {minutes}:{seconds.toString().padStart(2, "0")}
            </div>
        </div>
    );
}

export default function ProductExam() {
    const { test_id } = useParams();
    const navigate = useNavigate();

    // ✅ 예시 문항 리스트
    const questions = [
        {
            question_id: "q1",
            instruction: "Read the following question and select the most appropriate option.",
            question_text: "If a train travels 120 km in 2 hours, what is its average speed?",
            options: ["50 km/h", "60 km/h", "70 km/h", "80 km/h", "90 km/h"],
        },
        {
            question_id: "q2",
            instruction: "Solve the following percentage problem.",
            question_text: "A shirt originally costs $80. After a 25% discount, what is the sale price?",
            options: ["$55", "$60", "$65", "$70", "$75"],
        },
    ];

    const duration_minutes = 25;
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [timeOver, setTimeOver] = useState(false);
    const current = questions[currentIndex];

    const handleSelect = (index) => {
        setAnswers((prev) => ({
            ...prev,
            [current.question_id]: index,
        }));
    };

    const handleNext = () => {
        if (currentIndex < questions.length - 1) setCurrentIndex(currentIndex + 1);
    };

    const handlePrev = () => {
        if (currentIndex > 0) setCurrentIndex(currentIndex - 1);
    };

    const handleMoveTo = (idx) => {
        setCurrentIndex(idx);
    };

    const handleSubmit = () => {
        alert("Test Completed!\nYour Score: 0/" + questions.length);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans px-6 py-6"
        >
            <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-[3fr_1fr] gap-6">
                {/* ✅ 좌측: 문제 및 선택지 */}
                <div>
                    <CountdownTimer duration={duration_minutes} onTimeOver={() => setTimeOver(true)} />

                    <p className="text-lg font-semibold mb-2">
                        Question {currentIndex + 1} of {questions.length}
                    </p>

                    {/* 지시문 강조 박스 */}
                    {current.instruction && (
                        <div className="bg-blue-50 border border-blue-300 text-blue-700 text-sm rounded p-3 mb-3">
                            {current.instruction}
                        </div>
                    )}

                    <p className="text-xl font-medium mb-6">{current.question_text}</p>

                    {/* 선택지 */}
                    <ul className="space-y-3">
                        {current.options.map((opt, idx) => {
                            const isSelected = answers[current.question_id] === idx;
                            return (
                                <li
                                    key={idx}
                                    onClick={() => handleSelect(idx)}
                                    className={`border rounded px-4 py-3 cursor-pointer flex items-center text-sm transition
                                        ${isSelected
                                            ? "bg-blue-100 border-blue-500"
                                            : "hover:bg-gray-100 border-gray-300"
                                        }`}
                                >
                                    <span className="mr-3 font-bold text-gray-700">{`①②③④⑤`[idx]}</span>
                                    <span>{opt}</span>
                                </li>
                            );
                        })}
                    </ul>

                    {/* 이동 버튼 */}
                    <div className="flex justify-between mt-8">
                        <button
                            onClick={handlePrev}
                            disabled={currentIndex === 0}
                            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded disabled:opacity-50"
                        >
                            Previous
                        </button>
                        {currentIndex < questions.length - 1 ? (
                            <button
                                onClick={handleNext}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                            >
                                Next
                            </button>
                        ) : (
                            <button
                                onClick={handleSubmit}
                                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
                            >
                                Submit
                            </button>
                        )}
                    </div>
                </div>

                {/* ✅ 우측: 현황판 */}
                <div className="bg-gray-50 border border-gray-200 p-4 rounded shadow-sm text-sm">
                    <h3 className="font-semibold text-gray-700 mb-2">Questions</h3>
                    <div className="grid grid-cols-5 gap-2 mb-4">
                        {questions.map((q, idx) => {
                            const answered = answers[q.question_id] !== undefined;
                            const isCurrent = idx === currentIndex;
                            return (
                                <button
                                    key={q.question_id}
                                    onClick={() => handleMoveTo(idx)}
                                    className={`w-8 h-8 rounded text-sm font-medium
                                        ${isCurrent
                                            ? "bg-blue-600 text-white"
                                            : answered
                                                ? "bg-blue-100 text-blue-800"
                                                : "bg-white border border-gray-300 text-gray-500"
                                        }`}
                                >
                                    {idx + 1}
                                </button>
                            );
                        })}
                    </div>

                    <div className="space-y-1">
                        <div className="flex items-center gap-2 text-xs text-gray-600">
                            <div className="w-4 h-4 rounded bg-blue-600" /> Current
                        </div>
                        <div className="flex items-center gap-2 text-xs text-gray-600">
                            <div className="w-4 h-4 rounded bg-blue-100" /> Answered
                        </div>
                        <div className="flex items-center gap-2 text-xs text-gray-600">
                            <div className="w-4 h-4 rounded border border-gray-300 bg-white" /> Not Answered
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
