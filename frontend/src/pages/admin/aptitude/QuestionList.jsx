// src/pages/admin/aptitude/QuestionList.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * ✅ 문항 목록 페이지 (리스트 중심 + 필터/검색/모달 보기 지원)
 * - 검사 유형 필터 (usage_type: aptitude/personality 등)
 * - 검색 (문항명, 텍스트)
 * - 요약 카드 기반 리스트
 * - 모달로 문항 상세 보기
 */
export default function QuestionList() {
    const [questions, setQuestions] = useState([]);
    const [filtered, setFiltered] = useState([]);
    const [selectedQuestion, setSelectedQuestion] = useState(null); // 상세 보기용
    const [examType, setExamType] = useState("all");
    const [search, setSearch] = useState("");
    const [message, setMessage] = useState("");

    // ✅ 문항 목록 로드
    const fetchQuestions = async () => {
        try {
            const res = await axios.get("/api/admin/questions", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setQuestions(res.data);
            setFiltered(res.data);
        } catch {
            setMessage("문항 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchQuestions();
    }, []);

    // ✅ 필터/검색 반영
    useEffect(() => {
        let result = [...questions];

        if (examType !== "all") {
            result = result.filter((q) => q.usage_type === examType);
        }

        if (search.trim() !== "") {
            const keyword = search.toLowerCase();
            result = result.filter(
                (q) =>
                    q.question_name?.toLowerCase().includes(keyword) ||
                    q.question_text?.toLowerCase().includes(keyword) ||
                    q.instruction?.toLowerCase().includes(keyword)
            );
        }

        setFiltered(result);
    }, [examType, search, questions]);

    // ✅ 문항 삭제
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
            fetchQuestions();
        } catch {
            setMessage("삭제 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="w-full px-6 py-10">
            <h1 className="text-2xl font-bold mb-6">문항 목록</h1>

            {/* ✅ 메시지 출력 */}
            {message && <p className="text-blue-600 text-sm mb-4">{message}</p>}

            {/* ✅ 필터/검색 영역 */}
            <div className="flex flex-col md:flex-row md:items-center gap-4 mb-6">
                <select
                    value={examType}
                    onChange={(e) => setExamType(e.target.value)}
                    className="border rounded p-2 w-full md:w-40"
                >
                    <option value="all">전체 검사유형</option>
                    <option value="aptitude">적성검사</option>
                    <option value="personality">인성검사</option>
                    <option value="emotional">정서역량검사</option>
                </select>
                <input
                    type="text"
                    placeholder="문항명, 텍스트 검색"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="border rounded p-2 flex-1"
                />
            </div>

            {/* ✅ 문항 리스트 */}
            <div className="space-y-4">
                {filtered.map((q) => (
                    <div key={q.question_id} className="border p-4 rounded shadow-sm bg-white">
                        <div className="text-sm text-gray-500 mb-1">
                            검사유형: {q.usage_type} | 문항유형: {q.question_type} | 복수정답:{" "}
                            {q.is_multiple_choice ? "O" : "X"}
                        </div>
                        <div className="font-semibold text-base">{q.question_name}</div>
                        <div className="text-sm text-gray-600 truncate">
                            {q.instruction?.slice(0, 100)}
                        </div>
                        <div className="mt-2 flex gap-4 text-sm">
                            <button
                                onClick={() => setSelectedQuestion(q)}
                                className="text-blue-600 hover:underline"
                            >
                                상세 보기
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
                {filtered.length === 0 && (
                    <p className="text-gray-500 text-center">조건에 해당하는 문항이 없습니다.</p>
                )}
            </div>

            {/* ✅ 상세 보기 모달 */}
            {selectedQuestion && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <h2 className="text-xl font-bold mb-4">문항 상세 보기</h2>
                        <p className="mb-1 text-sm text-gray-500">
                            검사유형: {selectedQuestion.usage_type}
                        </p>
                        <p className="font-semibold">{selectedQuestion.question_name}</p>
                        <p className="whitespace-pre-line mb-2">{selectedQuestion.instruction}</p>
                        <p className="whitespace-pre-line mb-4">{selectedQuestion.question_text}</p>
                        <ul className="list-disc list-inside mb-4">
                            {selectedQuestion.options.map((opt, i) => (
                                <li key={i} className={opt.is_correct ? "text-green-600" : ""}>
                                    {opt.option_text}
                                    {opt.is_correct && " (정답)"}
                                </li>
                            ))}
                        </ul>
                        <p className="text-xs text-gray-500">
                            정답 해설: {selectedQuestion.correct_explanation || "없음"}
                        </p>
                        <p className="text-xs text-gray-500 mb-4">
                            오답 해설: {selectedQuestion.wrong_explanation || "없음"}
                        </p>
                        <div className="text-right">
                            <button
                                onClick={() => setSelectedQuestion(null)}
                                className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
                            >
                                닫기
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
