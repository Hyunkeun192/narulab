// src/pages/product.jsx

import React from "react";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/useUser"; // 공통 사용자 정보 훅

export default function Product() {
    const user = useUser();

    return (
        <div className="min-h-screen bg-white text-gray-900 font-sans">
            {/* Header */}
            <header className="flex items-center justify-between px-8 py-4 border-b border-gray-200">
                <Link to="/" className="text-xl font-bold">narulab</Link>
                <nav className="hidden md:flex space-x-8 text-sm font-medium">
                    <Link to="/notice" className="hover:text-blue-500">Notice</Link>
                    <Link to="/product" className="hover:text-blue-500">Product</Link>
                    <a href="#qna" className="hover:text-blue-500">QnA</a>
                    <a href="#contact" className="hover:text-blue-500">Contact</a>
                </nav>
                <div className="space-x-4 text-sm">
                    <a href="/login" className="hover:text-blue-500">Login</a>
                    <a href="/signup" className="text-white bg-blue-500 px-4 py-1.5 rounded-full hover:bg-blue-600">Sign up</a>
                </div>
            </header>

            {/* Product List */}
            <main className="max-w-3xl mx-auto px-4 py-10">
                <h1 className="text-3xl font-bold text-center mb-10">검사 / 제품 목록</h1>

                <div className="space-y-8">
                    <section>
                        <h2 className="text-xl font-semibold border-b pb-1 mb-2">퍼스널리티 검사</h2>
                        <ul className="list-disc list-inside text-gray-800 space-y-1">
                            <li><Link to="/tests/1" className="hover:underline">진로 적성 검사</Link></li>
                            <li><Link to="/tests/2" className="hover:underline">직무 성향 분석</Link></li>
                            <li><Link to="/tests/3" className="hover:underline">AI 자기소개서 분석</Link></li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold border-b pb-1 mb-2">기업 맞춤형 검사</h2>
                        <ul className="list-disc list-inside text-gray-800 space-y-1">
                            <li><Link to="/tests/4" className="hover:underline">삼성그룹 역량 진단</Link></li>
                            <li><Link to="/tests/5" className="hover:underline">LG 조직 적응력 테스트</Link></li>
                            <li><Link to="/tests/6" className="hover:underline">현대차 직무 중심 검사</Link></li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold border-b pb-1 mb-2">자기계발 / 취업 준비</h2>
                        <ul className="list-disc list-inside text-gray-800 space-y-1">
                            <li><Link to="/tests/7" className="hover:underline">이력서 클리닉 진단</Link></li>
                            <li><Link to="/tests/8" className="hover:underline">면접 피드백 분석</Link></li>
                            <li><Link to="/tests/9" className="hover:underline">취업 마인드셋 체크리스트</Link></li>
                        </ul>
                    </section>
                </div>
            </main>
        </div>
    );
}
