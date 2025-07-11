// src/pages/product.jsx

import React, { useEffect, useState } from "react";
import { useUser } from "../hooks/useUser";
import { motion } from "framer-motion";
import axios from "axios";
import ExamStartModal from "../components/ExamStartModal"; // ✅ 모달 컴포넌트 import

export default function Product() {
    const user = useUser();
    const [tests, setTests] = useState([]);
    const [selectedTestId, setSelectedTestId] = useState(null); // ✅ 선택된 검사 ID
    const [isModalOpen, setIsModalOpen] = useState(false); // ✅ 모달 상태

    useEffect(() => {
        const fetchTests = async () => {
            try {
                const response = await axios.get("/api/tests");
                const publishedTests = response.data.filter((test) => test.is_published);
                setTests(publishedTests);
            } catch (error) {
                console.error("검사 목록을 불러오는 데 실패했습니다:", error);
            }
        };
        fetchTests();
    }, []);

    const handleOpenModal = (testId) => {
        setSelectedTestId(testId);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setSelectedTestId(null);
        setIsModalOpen(false);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans"
        >
            <main className="max-w-4xl mx-auto px-4 py-10">
                <h1 className="text-3xl font-bold text-center mb-10">검사 / 제품 목록</h1>

                {tests.length === 0 ? (
                    <p className="text-center text-gray-500">현재 활성화된 검사가 없습니다.</p>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                        {tests.map((test) => (
                            <div
                                key={test.test_id}
                                className="border rounded-lg p-4 shadow hover:shadow-md transition bg-gray-50 hover:bg-white flex flex-col justify-between"
                            >
                                <div>
                                    <h3 className="text-lg font-semibold mb-1">{test.test_name}</h3>
                                    <p className="text-sm text-gray-600">문항 수: 약 {test.question_count ?? "?"}문항</p>
                                    <p className="text-sm text-gray-600 mb-4">소요 시간: 약 {test.duration_minutes ?? "?"}분</p>
                                </div>
                                <button
                                    onClick={() => handleOpenModal(test.test_id)}
                                    className="mt-auto bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-2 rounded transition"
                                >
                                    시작하기
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {isModalOpen && (
                    <ExamStartModal testId={selectedTestId} onClose={handleCloseModal} />
                )}
            </main>
        </motion.div>
    );
}
