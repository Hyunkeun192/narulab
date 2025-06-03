// frontend/src/pages/user/ReportResult.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 검사 결과 리포트 페이지
export default function ReportResult() {
    const [report, setReport] = useState(null);
    const [error, setError] = useState("");

    const userId = localStorage.getItem("userId"); // ✅ 로그인 사용자 ID 저장돼 있다고 가정

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const res = await axios.get(`/api/user/reports/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                });
                const sorted = res.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                setReport(sorted[0]); // ✅ 가장 최근 결과만 표시
            } catch (err) {
                setError("리포트 데이터를 불러오지 못했습니다.");
            }
        };

        fetchReport();
    }, [userId]);

    if (error) {
        return <p className="text-red-500 p-4">{error}</p>;
    }

    if (!report) {
        return <p className="p-4">로딩 중...</p>;
    }

    return (
        <div className="max-w-xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사 결과 리포트</h1>

            <div className="border rounded p-4 shadow">
                <p className="text-sm text-gray-500 mb-2">응시일: {new Date(report.created_at).toLocaleString()}</p>
                <p className="text-lg font-semibold mb-2">총점: {report.score}점</p>
                <p className="text-lg mb-2">STEN 등급: {report.sten} / 10</p>
                <p className="text-base mt-4 whitespace-pre-line">{report.description}</p>
            </div>
        </div>
    );
}
