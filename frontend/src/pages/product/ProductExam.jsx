// src/pages/ProductExam.jsx

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";

// ⏱️ 상단 타이머 컴포넌트
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
                남은 시간: {minutes}:{seconds.toString().padStart(2, "0")}
            </div>
        </div>
    );
}

export default function ProductExam() {
    const { test_id } = useParams();
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [currentIndex, setCurrentIndex] = useState(0);
    const [timeOver, setTimeOver] = useState(false);
    const duration_minutes = 25;

    const current = questions[currentIndex];

    // ✅ API로 문항 불러오기
    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const res = await fetch(`/api/tests/${test_id}/questions-public`);
                const data = await res.json();
                setQuestions(data.questions || []);
            } catch (err) {
                console.error("문항 불러오기 실패:", err);
            }
        };
        fetchQuestions();
    }, [test_id]);

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
        alert("검사 완료!\n총 문항 수: " + questions.length);
    };

    if (!current) return <div className="text-center mt-10">문항을 불러오는 중입니다...</div>;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="fixed inset-0 bg-white z-50 overflow-y-auto px-6 py-6"
        >
            <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-[3fr_1fr] gap-6">
                {/* ✅ 좌측: 문항 영역 */}
                <div>
                    <CountdownTimer duration={duration_minutes} onTimeOver={() => setTimeOver(true)} />

                    <p className="text-lg font-semibold mb-2">
                        문항 {currentIndex + 1} / {questions.length}
                    </p>

                    {/* 지시문 영역 */}
                    {current.instruction && (
                        <div className="bg-blue-50 border border-blue-300 text-blue-700 text-sm rounded p-3 mb-3">
                            {current.instruction}
                        </div>
                    )}

                    <p className="text-xl font-medium mb-6">{current.question_text}</p>

                    {/* 선택지 영역 */}
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

                    {/* 네비게이션 버튼 */}
                    <div className="flex justify-between mt-10">
                        <button
                            onClick={handlePrev}
                            disabled={currentIndex === 0}
                            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded disabled:opacity-50"
                        >
                            이전
                        </button>
                        {currentIndex < questions.length - 1 ? (
                            <button
                                onClick={handleNext}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                            >
                                다음
                            </button>
                        ) : (
                            <button
                                onClick={handleSubmit}
                                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
                            >
                                제출
                            </button>
                        )}
                    </div>
                </div>

                {/* ✅ 우측: 전체 현황판 */}
                <div className="bg-gray-50 border border-gray-200 p-4 rounded shadow-sm text-sm">
                    <h3 className="font-semibold text-gray-700 mb-2">문항 목록</h3>
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

                    {/* 범례 */}
                    <div className="space-y-1 text-xs text-gray-600">
                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded bg-blue-600" /> 현재
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded bg-blue-100" /> 응답 완료
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-4 h-4 rounded border border-gray-300 bg-white" /> 미응답
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
