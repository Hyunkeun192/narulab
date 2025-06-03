import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogIn, LogOut, Shield } from "lucide-react"; // ✅ 관리자 아이콘 추가
import logo from "../assets/logo.png"; // ✅ 로고 이미지 import

export default function Header() {
    const navigate = useNavigate();

    // ✅ 로그인 여부 판단 (accessToken 존재 여부)
    const isLoggedIn = !!localStorage.getItem("accessToken");

    // ✅ 관리자 여부 판단: localStorage에 저장된 userRole 값을 확인
    const role = localStorage.getItem("userRole"); // 예: 'super_admin', 'content_admin'
    const isAdmin = role === "super_admin" || role === "content_admin"; // ✅ super 또는 content 관리자만 true

    // ✅ 로그아웃 처리: accessToken과 userRole 모두 삭제
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

                {/* ✅ 관리자 전용 admin 메뉴: 로그인 + 관리자 권한일 때만 노출 */}
                {isLoggedIn && isAdmin && (
                    <button
                        onClick={() => navigate("/admin")}
                        className="text-blue-500 hover:underline flex items-center gap-1"
                    >
                        <Shield size={16} /> Admin
                    </button>
                )}
            </nav>

            {/* ✅ 오른쪽: 로그인 또는 로그아웃 버튼 */}
            <div className="flex justify-end items-center">
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
