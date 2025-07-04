// src/components/ExamStartModal.jsx

import React, { useEffect, useState } from "react";
import { getTestQuestions } from "../api/testApi"; // ✅ 실제 문항 불러오는 API
import { motion } from "framer-motion";
import ExampleQuestion from "./ExampleQuestion"; // ✅ 예제 문항 컴포넌트 추가

export default function ExamStartModal({ testId, testName, onClose }) {
    const [step, setStep] = useState("notice"); // notice → example → exam
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [currentIndex, setCurrentIndex] = useState(0);

    // ✅ 전체 문항 로딩
    useEffect(() => {
        const fetch = async () => {
            try {
                const data = await getTestQuestions(testId);
                setQuestions(data);
            } catch (err) {
                console.error("문항 불러오기 실패", err);
            }
        };
        fetch();
    }, [testId]);

    const handleSelect = (questionId, index) => {
        setAnswers((prev) => ({ ...prev, [questionId]: index }));
    };

    const handleNext = () => {
        if (currentIndex < questions.length - 1) {
            setCurrentIndex(currentIndex + 1);
        }
    };

    const handleGoTo = (idx) => setCurrentIndex(idx);

    const handleSubmit = () => {
        console.log("응답 결과:", answers);
        alert("제출 완료!");
        onClose();
    };

    const current = questions[currentIndex];

    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-center">
            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white w-full max-w-2xl rounded-xl shadow-lg p-6 relative max-h-[90vh] overflow-y-auto"
            >
                <button
                    onClick={onClose}
                    className="absolute top-3 right-4 text-gray-500 hover:text-black text-sm"
                >
                    닫기
                </button>

                {/* ✅ 검사 유의사항 */}
                {step === "notice" && (
                    <div>
                        <h2 className="text-xl font-semibold mb-4">검사 유의사항</h2>
                        <ul className="list-disc space-y-2 text-sm text-gray-700 pl-5">
                            <li>검사 시간 동안 집중해 주세요.</li>
                            <li>답변은 솔직하게 응답해 주세요.</li>
                            <li>문항은 1개씩 출제되며, 제출 시 결과로 반영됩니다.</li>
                        </ul>
                        <div className="text-center mt-6">
                            <button
                                onClick={() => setStep("example")}
                                className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700"
                            >
                                예제 문항 풀기
                            </button>
                        </div>
                    </div>
                )}

                {/* ✅ 예제 문항 영역 - 컴포넌트 분리 */}
                {step === "example" && (
                    <ExampleQuestion testName="언어이해검사 A" onNext={() => setStep("exam")} />
                )}

                {/* ✅ 본검사 */}
                {step === "exam" && questions.length > 0 && current && (
                    <div>
                        <div className="text-sm text-right text-gray-500 mb-2">
                            {currentIndex + 1} / {questions.length} 문항
                        </div>

                        {current.instruction && (
                            <p className="text-sm text-gray-600 mb-2">{current.instruction}</p>
                        )}
                        <p className="font-medium mb-3">{current.question_text}</p>

                        <ul className="space-y-2 text-sm mb-4">
                            {current.options
                                ?.sort((a, b) => a.option_order - b.option_order)
                                .map((opt, idx) => (
                                    <li
                                        key={idx}
                                        onClick={() => handleSelect(current.question_id, idx)}
                                        className={`cursor-pointer border rounded p-2 hover:bg-gray-100 ${answers[current.question_id] === idx
                                                ? "bg-blue-100 border-blue-400"
                                                : ""
                                            }`}
                                    >
                                        {idx + 1}. {opt.option_text}
                                    </li>
                                ))}
                        </ul>

                        <div className="flex gap-1 mb-4 flex-wrap">
                            {questions.map((q, idx) => (
                                <button
                                    key={q.question_id}
                                    className={`w-6 h-6 text-xs rounded-full border ${answers[q.question_id] !== undefined
                                            ? "bg-blue-600 text-white"
                                            : "bg-gray-200 text-gray-600"
                                        } ${idx === currentIndex ? "ring-2 ring-blue-400" : ""}`}
                                    onClick={() => handleGoTo(idx)}
                                >
                                    {idx + 1}
                                </button>
                            ))}
                        </div>

                        <div className="flex justify-end">
                            {currentIndex < questions.length - 1 ? (
                                <button
                                    onClick={handleNext}
                                    className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700"
                                >
                                    다음 문항
                                </button>
                            ) : (
                                <button
                                    onClick={handleSubmit}
                                    className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700"
                                >
                                    제출하기
                                </button>
                            )}
                        </div>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
