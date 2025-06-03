// src/pages/admin/statistics/StenChart.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

// ✅ 관리자용 STEN 분포 차트 페이지
export default function StenChart() {
    const [tests, setTests] = useState([]);
    const [selectedTestId, setSelectedTestId] = useState("");
    const [chartData, setChartData] = useState([]);
    const [error, setError] = useState("");

    // ✅ 검사 목록 불러오기
    useEffect(() => {
        const fetchTests = async () => {
            try {
                const res = await axios.get("/api/tests", {
                    headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
                });
                setTests(res.data);
            } catch {
                setError("검사 목록을 불러오지 못했습니다.");
            }
        };
        fetchTests();
    }, []);

    // ✅ STEN 분포 요청
    const fetchStenStats = async (testId) => {
        try {
            const res = await axios.get(`/api/admin/statistics/sten/${testId}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
            });
            const raw = res.data;

            // ✅ STEN 1~10에 대한 count가 없는 값은 0으로 보정
            const filled = Array.from({ length: 10 }, (_, i) => ({
                sten: (i + 1).toString(),
                count: raw[i + 1] || 0,
            }));

            setChartData(filled);
        } catch {
            setError("통계 데이터를 불러오지 못했습니다.");
        }
    };

    const handleChange = (e) => {
        const testId = e.target.value;
        setSelectedTestId(testId);
        fetchStenStats(testId);
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">STEN 통계 차트</h1>

            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            {/* ✅ 검사 선택 드롭다운 */}
            <div className="mb-6">
                <label className="block text-sm font-medium mb-2">검사 선택</label>
                <select
                    className="w-full border p-2 rounded"
                    value={selectedTestId}
                    onChange={handleChange}
                >
                    <option value="">검사를 선택하세요</option>
                    {tests.map((test) => (
                        <option key={test.test_id} value={test.test_id}>
                            {test.test_name}
                        </option>
                    ))}
                </select>
            </div>

            {/* ✅ Recharts 막대 차트 */}
            <div className="w-full h-96 bg-white border rounded shadow p-4">
                {chartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="sten" />
                            <YAxis allowDecimals={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#3182ce" />
                        </BarChart>
                    </ResponsiveContainer>
                ) : (
                    <p className="text-gray-500">차트를 보려면 검사를 선택하세요.</p>
                )}
            </div>
        </div>
    );
}
