import React from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion"; // ✅ 애니메이션 관련 모듈 추가

export default function AdminHome() {
    const location = useLocation(); // ✅ 현재 경로 감지

    return (
        <div className="flex min-h-screen">
            {/* ✅ 좌측 사이드 메뉴 */}
            <aside className="w-52 flex-shrink-0 bg-gray-100 p-7 border-r">
                <h2 className="text-lg font-semibold mb-4">관리자 메뉴</h2>
                <nav className="flex flex-col gap-3 text-sm">
                    <Link to="/admin/tests/manage" className="hover:text-blue-500">검사 구성 관리</Link>
                    <Link to="/admin/aptitude/questions" className="hover:text-blue-500">적성검사 문항 등록</Link>
                    <Link to="/admin/personality/questions" className="hover:text-blue-500">인성검사 문항 등록</Link>
                    <Link to="/admin/norms" className="hover:text-blue-500">규준(Norm) 등록</Link>
                    <Link to="/admin/aptitude/questions/list" className="hover:text-blue-500">문항 리스트 / 수정</Link>
                    <Link to="/admin/norms" className="hover:text-blue-500">STEN 설정</Link>
                    <Link to="/admin/statistics/sten" className="hover:text-blue-500">STEN 통계</Link>
                    <Link to="/admin/reports/manage" className="hover:text-blue-500">리포트 기준 설정</Link>
                </nav>
            </aside>

            {/* ✅ 우측 콘텐츠 본문 (애니메이션 포함) */}
            <main className="flex-1 p-8">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={location.pathname}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                    >
                        <Outlet />
                    </motion.div>
                </AnimatePresence>
            </main>
        </div>
    );
}
