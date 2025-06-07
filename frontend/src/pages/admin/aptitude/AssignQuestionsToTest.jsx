// src/pages/admin/aptitude/AssignQuestionsToTest.jsx

import React, { useEffect, useState } from "react";
// ✅ 기존 axios 제거, testApi.js의 함수 사용
import { getTests, assignQuestionsToTest } from "../../../api/admin/testApi";

// ✅ 문항을 검사에 연결하는 관리자 전용 페이지
export default function AssignQuestionsToTest() {
    const [tests, setTests] = useState([]); // ✅ 전체 검사 목록 상태
    const [questions, setQuestions] = useState([]); // ✅ 전체 문항 목록 상태
    const [selectedTestId, setSelectedTestId] = useState(""); // ✅ 선택된 검사 ID
    const [selectedQuestionIds, setSelectedQuestionIds] = useState([]); // ✅ 선택된 문항 ID 배열
    const [message, setMessage] = useState(""); // ✅ 사용자 피드백 메시지

    // ✅ 검사 목록 가져오기 (최초 렌더링 시)
    useEffect(() => {
        const fetchTests = async () => {
            try {
                const data = await getTests(); // ✅ axios → testApi 함수 사용
                setTests(data);
            } catch {
                setMessage("검사 목록을 불러오지 못했습니다.");
            }
        };
        fetchTests();
    }, []);

    // ✅ 문항 목록 가져오기 (testApi.js에 없으므로 fetch 유지)
    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const res = await fetch("/api/admin/questions", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                });
                const data = await res.json();
                setQuestions(data);
            } catch {
                setMessage("문항 목록을 불러오지 못했습니다.");
            }
        };
        fetchQuestions();
    }, []);

    // ✅ 문항 체크박스 선택 토글 핸들러
    const toggleQuestion = (questionId) => {
        setSelectedQuestionIds((prev) =>
            prev.includes(questionId)
                ? prev.filter((id) => id !== questionId)
                : [...prev, questionId]
        );
    };

    // ✅ 선택한 문항들을 선택된 검사에 연결
    const handleAssign = async () => {
        if (!selectedTestId || selectedQuestionIds.length === 0) {
            setMessage("검사와 문항을 모두 선택해주세요.");
            return;
        }

        try {
            await assignQuestionsToTest(selectedTestId, selectedQuestionIds); // ✅ axios → testApi 함수 사용
            setMessage("문항이 검사에 성공적으로 연결되었습니다.");
        } catch {
            setMessage("문항 연결 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">문항을 검사에 연결</h1>

            {/* ✅ 검사 선택 드롭다운 */}
            <div className="mb-6">
                <label className="block text-sm font-medium mb-2">검사 선택</label>
                <select
                    className="w-full border p-2 rounded"
                    value={selectedTestId}
                    onChange={(e) => setSelectedTestId(e.target.value)}
                >
                    <option value="">검사를 선택하세요</option>
                    {tests.map((test) => (
                        <option key={test.test_id} value={test.test_id}>
                            {test.test_name} ({test.test_type})
                        </option>
                    ))}
                </select>
            </div>

            {/* ✅ 문항 선택 리스트 */}
            <div className="mb-6">
                <label className="block text-sm font-medium mb-2">문항 선택</label>
                <div className="space-y-2 max-h-64 overflow-y-auto border p-3 rounded">
                    {questions.map((q) => (
                        <label key={q.question_id} className="flex items-start gap-2">
                            <input
                                type="checkbox"
                                checked={selectedQuestionIds.includes(q.question_id)}
                                onChange={() => toggleQuestion(q.question_id)}
                            />
                            <span>
                                <strong>{q.question_name}</strong>: {q.question_text}
                            </span>
                        </label>
                    ))}
                </div>
            </div>

            {/* ✅ 메시지 출력 */}
            {message && <p className="text-sm text-blue-600 mb-4">{message}</p>}

            {/* ✅ 문항 연결 버튼 */}
            <button
                onClick={handleAssign}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
            >
                선택한 문항을 검사에 추가
            </button>
        </div>
    );
}
