// frontend/src/pages/login.jsx

import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion"; // ✅ 페이지 진입/이탈 애니메이션 효과를 위한 모듈

export default function LoginPage() {
    const navigate = useNavigate(); // ✅ 로그인 성공 시 홈으로 이동

    // ✅ 상태 관리: 입력값 및 에러/로딩 상태
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    // ✅ 로그인 처리 함수
    const handleLogin = async () => {
        setLoading(true);
        setError("");

        try {
            const trimmedEmail = email.trim(); // ✅ 공백 제거

            // ✅ 로그인 요청 → 토큰 수신
            const res = await axios.post("/api/login", {
                email: trimmedEmail,
                password,
            });

            const token = res.data.access_token;

            // ✅ accessToken 이름으로 토큰 저장 (Header.jsx 기준과 일치)
            localStorage.setItem("accessToken", token);

            // ✅ 사용자 정보 요청 (/api/me) - 인증 헤더 포함
            const meRes = await axios.get("/api/me", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            // ✅ 사용자 role 정보 저장 → Header.jsx에서 관리자 조건 확인 가능
            localStorage.setItem("userRole", meRes.data.role); // ✅ 관리자 권한 체크용

            // ✅ 로그인 성공 알림 → Header.jsx에서 상태 변경 감지 용도
            window.dispatchEvent(new Event("login-success")); // ✅ 상태 리렌더링 트리거

            // ✅ 로그인 성공 → 홈으로 이동
            navigate("/");
        } catch (err) {
            setError("이메일 또는 비밀번호가 올바르지 않습니다.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }} // ✅ 진입 애니메이션 시작
            animate={{ opacity: 1, y: 0 }}   // ✅ 도착 상태
            exit={{ opacity: 0, y: -20 }}    // ✅ 퇴장 애니메이션
            transition={{ duration: 0.3 }}
            className="min-h-screen text-gray-900 flex flex-col"
        >
            {/* ✅ 로그인 박스 */}
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="w-full max-w-md bg-gray-50 rounded-md p-8">
                    <h2 className="text-2xl font-normal text-center mb-6">Login</h2>

                    {/* ✅ 입력 영역 */}
                    <div className="mt-12">
                        <input
                            type="email"
                            placeholder="Your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border border-[#CCCCCC] rounded text-sm"
                        />
                        <div className="mt-3"></div>
                        <input
                            type="password"
                            placeholder="Your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border border-[#CCCCCC] rounded text-sm"
                        />

                        {/* ✅ 에러 메시지 */}
                        {error && <p className="text-sm text-red-500">{error}</p>}

                        {/* ✅ 로그인 버튼 */}
                        <div className="mt-12"></div>
                        <button
                            onClick={handleLogin}
                            disabled={!email || !password || loading}
                            className="w-full bg-[#007AFF] text-white py-2 rounded hover:bg-blue-600 disabled:opacity-50"
                        >
                            {loading ? "로그인 중..." : "로그인"}
                        </button>

                        {/* ✅ 하단 링크 */}
                        <div className="mt-4"></div>
                        <div className="flex justify-between text-sm text-gray-500 pt-2">
                            <Link to="/forgot-password" className="text-blue-500 hover:underline">
                                비밀번호 찾기
                            </Link>
                            <Link to="/signup" className="text-blue-500 hover:underline">
                                회원가입
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
