import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getTestQuestions } from "../../api/testApi";

export default function ProductExam() {
    const location = useLocation();
    const testId = location?.state?.testId;
    const testName = location?.state?.testName;

    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [submitted, setSubmitted] = useState(false);
    const [score, setScore] = useState(0);
    const [timeLeft, setTimeLeft] = useState(25 * 60); // 25분

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const data = await getTestQuestions(testId);
                setQuestions(data?.questions || []);
                setAnswers(new Array(data?.questions?.length || 0).fill(null));
            } catch (err) {
                console.error("문항 불러오기 실패:", err);
            }
        };
        fetchQuestions();
    }, [testId]);

    useEffect(() => {
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    handleSubmit();
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const formatTime = (seconds) => {
        const m = String(Math.floor(seconds / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${m}:${s}`;
    };

    const handleAnswer = (choiceIndex) => {
        const updated = [...answers];
        updated[currentIndex] = choiceIndex;
        setAnswers(updated);
    };

    const handleSubmit = () => {
        let sc = 0;
        answers.forEach((ans, idx) => {
            if (ans === questions[idx]?.correct) sc++;
        });
        setScore(sc);
        setSubmitted(true);
    };

    if (submitted) {
        return (
            <div className="flex flex-col items-center justify-center h-screen">
                <div className="bg-white p-8 rounded-xl shadow-md text-center w-[350px]">
                    <div className="text-green-600 text-3xl mb-4">✔</div>
                    <h2 className="text-xl font-semibold mb-2">Test Completed!</h2>
                    <p className="text-gray-600 mb-4">Thank you for taking the test.</p>
                    <div className="text-lg font-medium bg-blue-100 py-2 rounded">
                        Your Score: <strong>{score}</strong> / {questions.length}
                    </div>
                    <button
                        onClick={() => window.location.reload()}
                        className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        Take Test Again
                    </button>
                </div>
            </div>
        );
    }

    const current = questions[currentIndex];

    return (
        <div className="flex flex-col p-6 max-w-5xl mx-auto min-h-screen">
            {/* 타이머 */}
            <div className="flex justify-end text-gray-600 mb-4">
                Time Remaining: <span className="ml-2 font-semibold">{formatTime(timeLeft)}</span>
            </div>

            {/* 문항 영역 */}
            {current && (
                <div className="bg-white p-6 rounded-xl shadow-md w-full">
                    <div className="text-sm text-gray-500 mb-2">
                        Question {currentIndex + 1} of {questions.length}
                    </div>
                    <h3 className="text-lg font-semibold text-blue-700 mb-2">
                        {current.instruction}
                    </h3>
                    <div className="bg-blue-50 p-3 rounded-md mb-4 text-sm text-gray-800 leading-relaxed">
                        {current.content}
                    </div>

                    {/* 선택지 */}
                    <div className="flex flex-col gap-3">
                        {current.choices.map((choice, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleAnswer(idx)}
                                className={`text-left border px-4 py-2 rounded hover:bg-blue-50 ${answers[currentIndex] === idx
                                        ? "border-blue-500 bg-blue-100"
                                        : "border-gray-300"
                                    }`}
                            >
                                {idx + 1}. {choice}
                            </button>
                        ))}
                    </div>

                    {/* 하단 버튼 */}
                    <div className="flex justify-between mt-6">
                        <button
                            disabled={currentIndex === 0}
                            onClick={() => setCurrentIndex((prev) => prev - 1)}
                            className="px-4 py-2 border rounded disabled:opacity-30"
                        >
                            Previous
                        </button>
                        {currentIndex < questions.length - 1 ? (
                            <button
                                onClick={() => setCurrentIndex((prev) => prev + 1)}
                                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                            >
                                Next
                            </button>
                        ) : (
                            <button
                                onClick={handleSubmit}
                                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                            >
                                Submit
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* 우측 번호판 */}
            <div className="flex justify-center mt-6">
                <div className="grid grid-cols-10 gap-2">
                    {questions.map((_, idx) => (
                        <button
                            key={idx}
                            onClick={() => setCurrentIndex(idx)}
                            className={`w-8 h-8 rounded-full text-sm ${idx === currentIndex
                                    ? "bg-blue-500 text-white"
                                    : answers[idx] !== null
                                        ? "bg-gray-300"
                                        : "bg-white border border-gray-400"
                                }`}
                        >
                            {idx + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
