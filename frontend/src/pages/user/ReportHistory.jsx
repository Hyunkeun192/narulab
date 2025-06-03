// frontend/src/pages/user/ReportHistory.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 사용자 리포트 이력 페이지
export default function ReportHistory() {
    const [reports, setReports] = useState([]);
    const [error, setError] = useState("");

    const userId = localStorage.getItem("userId");

    useEffect(() => {
        const fetchReports = async () => {
            try {
                const res = await axios.get(`/api/user/reports/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                });
                const sorted = res.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                setReports(sorted);
            } catch (err) {
                setError("리포트 이력을 불러오는 데 실패했습니다.");
            }
        };
        fetchReports();
    }, [userId]);

    if (error) return <p className="text-red-500 p-4">{error}</p>;

    return (
        <div className="max-w-3xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">검사 리포트 이력</h1>

            {reports.length === 0 ? (
                <p>저장된 리포트가 없습니다.</p>
            ) : (
                <div className="space-y-4">
                    {reports.map((report) => (
                        <div
                            key={report.report_id}
                            className="border p-4 rounded shadow hover:shadow-md transition"
                        >
                            <p className="text-sm text-gray-500 mb-1">
                                응시일: {new Date(report.created_at).toLocaleString()}
                            </p>
                            <p className="font-semibold">
                                총점: {report.score}점 | STEN: {report.sten} / 10
                            </p>
                            <p className="text-sm mt-2 text-gray-700 whitespace-pre-line">
                                {report.description.length > 120
                                    ? report.description.slice(0, 120) + "..."
                                    : report.description}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
