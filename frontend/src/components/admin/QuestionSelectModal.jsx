import React, { useEffect, useState } from "react";
import axios from "axios";

const QuestionSelectModal = ({ isOpen, onClose, onConfirm }) => {
    const [questions, setQuestions] = useState([]);
    const [selectedQuestions, setSelectedQuestions] = useState([]);
    const [search, setSearch] = useState("");
    const [previewQuestion, setPreviewQuestion] = useState(null); // ✅ 문항 미리보기
    const [usageList, setUsageList] = useState([]); // ✅ 사용 검사 리스트
    const [showUsageModal, setShowUsageModal] = useState(false); // ✅ 사용 현황 모달 열림 여부
    const [loadingUsage, setLoadingUsage] = useState(false); // ✅ 로딩 상태

    // ✅ 문항 미리보기
    const handlePreview = async (questionId) => {
        try {
            const res = await axios.get(`/api/admin/questions/detail/${questionId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setPreviewQuestion(res.data);
        } catch (err) {
            console.error("미리보기 문항 불러오기 실패", err);
        }
    };

    // ✅ 사용 현황 불러오기
    const handleUsage = async (questionId) => {
        setShowUsageModal(true);
        setLoadingUsage(true);
        try {
            const res = await axios.get(`/api/admin/questions/${questionId}/used-in-tests`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setUsageList(res.data);
        } catch (err) {
            console.error("사용 현황 불러오기 실패", err);
            setUsageList([]);
        } finally {
            setLoadingUsage(false);
        }
    };

    useEffect(() => {
        if (isOpen) {
            axios
                .get("/api/admin/questions", {
                    params: {
                        usage_type: "aptitude",
                        status: "approved",
                    },
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                })
                .then((res) => {
                    setQuestions(res.data);
                })
                .catch((err) => {
                    console.error("문항 불러오기 오류", err);
                });
        }
    }, [isOpen]);

    const handleAdd = (question) => {
        if (selectedQuestions.find((q) => q.question_id === question.question_id)) return;
        if (selectedQuestions.length >= 30) {
            alert("최대 30문항까지 선택 가능합니다.");
            return;
        }
        setSelectedQuestions((prev) => [...prev, question]);
    };

    const handleRemove = (questionId) => {
        setSelectedQuestions((prev) => prev.filter((q) => q.question_id !== questionId));
    };

    const handleConfirm = () => {
        const orderedIds = selectedQuestions.map((q) => q.question_id);
        onConfirm(orderedIds);
        setSelectedQuestions([]);
    };

    const filtered = questions.filter((q) =>
        q.question_name.toLowerCase().includes(search.toLowerCase())
    );

    if (!isOpen) return null;

    return (
        <>
            {/* ✅ 메인 선택 모달 */}
            <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                <div className="bg-white w-[1000px] h-[600px] rounded-xl p-6 shadow-lg flex flex-col">
                    <h2 className="text-xl font-semibold mb-4">문항 선택</h2>

                    <div className="flex flex-1 gap-6 overflow-hidden">
                        {/* 좌측: 전체 문항 리스트 */}
                        <div className="w-1/2 flex flex-col border rounded overflow-hidden">
                            <div className="p-2 border-b">
                                <input
                                    type="text"
                                    placeholder="문항명 검색"
                                    className="w-full border rounded px-2 py-1 text-sm"
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                />
                            </div>
                            <div className="flex-1 overflow-y-auto p-2">
                                <ul className="space-y-2">
                                    {filtered.map((q) => (
                                        <li
                                            key={q.question_id}
                                            className="flex items-center justify-between bg-gray-50 hover:bg-gray-100 border px-2 py-1 rounded"
                                        >
                                            <span className="text-sm truncate">{q.question_name}</span>
                                            <div className="space-x-2">
                                                <button
                                                    className="text-xs text-purple-600 hover:underline"
                                                    onClick={() => handleUsage(q.question_id)}
                                                >
                                                    사용 현황
                                                </button>
                                                <button
                                                    className="text-xs text-gray-700 hover:underline"
                                                    onClick={() => handlePreview(q.question_id)}
                                                >
                                                    보기
                                                </button>
                                                <button
                                                    className="text-xs text-blue-600 hover:underline"
                                                    onClick={() => handleAdd(q)}
                                                >
                                                    추가
                                                </button>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        {/* 우측: 선택된 문항 리스트 */}
                        <div className="w-1/2 flex flex-col border rounded overflow-hidden">
                            <div className="p-2 border-b text-sm font-medium">
                                선택된 문항 ({selectedQuestions.length} / 30)
                            </div>
                            <div className="flex-1 overflow-y-auto p-2">
                                <ul className="space-y-2">
                                    {selectedQuestions.map((q, idx) => (
                                        <li
                                            key={q.question_id}
                                            className="flex items-center justify-between bg-white border px-2 py-1 rounded"
                                        >
                                            <span className="text-sm">
                                                {idx + 1}. {q.question_name}
                                            </span>
                                            <button
                                                className="text-xs text-red-500 hover:underline"
                                                onClick={() => handleRemove(q.question_id)}
                                            >
                                                제거
                                            </button>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

                    {/* 하단 버튼 영역 */}
                    <div className="flex justify-end mt-4 gap-2">
                        <button
                            onClick={onClose}
                            className="px-4 py-1 text-sm bg-gray-300 rounded hover:bg-gray-400"
                        >
                            닫기
                        </button>
                        <button
                            onClick={handleConfirm}
                            className="px-4 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            선택 완료
                        </button>
                    </div>
                </div>
            </div>

            {/* ✅ 문항 보기 모달 */}
            {previewQuestion && (
                <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-[999]">
                    <div className="bg-white w-[600px] max-h-[80vh] overflow-y-auto rounded-2xl shadow-xl p-6">
                        <h3 className="text-lg font-semibold mb-2">문항 보기</h3>
                        <p className="text-sm text-gray-600 mb-1">
                            <strong>문항명:</strong> {previewQuestion.question_name}
                        </p>
                        <p className="text-sm text-gray-600 mb-1 whitespace-pre-wrap">
                            <strong>지시문:</strong> {previewQuestion.instruction || "-"}
                        </p>
                        <p className="text-sm text-gray-600 mb-2 whitespace-pre-wrap">
                            <strong>본문:</strong> {previewQuestion.question_text}
                        </p>
                        <p className="text-sm text-gray-600 mb-2">
                            <strong>선택지:</strong>
                        </p>
                        <ul className="list-decimal list-inside text-sm pl-4 space-y-1">
                            {previewQuestion.options?.map((opt, idx) => (
                                <li key={idx}>
                                    {(typeof opt.option_order === "number" ? opt.option_order + 1 : idx + 1)}. {opt.option_text}
                                </li>
                            ))}
                        </ul>
                        <div className="text-right mt-4">
                            <button
                                onClick={() => setPreviewQuestion(null)}
                                className="px-4 py-1 text-sm bg-gray-300 rounded hover:bg-gray-400 transition"
                            >
                                닫기
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ✅ 사용 현황 모달 */}
            {showUsageModal && (
                <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-[999]">
                    <div className="bg-white w-[400px] max-h-[60vh] overflow-y-auto rounded-xl p-5 shadow-xl">
                        <h3 className="text-lg font-semibold mb-3">사용 중인 검사</h3>
                        {loadingUsage ? (
                            <p className="text-sm text-gray-500">불러오는 중...</p>
                        ) : usageList.length === 0 ? (
                            <p className="text-sm text-gray-500">아직 어떤 검사에도 사용되지 않았습니다.</p>
                        ) : (
                            <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                {usageList.map((name, idx) => (
                                    <li key={idx}>{name}</li>
                                ))}
                            </ul>
                        )}
                        <div className="text-right mt-4">
                            <button
                                onClick={() => setShowUsageModal(false)}
                                className="px-4 py-1 text-sm bg-gray-500 text-white rounded"
                            >
                                닫기
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default QuestionSelectModal;
