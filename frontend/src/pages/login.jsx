// ✅ 로그인 페이지 컴포넌트: 사용자 이메일과 비밀번호 입력을 받아 로그인 처리
import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion"; // ✅ 페이지 진입/이탈 애니메이션 효과를 위한 모듈

export default function LoginPage() {
    const navigate = useNavigate(); // ✅ 로그인 성공 시 /mypage로 이동을 위한 라우팅 기능

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
            // ✅ 로그인 요청
            await axios.post("/api/login", { email, password });

            // ✅ 사용자 정보 요청 (로그인 확인 후 사용자 상태 저장 등 추가 가능)
            await axios.get("/api/me");

            // ✅ 마이페이지로 이동
            navigate("/mypage");
        } catch (err) {
            // ✅ 로그인 실패 시 오류 메시지 표시
            setError("이메일 또는 비밀번호가 올바르지 않습니다.");
        } finally {
            setLoading(false);
        }
    };

    return (
        // ✅ 페이지 전환 애니메이션 적용
        <motion.div
            initial={{ opacity: 0, y: 20 }} // 시작 상태: 약간 아래에서 투명
            animate={{ opacity: 1, y: 0 }}   // 나타날 때: 정위치에서 보이게
            exit={{ opacity: 0, y: -20 }}    // 사라질 때: 위로 빠져나감
            transition={{ duration: 0.3 }}   // 전환 시간
            className="min-h-screen bg-[#FAFAFA] text-gray-900 flex flex-col" // ✅ 전체 배경 설정 + flex로 헤더 + 본문 분리
        >

            {/* ✅ 로그인 박스: 화면 정중앙에 정렬 */}
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="w-full max-w-md bg-white border border-gray-200 rounded-md p-8 shadow-sm">
                    {/* ✅ 로그인 타이틀 */}
                    <h2 className="text-2xl font-semibold text-center mb-6">로그인</h2>

                    {/* ✅ 입력 필드 및 버튼 */}
                    <div className="mt-12">
                        {/* ✅ 이메일 입력 필드 */}
                        <input
                            type="email"
                            placeholder="이메일"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border border-[#CCCCCC] rounded text-sm"
                        />

                        {/* ✅ 비밀번호 입력 필드 */}
                        <div className="mt-3"></div>
                        <input
                            type="password"
                            placeholder="비밀번호"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border border-[#CCCCCC] rounded text-sm"
                        />

                        {/* ✅ 에러 메시지 표시 */}
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

                        {/* ✅ 하단 링크: 비밀번호 찾기 및 회원가입 이동 */}
                        <div className="mt-4"></div>
                        <div className="flex justify-between text-sm text-gray-500 pt-2">
                            <Link to="/find-password" className="text-blue-500 hover:underline">
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
