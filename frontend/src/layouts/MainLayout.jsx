// src/layouts/MainLayout.jsx

import React from "react";
import Header from "../components/Header"; // ✅ 공통 Header 불러오기

// ✅ 모든 페이지에 공통적으로 적용되는 레이아웃 컴포넌트
export default function MainLayout({ children }) {
    return (
        <div className="min-h-screen bg-white text-gray-900 font-sans">

            {/* ✅ 모든 페이지 상단에 고정되는 헤더 */}
            <Header />

            {/* ✅ 개별 페이지 콘텐츠를 렌더링할 영역 */}
            {/* → 페이지 전환 애니메이션은 이 children 부분에만 적용됨 */}
            <main className="px-4 py-10">
                {children}
            </main>
        </div>
    );
}
