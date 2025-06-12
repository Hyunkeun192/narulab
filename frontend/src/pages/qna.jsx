import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/useUser";
import { motion } from "framer-motion"; // ✅ 페이지 전환 애니메이션용

export default function QnAPage() {
    const user = useUser();

    // ✅ 사용자 상태 정의
    const isLoggedIn = !!user?.id;
    const isSuperAdmin = !!user?.is_super_admin;
    const isContentAdmin = !!user?.is_content_admin;
    const isAdmin = isSuperAdmin || isContentAdmin;

    // ✅ 질문 및 목록 상태 정의
    const [question, setQuestion] = useState("");
    const [isPrivate, setIsPrivate] = useState(false); // 공개 여부 상태
    const [qnaList, setQnaList] = useState([]);

    // ✅ QnA 목록 불러오기
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

    // ✅ 질문 등록
    const handleQuestionSubmit = async () => {
        try {
            await axios.post("/api/qna", {
                question,
                is_private: isPrivate,
            });
            setQuestion("");
            setIsPrivate(false);
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
            {/* ✅ 페이지 타이틀 */}
            <main className="max-w-3xl mx-auto py-10 px-4">
                <h1 className="text-3xl font-bold text-center mb-6">QnA</h1>

                {/* ✅ 일반 사용자만 질문 등록 가능 */}
                {isLoggedIn && !isAdmin && (
                    <div className="mb-8">
                        <textarea
                            className="w-full border p-3 rounded mb-2"
                            rows={4}
                            placeholder="궁금한 점을 입력하세요"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                        />
                        <div className="flex justify-between items-center mb-2">
                            <label className="text-sm">
                                <input
                                    type="checkbox"
                                    checked={isPrivate}
                                    onChange={(e) => setIsPrivate(e.target.checked)}
                                    className="mr-2"
                                />
                                비공개로 등록하기
                            </label>
                            <button
                                onClick={handleQuestionSubmit}
                                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                            >
                                질문 등록
                            </button>
                        </div>
                    </div>
                )}

                {/* ✅ 질문 목록 */}
                <ul className="space-y-4">
                    {qnaList.map((qna) => {
                        const canView = !qna.is_private || (qna.is_private && isAdmin);

                        return canView ? (
                            <li key={qna.id} className="border p-4 rounded shadow-sm">
                                <p className="text-gray-900 font-medium whitespace-pre-line">{qna.question}</p>

                                {/* ✅ 답변 표시 */}
                                {qna.answer && (
                                    <div className="mt-2 bg-gray-100 p-3 rounded text-sm text-gray-700">
                                        <strong>답변:</strong> {qna.answer}
                                    </div>
                                )}

                                {/* ✅ 답글 작성은 관리자만 */}
                                {!qna.answer && isAdmin && (
                                    <div className="mt-4">
                                        <textarea
                                            placeholder="답변을 입력하세요..."
                                            className="w-full border rounded p-2 mb-2"
                                        />
                                        <button className="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700">
                                            답변 등록
                                        </button>
                                    </div>
                                )}
                            </li>
                        ) : null;
                    })}
                </ul>
            </main>
        </motion.div>
    );
}
