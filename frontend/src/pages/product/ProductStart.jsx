// src/pages/product/ProductStart.jsx

import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function ProductStart() {
    const { test_id } = useParams(); // URL에서 검사 ID 추출
    const navigate = useNavigate();

    const handleStartExample = () => {
        navigate(`/product/${test_id}/example`);
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
                <h1 className="text-2xl font-bold mb-6">검사 유의사항 안내</h1>

                <div className="bg-gray-100 rounded-lg p-6 text-sm leading-relaxed text-gray-800 shadow">
                    <ul className="list-disc pl-6 space-y-2">
                        <li>이 검사는 정확한 분석을 위해 솔직하게 응답해 주세요.</li>
                        <li>검사 시간은 제한되어 있으며, 타이머가 함께 제공됩니다.</li>
                        <li>검사 도중에는 페이지를 벗어나지 말아 주세요.</li>
                        <li>문항은 순차적으로 한 개씩 보여지며, 이전 문항으로는 돌아갈 수 없습니다.</li>
                        <li>검사 도중 인터넷 연결이 끊기면 결과가 저장되지 않을 수 있습니다.</li>
                        <li>준비가 되면 예제 문항을 통해 방식을 확인하실 수 있습니다.</li>
                    </ul>
                </div>

                <div className="mt-10 text-center">
                    <button
                        onClick={handleStartExample}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded transition text-sm"
                    >
                        예제 문제 풀기
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
