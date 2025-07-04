// 기존 주석 유지 + 추가된 부분 주석 처리

import React from "react";
import { useNavigate } from "react-router-dom";

function ProductStart({ testId }) {
    const navigate = useNavigate();

    const handleExampleStart = () => {
        // ✅ testName을 함께 넘겨줍니다.
        navigate(`/product/${testId}/example`, {
            state: { testName: "언어이해검사 A" },
        });
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-2xl font-bold mb-6">검사 유의사항</h1>
            <ul className="list-disc text-left mb-6">
                <li>문제를 집중해서 풀어주세요.</li>
                <li>검사는 한 번만 응시할 수 있습니다.</li>
                <li>중간에 종료하면 저장되지 않습니다.</li>
            </ul>
            <button
                onClick={handleExampleStart}
                className="bg-blue-500 text-white px-4 py-2 rounded"
            >
                예제 문제 풀기
            </button>
        </div>
    );
}

export default ProductStart;
