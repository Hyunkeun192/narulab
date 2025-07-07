// ExamStartModal.jsx

import React, { useEffect, useState } from "react";
import { getTestQuestions } from "../api/testApi";
import ExampleQuestion from "./ExampleQuestion";

export default function ExamStartModal({ testId, testName, onClose }) {
    const [step, setStep] = useState("example");
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [submitted, setSubmitted] = useState(false);
    const [score, setScore] = useState(0);
    const [timeLeft, setTimeLeft] = useState(25 * 60); // 25분

    useEffect(() => {
        const fetch = async () => {
            try {
                const data = await getTestQuestions(testId);
                setQuestions(data.questions);
                setAnswers(new Array(data.questions.length).fill(null));
            } catch (err) {
                console.error("문항 불러오기 실패", err);
            }
        };
        fetch();
    }, [testId]);

    useEffect(() => {
        if (step !== "exam") return;
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    handleSubmit();
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [step]);

    const formatTime = (seconds) => {
        const m = String(Math.floor(seconds / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${m}:${s}`;
    };

    const handleAnswer = (choiceIndex) => {
        const updated = [...answers];
        updated[currentIndex] = choiceIndex;
        setAnswers(updated);
    };

    const handleSubmit = () => {
        let sc = 0;
        answers.forEach((ans, idx) => {
            if (ans === questions[idx]?.correct) sc++;
        });
        setScore(sc);
        setSubmitted(true);
    };

    const current = questions[currentIndex];

    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 overflow-auto z-50 p-4">
            <div className="bg-white w-full max-w-5xl rounded-xl shadow-lg p-8 relative flex flex-col">
                {/* 닫기 버튼 */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-400 hover:text-gray-700"
                >
                    ✕
                </button>

                {/* ✅ STEP: 예제 문항 */}
                {/* ✅ 예제 문항 – 본검사 전에 1회만 출력되는 예제 화면입니다. */}
                {/* - 검사 이름(testName)을 기준으로 예제 문항을 가져옵니다. */}
                {/* - onNext()가 호출되면 step이 'exam'으로 전환되어 본검사가 시작됩니다. */}
                {step === "example" && (
                    <ExampleQuestion
                        testName="언어이해검사 A"     // ✅ 예제 문항 구분 기준이 되는 검사 이름
                        onNext={() => setStep("exam")} // ✅ '본검사 시작' 클릭 시 exam 단계로 전환
                    />
                )}
                
                {/* ✅ STEP: 본검사 */}
                {step === "exam" && questions.length > 0 && current && (
                    <div className="flex flex-col md:flex-row gap-8">
                        {/* 왼쪽: 문항 본문 */}
                        <div className="flex-1">
                            {/* 상단 정보 */}
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h2 className="text-xl font-semibold text-gray-800">
                                        {testName || "Aptitude Test"}
                                    </h2>
                                    <p className="text-sm text-gray-500">
                                        Complete all {questions.length} questions within the time limit
                                    </p>
                                </div>
                                <div className="text-right">
                                    <div className="text-sm text-gray-500">Time Remaining</div>
                                    <div className="text-xl font-bold text-blue-700">{formatTime(timeLeft)}</div>
                                </div>
                            </div>

                            {/* 문항 */}
                            <div className="mb-4 text-sm text-gray-600">
                                Question {currentIndex + 1} of {questions.length}
                            </div>
                            <div className="text-blue-700 font-semibold mb-2">
                                {current.instruction}
                            </div>
                            <div className="bg-blue-50 p-4 rounded-md mb-5 text-gray-800 text-sm leading-relaxed">
                                {current.question_text}
                            </div>

                            {/* 선택지 */}
                            <div className="flex flex-col gap-3">
                                {current.options.map((opt, idx) => (
                                    <button
                                        key={opt.option_id || idx}
                                        onClick={() => handleAnswer(idx)}
                                        className={`text-left border px-4 py-2 rounded-md transition ${answers[currentIndex] === idx
                                                ? "border-blue-500 bg-blue-100"
                                                : "border-gray-300 hover:bg-gray-50"
                                            }`}
                                    >
                                        {idx + 1}. {opt.option_text}
                                    </button>
                                ))}
                            </div>

                            {/* 하단 네비게이션 */}
                            <div className="flex justify-between mt-6">
                                <button
                                    disabled={currentIndex === 0}
                                    onClick={() => setCurrentIndex((prev) => prev - 1)}
                                    className="px-4 py-2 rounded bg-gray-200 text-gray-700 disabled:opacity-40"
                                >
                                    Previous
                                </button>
                                {currentIndex < questions.length - 1 ? (
                                    <button
                                        onClick={() => setCurrentIndex((prev) => prev + 1)}
                                        className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
                                    >
                                        Next
                                    </button>
                                ) : (
                                    <button
                                        onClick={handleSubmit}
                                        className="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-700"
                                    >
                                        Submit
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* 오른쪽: 문항 현황판 */}
                        {/* ✅ 오른쪽 문항 번호판 - 회색 테두리 제거 + 크기 축소 + 배경박스 처리 */}
                        <div className="w-full md:w-[180px] scale-90">
                            {/* ✅ 배경이 있는 깔끔한 박스 형태로 래핑 */}
                            <div className="bg-gray-50 rounded-lg p-4 shadow-sm">
                                <h4 className="text-sm font-semibold text-gray-700 mb-2">Questions</h4>

                                {/* 번호 버튼들 */}
                                <div className="grid grid-cols-5 md:grid-cols-3 gap-2 mb-4">
                                    {questions.map((_, idx) => {
                                        const isCurrent = idx === currentIndex;
                                        const isAnswered = answers[idx] !== null;

                                        return (
                                            <button
                                                key={idx}
                                                onClick={() => setCurrentIndex(idx)}
                                                className={`w-8 h-8 text-sm rounded-full font-medium ${isCurrent
                                                        ? "bg-blue-600 text-white"
                                                        : isAnswered
                                                            ? "bg-gray-300 text-gray-800"
                                                            : "bg-white border border-gray-300"
                                                    }`}
                                            >
                                                {idx + 1}
                                            </button>
                                        );
                                    })}
                                </div>

                                {/* 색상 설명 */}
                                <div className="mt-2 text-xs text-gray-500 space-y-1">
                                    <div>
                                        <span className="inline-block w-3 h-3 rounded-full bg-blue-600 mr-2"></span>
                                        Current
                                    </div>
                                    <div>
                                        <span className="inline-block w-3 h-3 rounded-full bg-gray-300 mr-2"></span>
                                        Answered
                                    </div>
                                    <div>
                                        <span className="inline-block w-3 h-3 rounded-full border border-gray-400 mr-2"></span>
                                        Not Answered
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                )}

                {/* ✅ STEP: 완료 결과 */}
                {submitted && (
                    <div className="flex flex-col items-center justify-center h-full">
                        <div className="bg-white p-8 rounded-xl shadow-md text-center w-[350px]">
                            <div className="text-green-600 text-4xl mb-4">✔</div>
                            <h2 className="text-xl font-semibold mb-2">Test Completed!</h2>
                            <p className="text-gray-600 mb-4">
                                Thank you for taking the {testName || "test"}.
                            </p>
                            <div className="text-lg font-medium bg-blue-50 py-3 rounded text-blue-800">
                                Your Score: <strong>{score}</strong> / {questions.length}
                            </div>
                            <button
                                onClick={onClose}
                                className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                            >
                                Take Test Again
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
