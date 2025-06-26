import React, { useEffect, useState } from "react";
import axios from "axios";
import QuestionSelectModal from "../../../components/admin/QuestionSelectModal"; // ✅ 모달 import

export default function TestManage() {
    const [tests, setTests] = useState([]);
    const [testName, setTestName] = useState("");
    const [testType, setTestType] = useState("aptitude");
    const [message, setMessage] = useState("");

    const [showModal, setShowModal] = useState(false); // ✅ 모달 열림 여부
    const [selectedTestId, setSelectedTestId] = useState(null); // ✅ 선택된 test_id

    // ✅ 전체 검사 목록 불러오기
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

    // ✅ 검사 등록
    const handleCreate = async () => {
        if (!testName || !testType) {
            setMessage("검사명과 유형을 입력해주세요.");
            return;
        }

        try {
            await axios.post(
                "/api/tests",
                {
                    test_name: testName,
                    test_type: testType,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            setMessage("검사가 등록되었습니다.");
            setTestName("");
            fetchTests();
        } catch {
            setMessage("검사 등록 중 오류가 발생했습니다.");
        }
    };

    // ✅ 검사 삭제
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

    // ✅ 모달 열기
    const handleOpenModal = (testId) => {
        setSelectedTestId(testId);
        setShowModal(true);
    };

    // ✅ 선택된 문항 검사에 연결 API 호출
    const handleLinkQuestions = async (questionIds) => {
        console.log("🧪 연결 요청 test_id:", selectedTestId); // 🔍 디버깅용 로그
        console.log("🧪 연결할 문항 목록:", questionIds); // 🔍 디버깅용 로그

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
            setMessage("문항이 연결되었습니다.");
        } catch (error) {
            console.error("문항 등록 오류:", error);
            alert("문항 등록 중 오류가 발생했습니다.");
        } finally {
            setShowModal(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사 목록 관리</h1>

            <div className="mb-10">
                <h2 className="text-lg font-semibold mb-2">검사 등록</h2>
                <input
                    type="text"
                    placeholder="검사명 입력"
                    className="border rounded px-3 py-2 mr-2"
                    value={testName}
                    onChange={(e) => setTestName(e.target.value)}
                />
                <select
                    value={testType}
                    onChange={(e) => setTestType(e.target.value)}
                    className="border rounded px-3 py-2 mr-2"
                >
                    <option value="aptitude">적성검사</option>
                    <option value="personality">인성검사</option>
                </select>
                <button
                    onClick={handleCreate}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                >
                    등록
                </button>
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
                            <th className="border px-4 py-2">문항 등록</th>
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
                                <td className="border px-4 py-2 text-center">
                                    <button
                                        onClick={() => handleOpenModal(test.test_id)}
                                        className="text-blue-500 hover:underline text-sm"
                                    >
                                        문항 등록하기
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {tests.length === 0 && (
                            <tr>
                                <td colSpan="5" className="text-center py-4 text-gray-500">
                                    등록된 검사가 없습니다.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* ✅ 문항 선택 모달 */}
            <QuestionSelectModal
                isOpen={showModal}
                onClose={() => setShowModal(false)}
                onConfirm={handleLinkQuestions}
            />
        </div>
    );
}
