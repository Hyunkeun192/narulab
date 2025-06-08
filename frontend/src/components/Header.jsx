import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogIn, LogOut, Shield } from "lucide-react"; // ✅ 관리자 아이콘 추가
import logo from "../assets/logo.png"; // ✅ 로고 이미지 import

export default function Header() {
    const navigate = useNavigate();

    // ✅ 상태 기반 로그인 여부 및 관리자 여부 저장
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [role, setRole] = useState(null);

    // ✅ localStorage 값 초기 로딩 및 리렌더링 반영
    useEffect(() => {
        const token = localStorage.getItem("accessToken");
        const userRole = localStorage.getItem("userRole");

        setIsLoggedIn(!!token);
        setRole(userRole);
    }, []);

    // ✅ 관리자 여부: 상태에 따라 판별
    const isAdmin = role === "super_admin" || role === "content_admin";

    // ✅ 로그아웃 처리: localStorage 제거 + 이동
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("userRole");
        navigate("/");
    };

    return (
        <header className="grid grid-cols-3 items-center px-6 py-4 border-b border-gray-200 bg-white">
            {/* ✅ 왼쪽: 로고 클릭 시 홈으로 이동 */}
            <div className="flex items-center">
                <Link to="/" className="flex items-center">
                    <img src={logo} alt="narulab logo" className="h-5 w-auto" />
                </Link>
            </div>

            {/* ✅ 가운데: 공통 네비게이션 메뉴 */}
            <nav
                className="
                    flex justify-center flex-wrap gap-x-6 gap-y-2 
                    text-sm sm:text-base font-medium
                "
            >
                {/* ✅ 메뉴 항목: 화면이 넓을 때는 가로 한 줄, 좁아질수록 2개씩 2줄로 줄바꿈됨 */}
                <Link to="/notice" className="hover:text-blue-500">Notice</Link>
                <Link to="/product" className="hover:text-blue-500">Product</Link>
                <Link to="/qna" className="hover:text-blue-500">QnA</Link>
                <Link to="/contact" className="hover:text-blue-500">Contact</Link>
            </nav>

            {/* ✅ 오른쪽: 관리자 메뉴 + 로그인/로그아웃 */}
            <div className="flex justify-end items-center gap-4">
                {/* ✅ 관리자 전용 메뉴: 로그인 상태 + 관리자 권한일 때만 노출 */}
                {isLoggedIn && isAdmin && (
                    <Link
                        to="/admin"
                        className="text-blue-500 hover:underline flex items-center gap-1"
                    >
                        <Shield size={16} /> 관리자 페이지
                    </Link>
                )}

                {/* ✅ 로그인 상태에 따른 버튼 표시 */}
                {!isLoggedIn ? (
                    // ✅ 로그인 상태가 아니라면 로그인 버튼 표시
                    <Link
                        to="/login"
                        className="group relative flex items-center justify-center w-24 h-10"
                    >
                        {/* ✅ 로그인 버튼 배경 애니메이션 */}
                        <div
                            className="absolute inset-0 rounded-full bg-blue-500 opacity-0 scale-95 
                                group-hover:opacity-100 group-hover:scale-100 
                                transition-all duration-300 ease-in-out"
                        ></div>
                        <div className="relative z-10 flex items-center gap-1 text-blue-500 group-hover:text-white transition-colors duration-300">
                            <LogIn size={16} className="transition-colors group-hover:text-white" />
                            Login
                        </div>
                    </Link>
                ) : (
                    // ✅ 로그인 상태라면 로그아웃 버튼 표시
                    <button
                        onClick={handleLogout}
                        className="group relative flex items-center justify-center w-24 h-10"
                    >
                        {/* ✅ 로그아웃 버튼 배경 애니메이션 */}
                        <div
                            className="absolute inset-0 rounded-full bg-blue-500 opacity-0 scale-95 
                                group-hover:opacity-100 group-hover:scale-100 
                                transition-all duration-300 ease-in-out"
                        ></div>
                        <div className="relative z-10 flex items-center gap-1 text-blue-500 group-hover:text-white transition-colors duration-300">
                            <LogOut size={16} className="transition-colors group-hover:text-white" />
                            Logout
                        </div>
                    </button>
                )}
            </div>
        </header>
    );
}
