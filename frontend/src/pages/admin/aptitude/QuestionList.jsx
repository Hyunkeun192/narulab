import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * ✅ 문항 목록 페이지 (리스트 중심 + 필터/검색/모달 보기 지원)
 * - 카드 방식 → 리스트 1행 요약형으로 변경
 * - 필터: usage_type (적성/인성 등)
 * - 검색: 문항명, 문항 내용 등 텍스트
 * - 상세보기: 클릭 시 모달로 문항 정보 표시
 */
export default function QuestionList() {
    const [questions, setQuestions] = useState([]);
    const [filtered, setFiltered] = useState([]);
    const [selectedQuestion, setSelectedQuestion] = useState(null); // 상세 보기용
    const [examType, setExamType] = useState("all");
    const [search, setSearch] = useState("");
    const [message, setMessage] = useState("");
    const [editMode, setEditMode] = useState(false);


    // ✅ 문항 목록 로드 (최초 실행 시)
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

    // ✅ 필터/검색 적용
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

    // ✅ 문항 삭제 처리
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
            fetchQuestions(); // 삭제 후 목록 갱신
        } catch {
            setMessage("삭제 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="max-w-6xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">문항 목록</h1>

            {/* ✅ 메시지 출력 */}
            {message && <p className="text-blue-600 text-sm mb-4">{message}</p>}

            {/* ✅ 필터/검색 UI */}
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

            {/* ✅ 리스트 헤더 */}
            <div className="grid grid-cols-5 gap-2 px-2 py-2 font-semibold text-gray-700 border-b bg-gray-50">
                <div>검사유형</div>
                <div>문항유형</div>
                <div>문항명</div>
                <div className="text-center">상세보기</div>
                <div className="text-center">삭제</div>
            </div>

            {/* ✅ 문항 리스트 */}
            <div className="divide-y">
                {filtered.map((q) => (
                    <div
                        key={q.question_id}
                        className="grid grid-cols-5 gap-2 items-center px-2 py-3 text-sm"
                    >
                        <div>{q.usage_type}</div>
                        <div>{q.question_type}</div>
                        <div>{q.question_name}</div>
                        <div className="text-center">
                            <button
                                onClick={() => setSelectedQuestion(q)}
                                className="text-blue-600 hover:underline"
                            >
                                상세 보기
                            </button>
                        </div>
                        <div className="text-center">
                            <button
                                onClick={() => handleDelete(q.question_id)}
                                className="text-red-500 hover:underline"
                            >
                                삭제
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* ✅ 조건 불만족 시 안내 */}
            {filtered.length === 0 && (
                <p className="text-gray-500 text-center mt-4">
                    조건에 해당하는 문항이 없습니다.
                </p>
            )}

            {selectedQuestion && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <h2 className="text-xl font-bold mb-4">
                            문항 {editMode ? "수정" : "상세 보기"}
                        </h2>

                        {/* 문항 제목/본문 */}
                        {editMode ? (
                            <>
                                <input
                                    className="border p-2 mb-2 w-full"
                                    value={selectedQuestion.question_name}
                                    onChange={(e) =>
                                        setSelectedQuestion({ ...selectedQuestion, question_name: e.target.value })
                                    }
                                    placeholder="문항명"
                                />
                                <textarea
                                    className="border p-2 mb-2 w-full"
                                    value={selectedQuestion.instruction}
                                    onChange={(e) =>
                                        setSelectedQuestion({ ...selectedQuestion, instruction: e.target.value })
                                    }
                                    placeholder="지시문"
                                />
                                <textarea
                                    className="border p-2 mb-4 w-full"
                                    value={selectedQuestion.question_text}
                                    onChange={(e) =>
                                        setSelectedQuestion({ ...selectedQuestion, question_text: e.target.value })
                                    }
                                    placeholder="문항 텍스트"
                                />
                            </>
                        ) : (
                            <>
                                <p className="mb-1 text-sm text-gray-500">검사유형: {selectedQuestion.usage_type}</p>
                                <p className="mb-1 text-sm text-gray-500">문항유형: {selectedQuestion.question_type}</p>
                                <p className="font-semibold">{selectedQuestion.question_name}</p>
                                <p className="whitespace-pre-line mb-2">{selectedQuestion.instruction}</p>
                                <p className="whitespace-pre-line mb-4">{selectedQuestion.question_text}</p>
                            </>
                        )}

                        {/* 선택지 */}
                        <ul className="mb-4">
                            {selectedQuestion.options.map((opt, i) => (
                                <li key={i} className="flex items-center gap-2 mb-2">
                                    {editMode ? (
                                        <>
                                            <input
                                                className="border p-1 flex-1"
                                                value={opt.option_text}
                                                onChange={(e) => {
                                                    const updated = [...selectedQuestion.options];
                                                    updated[i].option_text = e.target.value;
                                                    setSelectedQuestion({ ...selectedQuestion, options: updated });
                                                }}
                                            />
                                            <label className="text-sm flex items-center gap-1">
                                                <input
                                                    type="checkbox"
                                                    checked={opt.is_correct}
                                                    onChange={() => {
                                                        const updated = [...selectedQuestion.options];
                                                        updated[i].is_correct = !opt.is_correct;
                                                        setSelectedQuestion({ ...selectedQuestion, options: updated });
                                                    }}
                                                />
                                                정답
                                            </label>
                                        </>
                                    ) : (
                                        <span className={opt.is_correct ? "text-green-600" : ""}>
                                            {opt.option_text}
                                            {opt.is_correct && " (정답)"}
                                        </span>
                                    )}
                                </li>
                            ))}
                        </ul>

                        {/* 해설 */}
                        <p className="text-xs text-gray-500">
                            정답 해설: {selectedQuestion.correct_explanation || "없음"}
                        </p>
                        <p className="text-xs text-gray-500 mb-4">
                            오답 해설: {selectedQuestion.wrong_explanation || "없음"}
                        </p>

                        {/* 버튼 영역 */}
                        <div className="text-right flex gap-2 justify-end">
                            {editMode ? (
                                <>
                                    <button
                                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                                        
                                        onClick={async () => {
                                            try {
                                                const payload = {
                                                    test_id: selectedQuestion.test_id || null,
                                                    question_name: selectedQuestion.question_name,
                                                    question_text: selectedQuestion.question_text,
                                                    question_type: selectedQuestion.question_type,
                                                    usage_type: selectedQuestion.usage_type || "aptitude", // ✅ 요 줄 추가!
                                                    is_multiple_choice: selectedQuestion.is_multiple_choice,
                                                    instruction: selectedQuestion.instruction,
                                                    correct_explanation: selectedQuestion.correct_explanation,
                                                    wrong_explanation: selectedQuestion.wrong_explanation,
                                                    question_image_url: selectedQuestion.question_image_url || null,

                                                    // ✅ 선택지 구조 정합성 보장
                                                    options: [...selectedQuestion.options] // 원본 훼손 방지
                                                        .sort((a, b) => a.option_order - b.option_order) // ✅ 순서 보장
                                                        .map((opt, index) => ({
                                                            option_text: opt.option_text,
                                                            is_correct: opt.is_correct,
                                                            option_order: index, // index를 기준으로 재지정
                                                            option_image_url: opt.option_image_url || null,
                                                        })),                                                    
                                                };

                                                await axios.put(
                                                    `/api/admin/questions/${selectedQuestion.question_id}`,
                                                    payload,
                                                    {
                                                        headers: {
                                                            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                                                        },
                                                    }
                                                );

                                                setMessage("문항이 수정되었습니다.");
                                                setEditMode(false);
                                                setSelectedQuestion(null);
                                                fetchQuestions(); // 리스트 갱신
                                            } catch {
                                                setMessage("수정 중 오류가 발생했습니다.");
                                            }
                                        }}
                                          
                                        
                                    >
                                        ✅ 저장하기
                                    </button>
                                    <button
                                        className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
                                        onClick={() => setEditMode(false)}
                                    >
                                        취소
                                    </button>
                                </>
                            ) : (
                                <button
                                    className="bg-yellow-400 px-4 py-2 rounded hover:bg-yellow-500"
                                    onClick={() => setEditMode(true)}
                                >
                                    ✏️ 수정하기
                                </button>
                            )}
                            <button
                                onClick={() => {
                                    setEditMode(false);
                                    setSelectedQuestion(null);
                                }}
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
