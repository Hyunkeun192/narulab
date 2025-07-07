// ExampleQuestion.jsx

import React, { useState } from "react";
// ✅ getExampleQuestion 함수 import
import { getExampleQuestion } from "../data/exampleQuestions";

/**
 * [예제 문항 컴포넌트]
 * - props: testName (검사 이름), onNext (본검사 시작 핸들러)
 * - 검사 이름(testName)에 따라 해당하는 예제 문항을 불러오고 렌더링합니다.
 */
export default function ExampleQuestion({ testName, onNext }) {
    const [showExplanation, setShowExplanation] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);

    // ✅ 예제 문항 가져오기 (함수 기반)
    const example = getExampleQuestion(testName);

    if (!example) {
        return (
            <div className="text-center text-red-500 text-sm">
                예제 문항이 등록되어 있지 않습니다.
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-lg font-semibold mb-4">예제 문항</h2>
            <p className="mb-3">다음 글을 읽고 가장 적절한 보기를 선택하세요.</p>

            {/* ✅ 지문 */}
            <div className="border p-4 rounded bg-gray-50 mb-4 text-sm text-gray-800 whitespace-pre-line leading-relaxed">
                {example.passage}
            </div>

            {/* ✅ 질문 */}
            <p className="font-medium mb-2">{example.question}</p>

            {/* ✅ 선택지 */}
            <ul className="space-y-2 text-sm mb-4">
                {example.options.map((opt, idx) => (
                    <li
                        key={idx}
                        className={`cursor-pointer p-2 border rounded hover:bg-gray-100 ${selectedOption === idx ? "bg-blue-100 border-blue-400" : ""
                            }`}
                        onClick={() => setSelectedOption(idx)}
                    >
                        {opt}
                    </li>
                ))}
            </ul>

            {/* ✅ 해설 토글 */}
            <div className="mb-4">
                <button
                    onClick={() => setShowExplanation((prev) => !prev)}
                    className="text-sm text-blue-600 hover:underline"
                >
                    {showExplanation ? "해설 닫기 ▲" : "해설 보기 ▼"}
                </button>
                {showExplanation && (
                    <div className="mt-2 bg-gray-50 p-3 border rounded text-sm text-gray-700 whitespace-pre-line leading-relaxed">
                        {example.explanation}
                    </div>
                )}
            </div>

            {/* ✅ 본검사 시작 버튼 */}
            <div className="text-right">
                <button
                    onClick={onNext}
                    className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700"
                >
                    본검사 시작
                </button>
            </div>
        </div>
    );
}
