// src/pages/NotFound.jsx

import React from "react";

// ✅ 존재하지 않는 경로 접근 시 보여주는 페이지
export default function NotFound() {
    return (
        <div className="text-center py-20">
            {/* ✅ 에러 제목 */}
            <h1 className="text-3xl font-bold mb-4">
                404 - 페이지를 찾을 수 없습니다
            </h1>

            {/* ✅ 설명 메시지 */}
            <p className="text-gray-600">
                요청하신 페이지가 존재하지 않거나 삭제되었습니다.
            </p>
        </div>
    );
}
