// src/pages/admin/reports/ReportRuleManage.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 검사별 STEN 해석 문구 등록 페이지
export default function ReportRuleManage() {
    const [tests, setTests] = useState([]); // ✅ 검사 목록
    const [selectedTestId, setSelectedTestId] = useState(""); // ✅ 선택된 검사 ID
    const [descriptions, setDescriptions] = useState({}); // ✅ STEN별 해석 문구
    const [message, setMessage] = useState("");

    // ✅ 검사 목록 불러오기
    useEffect(() => {
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
        fetchTests();
    }, []);

    // ✅ STEN 해석 문구 입력값 변경 핸들러
    const handleChange = (sten, value) => {
        setDescriptions((prev) => ({
            ...prev,
            [sten]: value,
        }));
    };

    // ✅ 저장 요청
    const handleSave = async () => {
        if (!selectedTestId) {
            setMessage("검사를 선택해주세요.");
            return;
        }

        try {
            await axios.post(
                `/api/admin/report-rules/${selectedTestId}`,
                {
                    sten_descriptions: descriptions,
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                }
            );
            setMessage("저장되었습니다.");
        } catch {
            setMessage("저장 중 오류가 발생했습니다.");
        }
    };

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사별 리포트 해석 기준 등록</h1>

            {/* ✅ 메시지 */}
            {message && <p className="text-blue-600 mb-4 text-sm">{message}</p>}

            {/* ✅ 검사 선택 */}
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

            {/* ✅ STEN별 해석 문구 입력 */}
            <div className="grid grid-cols-1 gap-4 mb-6">
                {Array.from({ length: 10 }, (_, i) => i + 1).map((sten) => (
                    <div key={sten}>
                        <label className="text-sm font-medium mb-1 block">STEN {sten}</label>
                        <textarea
                            rows={2}
                            className="w-full border rounded p-2"
                            value={descriptions[sten] || ""}
                            onChange={(e) => handleChange(sten, e.target.value)}
                            placeholder={`STEN ${sten}에 해당하는 해석 문구를 입력하세요`}
                        />
                    </div>
                ))}
            </div>

            {/* ✅ 저장 버튼 */}
            <button
                onClick={handleSave}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
            >
                저장하기
            </button>
        </div>
    );
}
