// src/components/Header.jsx

import React from "react";
import { Link } from "react-router-dom"; // ✅ 페이지 간 이동을 위한 Link 컴포넌트 사용

// ✅ Header 컴포넌트 정의
export default function Header() {
    return (
        // ✅ 상단 헤더 전체 박스: 좌우 여백 + 상하 패딩 + 경계선 + 흰 배경
        <header className="flex items-center justify-between px-8 py-4 border-b border-gray-200 bg-white">

            {/* ✅ 왼쪽 로고 or 홈 링크 */}
            <Link to="/" className="text-xl font-bold">
                narulab
            </Link>

            {/* ✅ 가운데 네비게이션 메뉴 (중간 breakpoint 이상에서만 표시) */}
            <nav className="hidden md:flex space-x-8 text-sm font-medium">
                <Link to="/notice" className="hover:text-blue-500">Notice</Link>
                <Link to="/product" className="hover:text-blue-500">Product</Link>
                <Link to="/qna" className="hover:text-blue-500">QnA</Link>
                <Link to="/contact" className="hover:text-blue-500">Contact</Link>
            </nav>

            {/* ✅ 오른쪽 사용자 액션: 로그인/회원가입 */}
            <div className="space-x-4 text-sm">
                {/* 로그인 버튼: 기본 텍스트 스타일 */}
                <Link to="/login" className="hover:text-blue-500">
                    Login
                </Link>

                {/* 회원가입 버튼: 파란 배경 + 둥근 테두리 + hover 효과 */}
                <Link
                    to="/signup"
                    className="text-white bg-blue-500 px-4 py-1.5 rounded-full hover:bg-blue-600"
                >
                    Sign up
                </Link>
            </div>
        </header>
    );
}
