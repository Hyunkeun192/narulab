import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion"; // ✅ motion 애니메이션 효과

// ✅ 랜덤 닉네임 생성 함수
const generateNicknames = () => {
    const animals = ["호랑이", "펭귄", "여우", "토끼", "사자", "고양이", "부엉이", "하마"];
    return Array.from({ length: 4 }, () => {
        const animal = animals[Math.floor(Math.random() * animals.length)];
        const num = Math.floor(100 + Math.random() * 900);
        return `${animal}${num}`;
    });
};

export default function SignupPage() {
    const navigate = useNavigate();

    // ✅ 휴대폰 번호 하이픈 자동 삽입 함수
    const formatPhoneNumber = (value) => {
        const digits = value.replace(/\D/g, "");
        if (digits.length < 4) return digits;
        if (digits.length < 8) return `${digits.slice(0, 3)}-${digits.slice(3)}`;
        return `${digits.slice(0, 3)}-${digits.slice(3, 7)}-${digits.slice(7, 11)}`;
    };

    // ✅ 단계 상태
    const [step, setStep] = useState(1);

    // ✅ 입력 상태
    const [email, setEmail] = useState("");
    const [emailValid, setEmailValid] = useState(false);
    const [emailExists, setEmailExists] = useState(false);

    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] = useState("");

    const [phoneNumber, setPhoneNumber] = useState("");

    const [nickname, setNickname] = useState("");
    const [nicknameCandidates, setNicknameCandidates] = useState([]);
    const [selectedNickname, setSelectedNickname] = useState("");
    const [nicknameExists, setNicknameExists] = useState(false);

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    // ✅ 진입 시 닉네임 후보 생성
    useEffect(() => {
        setNicknameCandidates(generateNicknames());
    }, []);

    // ✅ 이메일 유효성 검사
    const validateEmail = (value) =>
        /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(value);
    const isPasswordValid = () =>
        password.length >= 8 && password === passwordConfirm;

    // ✅ 이메일 중복 체크
    const checkEmailDuplicate = async () => {
        if (!validateEmail(email)) {
            setEmailValid(false);
            setEmailExists(false);
            return;
        }
        try {
            const res = await axios.get(`/api/users/check-email?email=${email}`);
            setEmailExists(!res.data.available);
            setEmailValid(true);
        } catch {
            setEmailExists(true);
            setEmailValid(false);
        }
    };

    // ✅ 닉네임 중복 체크
    const checkNicknameDuplicate = async (value) => {
        try {
            const res = await axios.get(`/api/users/check-nickname?nickname=${value}`);
            setNicknameExists(!res.data.available);
        } catch {
            setNicknameExists(true);
        }
    };

    // ✅ 단계 이동
    const goToNextStep = () => {
        if (step === 1 && emailValid && !emailExists) setStep(2);
        else if (step === 2 && isPasswordValid()) setStep(3);
        else if (step === 3 && phoneNumber) setStep(4);
    };

    // ✅ 최종 제출
    const handleSubmit = async () => {
        setLoading(true);
        setError("");
        const finalNickname = nickname || selectedNickname;

        if (!finalNickname || nicknameExists) {
            setError("닉네임을 확인해주세요.");
            setLoading(false);
            return;
        }

        try {
            await axios.post("/api/signup", {
                email,
                password,
                password_confirm: passwordConfirm,
                phone_number: phoneNumber,
                nickname: finalNickname,
            });
            navigate("/login");
        } catch {
            setError("회원가입에 실패했습니다.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-[#FAFAFA] flex items-center justify-center px-4"
        >
            <div className="w-full max-w-xl bg-white rounded-2xl shadow p-10">
                
                {/* ✅ 1단계: 이메일 입력 */}
                {step === 1 && (
                    <div>
                        {/* ✅ 제목 + 입력 영역 */}
                            <h2 className="text-xl font-normal text-center">이메일을 입력해주세요.</h2>
                            {/* ✅ 이메일 입력 필드 */}

                        <div className="mt-12">
                            <input
                                type="email"
                                placeholder="이메일 입력"
                                value={email}
                                onChange={(e) => {
                                    const value = e.target.value;
                                    setEmail(value);
                                    setEmailValid(false);
                                    setEmailExists(false);

                                    // ✅ 입력 도중에도 유효하면 자동 중복 확인
                                    if (validateEmail(value)) {
                                        checkEmailDuplicate(value);
                                    }
                                }}
                                className="w-full px-0 py-4 border-b border-gray-400 bg-transparent text-lg focus:outline-none focus:border-blue-500 transition-all"
                            />

                            {/* ✅ 피드백 메시지 */}
                            {!validateEmail(email) && email && (
                                <p className="text-sm text-red-500">올바른 이메일 형식이 아닙니다.</p>
                            )}
                            {emailValid && !emailExists && (
                                <p className="text-sm text-green-600">사용 가능한 이메일입니다.</p>
                            )}
                            {emailExists && (
                                <p className="text-sm text-red-500">이미 사용 중입니다.</p>
                            )}
                        </div>

                        {/* ✅ 다음 버튼 */}
                        <div className="mt-12 flex justify-end">
                            <button
                                onClick={goToNextStep}
                                disabled={!validateEmail(email) || emailExists}
                                className="bg-[#007AFF] text-white px-6 py-1.5 text-sm rounded-md hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    </div>
                )}

                {/* ✅ 2단계: 비밀번호 입력 */}
                {step === 2 && (
                    <div>
                        
                            <h2 className="text-xl font-normal text-center">비밀번호를 입력해주세요.</h2>
                        <div className="mt-12">
                            <input
                                type="password"
                                placeholder="비밀번호 (8자 이상)"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-0 py-4 border-b border-gray-400 bg-transparent text-lg focus:outline-none focus:border-blue-500 transition-all"
                            />
                            <input
                                type="password"
                                placeholder="비밀번호 확인"
                                value={passwordConfirm}
                                onChange={(e) => setPasswordConfirm(e.target.value)}
                                className="w-full px-0 py-4 border-b border-gray-400 bg-transparent text-lg focus:outline-none focus:border-blue-500 transition-all"
                            />
                            {password && password.length < 8 && (
                                <p className="text-sm text-red-500">8자 이상 입력해주세요.</p>
                            )}
                            {password && passwordConfirm && password !== passwordConfirm && (
                                <p className="text-sm text-red-500">비밀번호가 일치하지 않습니다.</p>
                            )}
                            {isPasswordValid() && (
                                <p className="text-sm text-green-600">비밀번호가 유효합니다.</p>
                            )}
                        </div>

                        <div className="mt-12 flex justify-end">
                            <button
                                onClick={goToNextStep}
                                disabled={!isPasswordValid()}
                                className="bg-[#007AFF] text-white px-6 py-1.5 text-sm rounded-md hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    </div>
                )}

                {/* ✅ 3단계: 휴대폰 번호 입력 */}
                {step === 3 && (
                    <div>
                            <h2 className="text-xl font-normal text-center">휴대폰 번호를 입력해주세요.</h2>
                        <div className="mt-12">
                            <input
                                type="text"
                                placeholder="휴대폰 번호 입력"
                                value={formatPhoneNumber(phoneNumber)}
                                onChange={(e) =>
                                    setPhoneNumber(e.target.value.replace(/\D/g, ""))
                                }
                                className="w-full px-0 py-4 border-b border-gray-400 bg-transparent text-lg focus:outline-none focus:border-blue-500 transition-all"
                            />
                        </div>

                        <div className="mt-12 flex justify-end">
                            <button
                                onClick={goToNextStep}
                                disabled={!phoneNumber}
                                className="bg-[#007AFF] text-white px-6 py-1.5 text-sm rounded-md hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    </div>
                )}

                {/* ✅ 4단계: 닉네임 선택 */}
                {step === 4 && (
                    <div>
                            {/* ✅ 제목 */}
                            <h2 className="text-xl font-normal text-center">
                                닉네임을 선택해주세요. <span className="text-gray-400 text-base">(선택)</span>
                            </h2>
                        <div className="mt-12">
                        
                            {/* ✅ 추천 닉네임: 제목과 여유 있는 간격 확보 */}
                            <div className="mt-10 grid grid-cols-2 gap-2">
                                {nicknameCandidates.map((name) => (
                                    <button
                                        key={name}
                                        type="button"
                                        onClick={() => {
                                            setSelectedNickname(name); // 선택 상태로
                                            setNickname(name);         // 입력창에 자동 반영
                                            setNicknameExists(false);  // 에러 제거
                                            setError("");              // 기타 에러 제거
                                        }}
                                        className={`border px-3 py-1 rounded-full text-sm ${selectedNickname === name
                                                ? "border-blue-500 text-blue-600"
                                                : "border-gray-300"
                                            }`}
                                    >
                                        {name}
                                    </button>
                                ))}
                            </div>

                            {/* ✅ 직접 입력 */}
                        <div className="mt-12">
                            <input
                                type="text"
                                placeholder="직접 입력"
                                value={nickname}
                                onChange={(e) => {
                                    setNickname(e.target.value);
                                    setSelectedNickname(""); // 추천 선택 해제
                                    checkNicknameDuplicate(e.target.value); // 중복 검사만 직접 입력 시 실행
                                }}
                                className="w-full px-0 py-4 border-b border-gray-400 bg-transparent text-lg focus:outline-none focus:border-blue-500 transition-all"
                            />

                            {/* ✅ 메시지 영역 */}
                            {nicknameExists && (
                                <p className="text-sm text-red-500">이미 사용 중입니다.</p>
                            )}
                            {error && <p className="text-sm text-red-500">{error}</p>}
                        </div>
                    </div>

                        {/* ✅ 버튼 영역 */}
                        <div className="mt-12 flex justify-end">
                            <button
                                onClick={handleSubmit}
                                disabled={
                                    loading ||
                                    (!nickname && !selectedNickname) ||
                                    nicknameExists
                                }
                                className="bg-[#007AFF] text-white px-6 py-1.5 text-sm rounded-md hover:bg-blue-600 disabled:opacity-50"
                            >
                                {loading ? "가입 중..." : "가입 완료"}
                            </button>
                        </div>
                    </div>
                )}

            </div>
        </motion.div>
    );
}
