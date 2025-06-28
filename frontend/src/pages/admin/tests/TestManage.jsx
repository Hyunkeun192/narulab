import React, { useEffect, useState } from "react";
import axios from "axios";
import QuestionSelectModal from "../../../components/admin/QuestionSelectModal";
import QuestionEditModal from "./QuestionEditModal";
import QuestionViewModal from "./QuestionViewModal";

export default function TestManage() {
    const [tests, setTests] = useState([]);
    const [testName, setTestName] = useState("");
    const [testType, setTestType] = useState("aptitude");
    const [durationMinutes, setDurationMinutes] = useState(""); // ✅ 소요 시간 추가
    const [message, setMessage] = useState("");

    const [showModal, setShowModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [showViewModal, setShowViewModal] = useState(false);
    const [selectedTestId, setSelectedTestId] = useState(null);

    const fetchTests = async () => {
        try {
            const res = await axios.get("/api/tests", {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setTests(res.data);
        } catch {
            setMessage("검사 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchTests();
    }, []);

    const handleCreate = async () => {
        if (!testName || !testType || !durationMinutes) {
            setMessage("검사명, 유형, 소요 시간을 모두 입력해주세요.");
            return;
        }

        try {
            await axios.post(
                "/api/tests",
                {
                    test_name: testName,
                    test_type: testType,
                    duration_minutes: Number(durationMinutes), // ✅ 전송
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            setMessage("검사가 등록되었습니다.");
            setTestName("");
            setDurationMinutes(""); // ✅ 초기화
            fetchTests();
        } catch {
            setMessage("검사 등록 중 오류가 발생했습니다.");
        }
    };

    const handleDelete = async (testId) => {
        const confirm = window.confirm("정말 삭제하시겠습니까?");
        if (!confirm) return;

        try {
            await axios.delete(`/api/tests/${testId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            setMessage("검사가 삭제되었습니다.");
            fetchTests();
        } catch {
            setMessage("삭제 중 오류가 발생했습니다.");
        }
    };

    const handleOpenModal = (testId) => {
        setSelectedTestId(testId);
        setShowModal(true);
    };

    const handleOpenEditModal = (testId) => {
        setSelectedTestId(testId);
        setShowEditModal(true);
    };

    const handleOpenViewModal = (testId) => {
        setSelectedTestId(testId);
        setShowViewModal(true);
    };

    const handleLinkQuestions = async (questionIds) => {
        try {
            await axios.post(
                `/api/admin/tests/${selectedTestId}/questions`,
                { question_ids: questionIds },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            alert("✅ 문항이 검사에 등록되었습니다.");
        } catch (error) {
            console.error("문항 등록 오류:", error);
            alert("문항 등록 중 오류가 발생했습니다.");
        } finally {
            setShowModal(false);
        }
    };

    const handleTogglePublish = async (testId, publish) => {
        try {
            await axios.put(
                `/api/admin/tests/${testId}/publish`,
                {},
                {
                    params: { publish },
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            fetchTests();
        } catch (error) {
            console.error("검사 상태 변경 오류:", error);
            alert("검사 상태 변경 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사 목록 관리</h1>

            <div className="border rounded p-4 bg-gray-50 shadow-sm w-full max-w-xl mb-8">
                <h2 className="text-md font-semibold mb-3 text-gray-800">📝 신규 검사 등록</h2>
                <div className="flex gap-3 items-center">
                    <input
                        type="text"
                        placeholder="검사명 입력"
                        className="flex-1 border rounded px-3 py-2 text-sm focus:outline-blue-500"
                        value={testName}
                        onChange={(e) => setTestName(e.target.value)}
                    />
                    <select
                        value={testType}
                        onChange={(e) => setTestType(e.target.value)}
                        className="border rounded px-3 py-2 text-sm"
                    >
                        <option value="aptitude">적성검사</option>
                        <option value="personality">인성검사</option>
                    </select>
                    <input
                        type="number"
                        placeholder="시간(분)"
                        value={durationMinutes}
                        onChange={(e) => setDurationMinutes(e.target.value)}
                        className="w-20 border rounded px-2 py-2 text-sm"
                        min="1"
                    />
                    <button
                        onClick={handleCreate}
                        className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded"
                    >
                        등록
                    </button>
                </div>
            </div>

            {message && <p className="text-sm text-blue-600 mb-4">{message}</p>}

            <div>
                <h2 className="text-lg font-semibold mb-3">등록된 검사</h2>
                <table className="w-full table-auto border-collapse border">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="border px-4 py-2">검사명</th>
                            <th className="border px-4 py-2">유형</th>
                            <th className="border px-4 py-2">ID</th>
                            <th className="border px-4 py-2">삭제</th>
                            <th className="border px-4 py-2">문항</th>
                            <th className="border px-4 py-2">상태</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tests.map((test) => (
                            <tr key={test.test_id}>
                                <td className="border px-4 py-2">{test.test_name}</td>
                                <td className="border px-4 py-2">{test.test_type}</td>
                                <td className="border px-4 py-2 text-xs">{test.test_id}</td>
                                <td className="border px-4 py-2 text-center">
                                    <button
                                        onClick={() => handleDelete(test.test_id)}
                                        className="text-red-500 hover:underline text-sm"
                                    >
                                        삭제
                                    </button>
                                </td>
                                <td className="border px-4 py-2 text-center space-x-2 text-sm">
                                    <button
                                        onClick={() => handleOpenModal(test.test_id)}
                                        className="text-blue-500 hover:underline"
                                    >
                                        등록
                                    </button>
                                    <button
                                        onClick={() => handleOpenEditModal(test.test_id)}
                                        className="text-yellow-500 hover:underline"
                                    >
                                        수정
                                    </button>
                                    <button
                                        onClick={() => handleOpenViewModal(test.test_id)}
                                        className="text-gray-700 hover:underline"
                                    >
                                        확인
                                    </button>
                                </td>
                                <td className="border px-4 py-2 text-center text-sm">
                                    {test.question_count > 0 ? (
                                        <button
                                            onClick={() =>
                                                handleTogglePublish(test.test_id, !test.is_published)
                                            }
                                            className={`px-2 py-1 rounded text-white text-xs ${test.is_published
                                                ? "bg-gray-500 hover:bg-gray-600"
                                                : "bg-green-600 hover:bg-green-700"
                                                }`}
                                        >
                                            {test.is_published ? "비활성화" : "활성화"}
                                        </button>
                                    ) : (
                                        <span className="text-gray-400 text-xs">-</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {tests.length === 0 && (
                            <tr>
                                <td colSpan="6" className="text-center py-4 text-gray-500">
                                    등록된 검사가 없습니다.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* 모달들 */}
            <QuestionSelectModal
                isOpen={showModal}
                onClose={() => setShowModal(false)}
                onConfirm={handleLinkQuestions}
            />

            {showEditModal && (
                <QuestionEditModal
                    testId={selectedTestId}
                    onClose={() => setShowEditModal(false)}
                />
            )}

            {showViewModal && (
                <QuestionViewModal
                    testId={selectedTestId}
                    onClose={() => setShowViewModal(false)}
                />
            )}
        </div>
    );
}
