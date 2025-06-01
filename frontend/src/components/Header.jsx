import React from "react";
import { Link, useNavigate } from "react-router-dom"; // ✅ navigate 추가
import { LogIn, LogOut } from "lucide-react"; // ✅ 로그인/로그아웃 아이콘 추가
import logo from "../assets/logo.png"; // ✅ 로고 이미지 import

export default function Header() {
    const navigate = useNavigate();

    // ✅ 로그인 여부 판단 (accessToken 존재 여부)
    const isLoggedIn = !!localStorage.getItem("accessToken");

    // ✅ 로그아웃 처리
    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        navigate("/");
    };

    return (
        <header className="grid grid-cols-3 items-center px-6 py-4 border-b border-gray-200 bg-white">
            {/* ✅ 왼쪽: 로고 */}
            <div className="flex items-center">
                <Link to="/" className="flex items-center">
                    <img src={logo} alt="narulab logo" className="h-5 w-auto" />
                </Link>
            </div>

            {/* ✅ 가운데: 네비게이션 메뉴 (작은 화면에서도 유지) */}
            <nav className="flex justify-center flex-wrap gap-x-4 md:gap-x-8 text-sm md:text-base font-medium">
                <Link to="/notice" className="hover:text-blue-500">Notice</Link>
                <Link to="/product" className="hover:text-blue-500">Product</Link>
                <Link to="/qna" className="hover:text-blue-500">QnA</Link>
                <Link to="/contact" className="hover:text-blue-500">Contact</Link>
            </nav>

            {/* ✅ 오른쪽: 로그인 또는 로그아웃 */}
            <div className="flex justify-end items-center">
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
