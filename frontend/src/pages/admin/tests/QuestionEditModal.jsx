import React, { useEffect, useState } from "react";
import axios from "axios";
import QuestionSelectModal from "../../../components/admin/QuestionSelectModal"; // 문항 선택용 모달 재사용

export default function QuestionEditModal({ testId, onClose }) {
    const [linkedQuestions, setLinkedQuestions] = useState([]);
    const [showSelectModal, setShowSelectModal] = useState(false);

    // 🔹 현재 연결된 문항 불러오기
    const fetchLinkedQuestions = async () => {
        try {
            const res = await axios.get(`/api/admin/tests/${testId}/questions`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setLinkedQuestions(res.data);
        } catch (error) {
            console.error("문항 불러오기 오류:", error);
            alert("문항 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchLinkedQuestions();
    }, [testId]);

    // 🔹 문항 삭제
    const handleRemove = (questionId) => {
        const updated = linkedQuestions.filter(q => q.question_id !== questionId);
        setLinkedQuestions(updated);
    };

    // 🔹 추가로 문항 선택 후 합치기
    const handleAddQuestions = (selectedIds) => {
        const currentIds = linkedQuestions.map(q => q.question_id);
        const newOnes = selectedIds
            .filter(id => !currentIds.includes(id))
            .map(id => ({ question_id: id }));
        setLinkedQuestions([...linkedQuestions, ...newOnes]);
        setShowSelectModal(false);
    };

    // 🔹 저장: 전체 문항 리스트를 bulk link
    const handleSave = async () => {
        try {
            await axios.post(
                `/api/admin/tests/${testId}/questions`,
                { question_ids: linkedQuestions.map(q => q.question_id) },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            alert("✅ 문항 구성이 수정되었습니다.");
            onClose();
        } catch (error) {
            console.error("저장 오류:", error);
            alert("문항 구성 저장 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center justify-center">
            <div className="bg-white rounded-lg w-[600px] max-h-[80vh] overflow-y-auto shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4">문항 수정</h2>

                {/* 🔸 등록된 문항 리스트 */}
                {linkedQuestions.length === 0 ? (
                    <p className="text-gray-500 text-sm mb-4">등록된 문항이 없습니다.</p>
                ) : (
                    <ul className="mb-4 space-y-2">
                        {linkedQuestions.map((q, index) => (
                            <li key={q.question_id} className="flex justify-between items-center border p-2 rounded">
                                <span className="text-sm">{index + 1}. {q.question_name || "(문항명 없음)"}</span>
                                <button
                                    onClick={() => handleRemove(q.question_id)}
                                    className="text-red-500 text-xs hover:underline"
                                >
                                    ❌ 삭제
                                </button>
                            </li>
                        ))}
                    </ul>
                )}

                <div className="flex justify-between mt-4">
                    <button
                        onClick={() => setShowSelectModal(true)}
                        className="text-blue-500 text-sm hover:underline"
                    >
                        + 문항 추가하기
                    </button>

                    <div className="space-x-2">
                        <button
                            onClick={onClose}
                            className="px-4 py-1 border rounded text-sm"
                        >
                            닫기
                        </button>
                        <button
                            onClick={handleSave}
                            className="px-4 py-1 bg-blue-600 text-white rounded text-sm"
                        >
                            저장
                        </button>
                    </div>
                </div>

                {/* 🔹 문항 선택 모달 */}
                {showSelectModal && (
                    <QuestionSelectModal
                        isOpen={showSelectModal}
                        onClose={() => setShowSelectModal(false)}
                        onConfirm={handleAddQuestions}
                    />
                )}
            </div>
        </div>
    );
}
