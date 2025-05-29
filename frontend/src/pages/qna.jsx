import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/useUser";
import { motion } from "framer-motion";  // ✅ 추가

export default function QnAPage() {
    const user = useUser();
    const [question, setQuestion] = useState("");
    const [qnaList, setQnaList] = useState([]);

    const fetchQnaList = async () => {
        try {
            const res = await axios.get("/api/qna");
            setQnaList(res.data);
        } catch (err) {
            console.error("QnA 목록 불러오기 실패:", err);
        }
    };

    useEffect(() => {
        fetchQnaList();
    }, []);

    const handleQuestionSubmit = async () => {
        try {
            await axios.post("/api/qna", { question });
            setQuestion("");
            fetchQnaList();
        } catch (err) {
            console.error("질문 등록 실패:", err);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans"
        >

            {/* ✅ 본문 영역 */}
            <main className="max-w-3xl mx-auto py-10 px-4">
                <h1 className="text-3xl font-bold text-center mb-6">QnA</h1>

                {user && (
                    <div className="mb-8">
                        <textarea
                            className="w-full border p-3 rounded mb-2"
                            rows={4}
                            placeholder="궁금한 점을 입력하세요"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                        />
                        <button
                            onClick={handleQuestionSubmit}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            질문 등록
                        </button>
                    </div>
                )}

                <ul className="space-y-4">
                    {qnaList.map((qna) => (
                        <li key={qna.id} className="border p-4 rounded shadow-sm">
                            <p className="text-gray-900 font-medium whitespace-pre-line">{qna.question}</p>
                            {qna.answer && (
                                <div className="mt-2 bg-gray-100 p-3 rounded text-sm text-gray-700">
                                    <strong>답변:</strong> {qna.answer}
                                </div>
                            )}
                        </li>
                    ))}
                </ul>
            </main>
        </motion.div>
    );
}
