// src/pages/admin/aptitude/QuestionList.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 문항 목록 및 수정/삭제 기능 제공 페이지
export default function QuestionList() {
    const [questions, setQuestions] = useState([]); // ✅ 전체 문항 리스트
    const [selectedQuestion, setSelectedQuestion] = useState(null); // ✅ 수정 중인 문항
    const [message, setMessage] = useState("");

    // ✅ 전체 문항 목록 로드
    const fetchQuestions = async () => {
        try {
            const res = await axios.get("/api/admin/questions", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setQuestions(res.data);
        } catch {
            setMessage("문항 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchQuestions();
    }, []);

    // ✅ 문항 삭제 요청
    const handleDelete = async (id) => {
        const confirm = window.confirm("정말 이 문항을 삭제하시겠습니까?");
        if (!confirm) return;

        try {
            await axios.delete(`/api/admin/questions/${id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setMessage("문항이 삭제되었습니다.");
            fetchQuestions(); // 목록 새로고침
        } catch {
            setMessage("삭제 중 오류가 발생했습니다.");
        }
    };

    // ✅ 수정 모드 진입
    const handleEdit = (question) => {
        setSelectedQuestion({ ...question }); // 깊은 복사
    };

    // ✅ 수정 항목 변경 핸들러 (선택지용)
    const updateOption = (index, key, value) => {
        const updated = { ...selectedQuestion };
        updated.options[index][key] = value;
        setSelectedQuestion(updated);
    };

    // ✅ 수정 항목 변경 핸들러 (문항 자체 정보용)
    const updateQuestionField = (key, value) => {
        setSelectedQuestion({ ...selectedQuestion, [key]: value });
    };

    // ✅ 수정 저장
    const handleSave = async () => {
        try {
            await axios.put(
                `/api/admin/questions/${selectedQuestion.question_id}`,
                {
                    question_text: selectedQuestion.question_text,
                    question_type: selectedQuestion.question_type,
                    is_multiple_choice: selectedQuestion.is_multiple_choice,
                    options: selectedQuestion.options,
                    instruction: selectedQuestion.instruction, // ✅ 추가: 지시문
                    question_name: selectedQuestion.question_name, // ✅ 추가: 문항 이름
                    correct_explanation: selectedQuestion.correct_explanation, // ✅ 추가: 정답 해설
                    wrong_explanation: selectedQuestion.wrong_explanation, // ✅ 추가: 오답 해설
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            setMessage("문항이 수정되었습니다.");
            setSelectedQuestion(null);
            fetchQuestions();
        } catch {
            setMessage("수정 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">적성검사 문항 목록</h1>

            {/* ✅ 메시지 출력 */}
            {message && <p className="text-blue-600 text-sm mb-4">{message}</p>}

            {/* ✅ 수정 모드 */}
            {selectedQuestion && (
                <div className="border p-4 rounded mb-6 bg-gray-50">
                    <h2 className="font-semibold mb-2">문항 수정</h2>

                    {/* ✅ 문항 이름 */}
                    <input
                        value={selectedQuestion.question_name || ""}
                        onChange={(e) => updateQuestionField("question_name", e.target.value)}
                        className="w-full border rounded p-2 mb-2"
                        placeholder="문항 이름 (예: 중심 내용 파악)"
                    />

                    {/* ✅ 지시문 */}
                    <textarea
                        value={selectedQuestion.instruction || ""}
                        onChange={(e) => updateQuestionField("instruction", e.target.value)}
                        className="w-full border rounded p-2 mb-2"
                        rows={2}
                        placeholder="지시문 입력"
                    />

                    {/* ✅ 문항 텍스트 */}
                    <textarea
                        value={selectedQuestion.question_text}
                        onChange={(e) => updateQuestionField("question_text", e.target.value)}
                        className="w-full border rounded p-2 mb-2"
                        rows={2}
                        placeholder="문항 텍스트 입력"
                    />

                    {/* ✅ 선택지 수정 */}
                    <div className="mb-2 space-y-2">
                        {selectedQuestion.options.map((opt, index) => (
                            <div key={index} className="flex items-center gap-2">
                                <input
                                    type="text"
                                    value={opt.option_text}
                                    onChange={(e) =>
                                        updateOption(index, "option_text", e.target.value)
                                    }
                                    className="flex-1 border p-2 rounded"
                                />
                                <label className="flex items-center text-sm">
                                    <input
                                        type="checkbox"
                                        checked={opt.is_correct}
                                        onChange={(e) =>
                                            updateOption(index, "is_correct", e.target.checked)
                                        }
                                        className="mr-1"
                                    />
                                    정답
                                </label>
                            </div>
                        ))}
                    </div>

                    {/* ✅ 해설 입력 */}
                    <textarea
                        value={selectedQuestion.correct_explanation || ""}
                        onChange={(e) =>
                            updateQuestionField("correct_explanation", e.target.value)
                        }
                        className="w-full border rounded p-2 mt-2"
                        rows={2}
                        placeholder="정답 해설 입력"
                    />
                    <textarea
                        value={selectedQuestion.wrong_explanation || ""}
                        onChange={(e) =>
                            updateQuestionField("wrong_explanation", e.target.value)
                        }
                        className="w-full border rounded p-2 mt-2"
                        rows={2}
                        placeholder="오답 해설 입력"
                    />

                    {/* ✅ 저장/취소 버튼 */}
                    <div className="mt-3 flex gap-3">
                        <button
                            onClick={handleSave}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                        >
                            저장
                        </button>
                        <button
                            onClick={() => setSelectedQuestion(null)}
                            className="text-gray-600 hover:underline"
                        >
                            취소
                        </button>
                    </div>
                </div>
            )}

            {/* ✅ 문항 리스트 */}
            <div className="space-y-6">
                {questions.map((q) => (
                    <div key={q.question_id} className="border p-4 rounded shadow-sm bg-white">
                        <div className="text-gray-600 text-sm mb-1">
                            {q.question_name} ({q.question_type})
                        </div>
                        <div className="font-medium mb-1 whitespace-pre-line">
                            {q.instruction}
                        </div>
                        <div className="mb-2 whitespace-pre-line">
                            {q.question_text}
                        </div>
                        <ul className="list-disc list-inside mb-2">
                            {q.options.map((opt, i) => (
                                <li key={i} className={opt.is_correct ? "text-green-600" : ""}>
                                    {opt.option_text}
                                    {opt.is_correct && " (정답)"}
                                </li>
                            ))}
                        </ul>
                        <div className="text-xs text-gray-500 mb-1">
                            정답 해설: {q.correct_explanation || "없음"}
                        </div>
                        <div className="text-xs text-gray-500 mb-2">
                            오답 해설: {q.wrong_explanation || "없음"}
                        </div>
                        <div className="flex gap-4 text-sm">
                            <button
                                onClick={() => handleEdit(q)}
                                className="text-blue-600 hover:underline"
                            >
                                수정
                            </button>
                            <button
                                onClick={() => handleDelete(q.question_id)}
                                className="text-red-500 hover:underline"
                            >
                                삭제
                            </button>
                        </div>
                    </div>
                ))}
                {questions.length === 0 && (
                    <p className="text-gray-500 text-center">등록된 문항이 없습니다.</p>
                )}
            </div>
        </div>
    );
}
