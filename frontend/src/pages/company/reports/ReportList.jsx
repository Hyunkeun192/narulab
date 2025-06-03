// src/pages/company/reports/ReportList.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 기업 관리자 전용 리포트 리스트 페이지
export default function ReportList() {
    const [reports, setReports] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchReports = async () => {
            try {
                const res = await axios.get("/api/company/reports", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                    },
                });
                setReports(res.data);
            } catch (err) {
                setError("리포트를 불러오는 데 실패했습니다.");
            }
        };

        fetchReports();
    }, []);

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">지원자 검사 리포트</h1>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            {reports.length === 0 ? (
                <p className="text-gray-500">리포트가 없습니다.</p>
            ) : (
                <div className="space-y-4">
                    {reports.map((report) => (
                        <div key={report.report_id} className="border p-4 rounded shadow">
                            <p>지원자 ID: {report.user_id}</p>
                            <p>점수: {report.score}점 | STEN: {report.sten}</p>
                            <p className="text-sm text-gray-700 mt-2 whitespace-pre-line">
                                {report.description}
                            </p>

                            {/* ✅ PDF 다운로드 버튼 */}
                            <div className="mt-3">
                                <a
                                    href={`/api/admin/reports/pdf/${report.report_id}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 text-sm rounded"
                                >
                                    PDF 다운로드
                                </a>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
