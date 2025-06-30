// src/pages/product/ProductExam.jsx

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

// ✅ 타이머 컴포넌트
function CountdownTimer({ duration, onTimeOver }) {
    const [timeLeft, setTimeLeft] = useState(duration * 60); // 초 단위

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
        <div className="text-sm text-right text-gray-600 mb-2">
            남은 시간: {minutes}:{seconds.toString().padStart(2, "0")}
        </div>
    );
}

export default function ProductExam() {
    const { test_id } = useParams();
    const navigate = useNavigate();

    // ✅ 예시: 모의 문항 목록 (추후 API 대체 예정)
    const questions = [
        {
            question_id: "q1",
            instruction: "다음 문장을 읽고 알맞은 보기를 고르세요.",
            question_text: "나는 매일 아침 일찍 일어난다.",
            options: ["항상 그렇다", "대체로 그렇다", "보통이다", "드물다", "전혀 아니다"],
        },
        {
            question_id: "q2",
            instruction: null,
            question_text: "다른 사람과의 협업을 선호한다.",
            options: ["매우 그렇다", "그렇다", "보통이다", "아니다", "전혀 아니다"],
        },
    ];

    const duration_minutes = 10;
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
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(currentIndex + 1);
        }
    };

    const handleMoveTo = (idx) => {
        setCurrentIndex(idx);
    };

    const handleSubmit = () => {
        console.log("제출할 응답:", answers);
        alert("제출 완료! (응답은 콘솔에 출력됨)");
        // 추후: navigate(`/result/${test_id}`) 등 결과 페이지 이동
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans px-6 py-6"
        >
            <div className="max-w-3xl mx-auto">
                <CountdownTimer duration={duration_minutes} onTimeOver={() => setTimeOver(true)} />

                {/* ✅ 전체 현황판 */}
                <div className="flex gap-2 mb-4 flex-wrap text-sm">
                    {questions.map((q, idx) => (
                        <button
                            key={q.question_id}
                            className={`w-7 h-7 rounded-full border text-xs ${answers[q.question_id] !== undefined
                                    ? "bg-blue-500 text-white"
                                    : "bg-gray-100 text-gray-600"
                                } ${idx === currentIndex ? "ring-2 ring-blue-400" : ""}`}
                            onClick={() => handleMoveTo(idx)}
                        >
                            {idx + 1}
                        </button>
                    ))}
                </div>

                {/* ✅ 문항 출력 */}
                <div className="bg-gray-100 rounded p-6 mb-4 shadow">
                    {current.instruction && (
                        <p className="text-sm text-gray-600 mb-2">{current.instruction}</p>
                    )}
                    <p className="font-medium mb-4">{current.question_text}</p>

                    <ul className="space-y-2">
                        {current.options.map((opt, idx) => (
                            <li
                                key={idx}
                                onClick={() => handleSelect(idx)}
                                className={`border p-3 rounded cursor-pointer transition ${answers[current.question_id] === idx
                                        ? "bg-blue-100 border-blue-500"
                                        : "hover:bg-gray-200"
                                    }`}
                            >
                                <span className="font-semibold mr-2">{idx + 1}.</span>
                                {opt}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* ✅ 문항 이동 / 제출 */}
                <div className="flex justify-between items-center mt-6">
                    <div />
                    {currentIndex < questions.length - 1 ? (
                        <button
                            onClick={handleNext}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 text-sm rounded"
                        >
                            다음 문항
                        </button>
                    ) : (
                        <button
                            onClick={handleSubmit}
                            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 text-sm rounded"
                        >
                            제출하기
                        </button>
                    )}
                </div>
            </div>
        </motion.div>
    );
}
