// src/pages/product/ProductExample.jsx

import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function ProductExample() {
    const { test_id } = useParams();
    const navigate = useNavigate();

    // ✅ 예제 문항 데이터 (하드코딩)
    const exampleQuestion = {
        question_text: "다음 중 언어의 의미가 가장 유사한 단어는?",
        options: [
            "풍부하다", // 정답
            "거칠다",
            "좁다",
            "불안하다",
            "늦다"
        ],
        correct_index: 0,
        explanation: "‘풍부하다’는 양이 많고 넉넉하다는 뜻으로, 다른 보기들과는 의미가 가장 다릅니다."
    };

    const [selected, setSelected] = useState(null);
    const [showExplanation, setShowExplanation] = useState(false);

    const handleSelect = (index) => {
        setSelected(index);
        setShowExplanation(true);
    };

    const handleStartExam = () => {
        navigate(`/product/${test_id}/exam`);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans px-6 py-10"
        >
            <div className="max-w-3xl mx-auto">
                <h2 className="text-xl font-bold mb-6">예제 문항</h2>

                <div className="bg-gray-100 rounded-lg p-6 mb-6 shadow">
                    <p className="text-base mb-4">{exampleQuestion.question_text}</p>
                    <ul className="space-y-2">
                        {exampleQuestion.options.map((option, idx) => (
                            <li
                                key={idx}
                                onClick={() => handleSelect(idx)}
                                className={`border p-3 rounded cursor-pointer transition ${selected === idx
                                        ? "bg-blue-100 border-blue-500"
                                        : "hover:bg-gray-200"
                                    }`}
                            >
                                <span className="font-semibold mr-2">{idx + 1}.</span>
                                {option}
                            </li>
                        ))}
                    </ul>
                </div>

                {showExplanation && (
                    <div className="bg-green-100 border border-green-300 text-green-800 p-4 rounded mb-6">
                        <p className="font-semibold">정답 해설</p>
                        <p className="text-sm mt-1">{exampleQuestion.explanation}</p>
                    </div>
                )}

                <div className="text-center">
                    <button
                        onClick={handleStartExam}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded transition text-sm"
                    >
                        본검사 시작하기
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
