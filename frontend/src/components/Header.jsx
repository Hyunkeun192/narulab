import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogIn, LogOut, Shield } from "lucide-react"; // ✅ 관리자 아이콘
import logo from "../assets/logo.png"; // ✅ 로고 이미지

export default function Header() {
    const navigate = useNavigate();

    // ✅ 로그인 여부와 사용자 권한 상태 관리
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [role, setRole] = useState(null);

    // ✅ 로그인 상태 동기화 및 이벤트 기반 갱신
    useEffect(() => {
        const syncLoginState = () => {
            const token = localStorage.getItem("accessToken");
            const userRole = localStorage.getItem("userRole");
            setIsLoggedIn(!!token);
            setRole(userRole);
        };

        syncLoginState(); // 최초 마운트 시 상태 설정
        window.addEventListener("login-success", syncLoginState); // 로그인 성공 이벤트 감지

        return () => {
            window.removeEventListener("login-success", syncLoginState);
        };
    }, []);

    // ✅ 관리자 여부 판별
    const isAdmin = role === "super_admin" || role === "content_admin";

    // ✅ 로그아웃 처리 함수
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("userRole");
        setIsLoggedIn(false);
        setRole(null);
        navigate("/"); // 홈으로 이동
    };

    return (
        <header className="grid grid-cols-3 items-center px-6 py-4 border-b border-gray-200 bg-white">
            {/* ✅ 왼쪽: 로고 */}
            <div className="flex items-center">
                <Link to="/" className="flex items-center">
                    <img src={logo} alt="narulab logo" className="h-5 w-auto" />
                </Link>
            </div>

            {/* ✅ 가운데: 공통 네비게이션 메뉴 + 관리자 메뉴 조건부 포함 */}
            <nav
                className="flex flex-nowrap justify-center w-full gap-x-10 text-sm sm:text-base font-medium"
            >
                <Link to="/notice" className="w-12 text-center">Notice</Link>
                <Link to="/product" className="w-12 text-center">Product</Link>
                <Link to="/qna" className="w-12 text-center">QnA</Link>
                <Link to="/contact" className="w-12 text-center">Contact</Link>

                {/* ✅ 관리자 로그인 시에만 중앙 메뉴에 표시 */}
                {isLoggedIn && isAdmin && (
                    <Link to="/admin" className="w-12 text-center text-blue-500 hover:underline whitespace-nowrap">
                        Admin Page
                    </Link>
                )}
            </nav>

            {/* ✅ 오른쪽: 로그인 / 로그아웃 버튼 */}
            <div className="flex justify-end items-center gap-4">
                {/* ✅ 로그인 전: 로그인 버튼 */}
                {!isLoggedIn ? (
                    <Link
                        to="/login"
                        className="group relative flex items-center justify-center w-24 h-10"
                    >
                        <div className="absolute inset-0 rounded-full bg-blue-500 opacity-0 scale-95 
                            group-hover:opacity-100 group-hover:scale-100 
                            transition-all duration-300 ease-in-out"
                        ></div>
                        <div className="relative z-10 flex items-center gap-1 text-blue-500 group-hover:text-white transition-colors duration-300">
                            <LogIn size={16} className="transition-colors group-hover:text-white" />
                            Login
                        </div>
                    </Link>
                ) : (
                    // ✅ 로그인 후: 로그아웃 버튼
                    <button
                        onClick={handleLogout}
                        className="group relative flex items-center justify-center w-24 h-10"
                    >
                        <div className="absolute inset-0 rounded-full bg-blue-500 opacity-0 scale-95 
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
