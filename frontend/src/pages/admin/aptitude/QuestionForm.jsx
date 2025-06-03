// src/pages/admin/aptitude/QuestionForm.jsx

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

// ✅ 적성검사 문항 등록 페이지
export default function QuestionForm() {
    const navigate = useNavigate();

    // ✅ 상태 정의: 문항 내용
    const [questionText, setQuestionText] = useState("");

    // ✅ 상태 정의: 문항 유형 (text / image)
    const [questionType, setQuestionType] = useState("text");

    // ✅ 상태 정의: 복수 선택 여부
    const [isMultipleChoice, setIsMultipleChoice] = useState(false);

    // ✅ 상태 정의: 선택지 배열
    const [options, setOptions] = useState([
        { option_text: "", is_correct: false },
        { option_text: "", is_correct: false },
    ]);

    // ✅ 상태 정의: 로딩 및 에러 메시지
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // ✅ 선택지 추가 (최대 5개)
    const handleAddOption = () => {
        if (options.length < 5) {
            setOptions([...options, { option_text: "", is_correct: false }]);
        }
    };

    // ✅ 선택지 제거 (최소 2개)
    const handleRemoveOption = (index) => {
        if (options.length > 2) {
            const updated = [...options];
            updated.splice(index, 1);
            setOptions(updated);
        }
    };

    // ✅ 선택지 텍스트 수정
    const handleOptionTextChange = (index, value) => {
        const updated = [...options];
        updated[index].option_text = value;
        setOptions(updated);
    };

    // ✅ 정답 여부 토글
    const handleCorrectToggle = (index) => {
        const updated = [...options];
        if (isMultipleChoice) {
            updated[index].is_correct = !updated[index].is_correct;
        } else {
            updated.forEach((opt, i) => {
                opt.is_correct = i === index;
            });
        }
        setOptions(updated);
    };

    // ✅ 문항 등록 요청 (API 연동)
    const handleSubmit = async () => {
        setLoading(true);
        setError("");

        try {
            const testId = localStorage.getItem("currentTestId"); // ✅ 현재 선택된 검사 ID를 localStorage에서 가져옴
            if (!testId) {
                setError("test_id가 설정되지 않았습니다.");
                setLoading(false);
                return;
            }

            const payload = {
                test_id: testId,
                question_text: questionText,
                question_type: questionType,
                is_multiple_choice: isMultipleChoice,
                options,
            };

            await axios.post("/api/admin/questions", payload, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });

            alert("문항이 등록되었습니다.");
            navigate("/admin");
        } catch (err) {
            setError("문항 등록 중 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">적성검사 문항 등록</h1>

            {/* ✅ 문항 텍스트 입력 */}
            <label className="block text-sm font-medium mb-1">문항 내용</label>
            <textarea
                className="w-full border rounded p-2 mb-4"
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                rows={3}
            />

            {/* ✅ 문항 유형 선택 */}
            <label className="block text-sm font-medium mb-1">문항 유형</label>
            <select
                className="w-full border rounded p-2 mb-4"
                value={questionType}
                onChange={(e) => setQuestionType(e.target.value)}
            >
                <option value="text">텍스트</option>
                <option value="image">이미지</option>
            </select>

            {/* ✅ 복수 선택 여부 */}
            <label className="flex items-center mb-4">
                <input
                    type="checkbox"
                    checked={isMultipleChoice}
                    onChange={(e) => setIsMultipleChoice(e.target.checked)}
                    className="mr-2"
                />
                복수 정답 허용
            </label>

            {/* ✅ 보기 목록 */}
            <div className="mb-4">
                <label className="block text-sm font-medium mb-2">선택지</label>
                {options.map((opt, index) => (
                    <div key={index} className="flex items-center gap-2 mb-2">
                        <input
                            type="text"
                            className="flex-1 border rounded p-2"
                            placeholder={`선택지 ${index + 1}`}
                            value={opt.option_text}
                            onChange={(e) =>
                                handleOptionTextChange(index, e.target.value)
                            }
                        />
                        <label className="flex items-center">
                            <input
                                type="checkbox"
                                checked={opt.is_correct}
                                onChange={() => handleCorrectToggle(index)}
                                className="mr-1"
                            />
                            정답
                        </label>
                        {options.length > 2 && (
                            <button
                                type="button"
                                className="text-red-500 text-sm"
                                onClick={() => handleRemoveOption(index)}
                            >
                                삭제
                            </button>
                        )}
                    </div>
                ))}
                {options.length < 5 && (
                    <button
                        type="button"
                        onClick={handleAddOption}
                        className="text-blue-500 text-sm mt-1"
                    >
                        + 선택지 추가
                    </button>
                )}
            </div>

            {/* ✅ 에러 메시지 출력 */}
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            {/* ✅ 등록 버튼 */}
            <button
                onClick={handleSubmit}
                disabled={loading}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
            >
                {loading ? "등록 중..." : "문항 등록"}
            </button>
        </div>
    );
}
