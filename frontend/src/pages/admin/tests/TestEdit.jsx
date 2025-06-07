// src/pages/admin/tests/TestEdit.jsx

import React, { useEffect, useState } from "react";
// ✅ 기존 axios 제거하고 testApi 함수 import
import {
    getTestById,
    updateTest,
    assignQuestionsToTest,
} from "../../../api/admin/testApi";
import { useParams, useNavigate } from "react-router-dom";

// ✅ 검사 상세 보기 및 수정 페이지
export default function TestEdit() {
    const { testId } = useParams();
    const navigate = useNavigate();

    const [test, setTest] = useState(null); // ✅ 검사 정보
    const [questions, setQuestions] = useState([]); // ✅ 연결된 문항
    const [allQuestions, setAllQuestions] = useState([]); // ✅ 전체 문항
    const [selectedToAdd, setSelectedToAdd] = useState([]); // ✅ 새로 추가할 문항 ID들
    const [message, setMessage] = useState("");

    // ✅ 검사 정보 및 연결된 문항 불러오기
    const fetchTestDetails = async () => {
        try {
            const data = await getTestById(testId); // ✅ axios → getTestById 사용
            setTest(data.test);
            setQuestions(data.questions);
        } catch {
            setMessage("검사 정보를 불러오지 못했습니다.");
        }
    };

    // ✅ 전체 문항 목록 불러오기 (이 부분은 아직 fetch 사용)
    const fetchAllQuestions = async () => {
        try {
            const res = await fetch("/api/admin/questions", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            const data = await res.json();
            setAllQuestions(data);
        } catch {
            setMessage("문항 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchTestDetails();
        fetchAllQuestions();
    }, [testId]);

    // ✅ 검사 정보 저장 (수정)
    const handleSave = async () => {
        try {
            await updateTest(testId, {
                test_name: test.test_name,
                test_type: test.test_type,
            }); // ✅ updateTest 사용
            setMessage("검사 정보가 수정되었습니다.");
        } catch {
            setMessage("저장 중 오류 발생.");
        }
    };

    // ✅ 문항 제거 (axios 직접 사용 그대로 유지 – testApi에 정의되지 않음)
    const handleRemoveQuestion = async (questionId) => {
        try {
            await fetch(`/api/admin/tests/${testId}/questions/${questionId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setMessage("문항이 제거되었습니다.");
            fetchTestDetails();
        } catch {
            setMessage("문항 제거 실패.");
        }
    };

    // ✅ 문항 추가 연결
    const handleAddQuestions = async () => {
        if (selectedToAdd.length === 0) {
            setMessage("추가할 문항을 선택해주세요.");
            return;
        }

        try {
            await assignQuestionsToTest(testId, selectedToAdd); // ✅ assignQuestionsToTest 사용
            setMessage("문항이 추가되었습니다.");
            setSelectedToAdd([]);
            fetchTestDetails();
        } catch {
            setMessage("문항 추가 실패.");
        }
    };

    if (!test) return <div className="p-10">로딩 중...</div>;

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사 상세 수정</h1>

            {message && <p className="text-blue-600 text-sm mb-4">{message}</p>}

            {/* ✅ 검사 정보 수정 UI */}
            <div className="mb-8 space-y-3">
                <div>
                    <label className="block text-sm font-medium mb-1">검사명</label>
                    <input
                        className="w-full border p-2 rounded"
                        value={test.test_name}
                        onChange={(e) => setTest({ ...test, test_name: e.target.value })}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">검사 유형</label>
                    <select
                        className="w-full border p-2 rounded"
                        value={test.test_type}
                        onChange={(e) => setTest({ ...test, test_type: e.target.value })}
                    >
                        <option value="aptitude">적성검사</option>
                        <option value="personality">인성검사</option>
                    </select>
                </div>
                <button
                    onClick={handleSave}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                >
                    저장
                </button>
            </div>

            {/* ✅ 연결된 문항 목록 */}
            <div className="mb-10">
                <h2 className="text-lg font-semibold mb-3">연결된 문항</h2>
                {questions.length === 0 ? (
                    <p className="text-gray-500">연결된 문항이 없습니다.</p>
                ) : (
                    <ul className="space-y-2">
                        {questions.map((q) => (
                            <li
                                key={q.question_id}
                                className="border rounded p-3 bg-white shadow-sm flex justify-between items-center"
                            >
                                <span>{q.question_text}</span>
                                <button
                                    onClick={() => handleRemoveQuestion(q.question_id)}
                                    className="text-red-500 text-sm hover:underline"
                                >
                                    제거
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* ✅ 문항 추가 영역 */}
            <div>
                <h2 className="text-lg font-semibold mb-3">문항 추가</h2>
                <div className="border p-4 rounded bg-gray-50 max-h-64 overflow-y-auto mb-4 space-y-2">
                    {allQuestions.map((q) => (
                        <label key={q.question_id} className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={selectedToAdd.includes(q.question_id)}
                                onChange={(e) => {
                                    const updated = e.target.checked
                                        ? [...selectedToAdd, q.question_id]
                                        : selectedToAdd.filter((id) => id !== q.question_id);
                                    setSelectedToAdd(updated);
                                }}
                            />
                            <span>{q.question_text}</span>
                        </label>
                    ))}
                </div>
                <button
                    onClick={handleAddQuestions}
                    className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
                >
                    선택한 문항 추가
                </button>
            </div>
        </div>
    );
}
