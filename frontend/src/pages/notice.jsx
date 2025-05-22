import React from "react";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/useUser"; // ✅ 공통 훅으로 분리된 useUser

export default function Notice() {
    const user = useUser();
    const isAdmin = user?.is_super_admin;

    return (
        <div className="min-h-screen bg-white text-gray-900 font-sans">
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

            <main className="max-w-3xl mx-auto px-4 py-10">
                <h1 className="text-3xl font-bold mb-6 text-center">공지사항</h1>

                {isAdmin && (
                    <div className="mb-6 text-right">
                        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                            + 공지 등록
                        </button>
                    </div>
                )}

                <p className="text-gray-500 text-center">등록된 공지사항이 없습니다.</p>
            </main>
        </div>
    );
}
