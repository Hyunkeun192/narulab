// src/pages/product/ProductExample.jsx

import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import ExampleQuestion from "../../components/ExampleQuestion";

export default function ProductExample() {
    const { test_id } = useParams(); // 검사 ID
    const location = useLocation();
    const navigate = useNavigate();

    // ✅ ProductStart에서 전달한 검사명 (exampleQuestions.js 키값으로 사용됨)
    const { testName } = location.state || {};

    const handleStartExam = () => {
        navigate(`/product/${test_id}/exam`, {
            state: { testName },
        });
    };

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
            <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
                {/* ✅ 예제 문항 */}
                <ExampleQuestion testName={testName} onNext={handleStartExam} />
            </div>
        </div>
    );
}
