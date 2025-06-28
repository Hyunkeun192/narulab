import React, { useEffect, useState } from "react";
import axios from "axios";

export default function QuestionViewModal({ testId, onClose }) {
    const [questions, setQuestions] = useState([]);
    const [expandedId, setExpandedId] = useState(null); // 펼쳐진 문항 ID

    // 🔹 검사에 등록된 문항 불러오기
    const fetchQuestions = async () => {
        try {
            const res = await axios.get(`/api/admin/tests/${testId}/questions`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setQuestions(res.data);
        } catch (error) {
            console.error("문항 불러오기 오류:", error);
            alert("문항 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchQuestions();
    }, [testId]);

    // 🔹 문항 펼침/닫기 토글
    const toggleExpand = (questionId) => {
        setExpandedId(prev => (prev === questionId ? null : questionId));
    };

    return (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center justify-center">
            <div className="bg-white rounded-lg w-[700px] max-h-[80vh] overflow-y-auto shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4">문항 확인</h2>

                {questions.length === 0 ? (
                    <p className="text-gray-500 text-sm mb-4">등록된 문항이 없습니다.</p>
                ) : (
                    <ul className="space-y-3">
                        {questions.map((q, index) => (
                            <li key={q.question_id} className="border rounded p-3">
                                <div
                                    className="cursor-pointer flex justify-between items-center"
                                    onClick={() => toggleExpand(q.question_id)}
                                >
                                    <span className="text-sm font-medium">
                                        {index + 1}. {q.question_name || "(문항명 없음)"}
                                    </span>
                                    <span className="text-xs text-blue-500">
                                        {expandedId === q.question_id ? "접기 ▲" : "펼치기 ▼"}
                                    </span>
                                </div>

                                {expandedId === q.question_id && (
                                    <div className="mt-3 space-y-2 text-sm text-gray-700">
                                        {q.instruction && (
                                            <p><strong>지시문:</strong> {q.instruction}</p>
                                        )}
                                        {q.question_text && (
                                            <p><strong>문항:</strong> {q.question_text}</p>
                                        )}
                                        {q.options?.length > 0 && (
                                            <div>
                                                <strong>보기:</strong>
                                                <ul className="list-disc list-inside mt-1">
                                                    {q.options.map((opt, i) => (
                                                        <li key={opt.option_id}>
                                                            {opt.option_text}
                                                            {opt.is_correct && (
                                                                <span className="text-green-600 text-xs ml-2">(정답)</span>
                                                            )}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                )}

                <div className="mt-6 text-right">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-600 text-white rounded text-sm"
                    >
                        닫기
                    </button>
                </div>
            </div>
        </div>
    );
}
