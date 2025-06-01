// src/pages/signup.jsx

import React, { useState, useEffect, useRef } from "react"; // ✅ useRef 추가
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion"; // ✅ motion 애니메이션 효과

// ✅ 랜덤 닉네임 4개 생성 함수
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

    const formatPhoneNumber = (value) => {
        const digits = value.replace(/\D/g, "");
        if (digits.length < 4) return digits;
        if (digits.length < 8) return `${digits.slice(0, 3)}-${digits.slice(3)}`;
        return `${digits.slice(0, 3)}-${digits.slice(3, 7)}-${digits.slice(7, 11)}`;
    };

    // ✅ 회원가입 단계 (0~4)
    const [step, setStep] = useState(0);
    const [email, setEmail] = useState("");
    const [emailValid, setEmailValid] = useState(false);
    const [emailExists, setEmailExists] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [phoneExists, setPhoneExists] = useState(false);
    const [nickname, setNickname] = useState("");
    const [nicknameCandidates, setNicknameCandidates] = useState([]);
    const [selectedNickname, setSelectedNickname] = useState("");
    const [nicknameExists, setNicknameExists] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [agreed, setAgreed] = useState(false); // ✅ 스크롤 동의 여부
    const [agreedOptional, setAgreedOptional] = useState(false); // 선택 동의 여부


    useEffect(() => {
        setNicknameCandidates(generateNicknames());
    }, []);

    const validateEmail = (value) =>
        /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(value);

    const isPasswordValid = () =>
        password.length >= 8 && password === passwordConfirm;

    // ✅ 이메일 중복 확인 요청
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

    // ✅ 전화번호 중복 확인 요청 함수
    const checkPhoneNumberDuplicate = async (value) => {
        try {
            const res = await axios.get(`/api/users/check-phone?phone=${value}`);
            setPhoneExists(!res.data.available);
        } catch {
            setPhoneExists(false);
        }
    };

    // ✅ 닉네임 중복 확인 요청 함수
    const checkNicknameDuplicate = async (value) => {
        try {
            const res = await axios.get(`/api/users/check-nickname?nickname=${value}`);
            setNicknameExists(!res.data.available);
        } catch {
            setNicknameExists(true);
        }
    };

    // ✅ 닉네임 중복 확인 디바운스 (0.5초)
    useEffect(() => {
        const timer = setTimeout(() => {
            if (nickname.length > 1) {
                checkNicknameDuplicate(nickname);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [nickname]);

    // ✅ 전화번호 중복 확인 디바운스 (0.5초)
    useEffect(() => {
        const timer = setTimeout(() => {
            if (phoneNumber.length >= 10) {
                checkPhoneNumberDuplicate(phoneNumber);
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [phoneNumber]);

    // ✅ 스크롤 참조 및 이벤트 처리
    const scrollRef = useRef(null);
    const handleScroll = () => {
        const el = scrollRef.current;
        if (el && el.scrollTop + el.clientHeight >= el.scrollHeight - 5) {
            setAgreed(true);
        }
    };

    const goToNextStep = () => {
        if (step === 1 && emailValid && !emailExists) setStep(2);
        else if (step === 2 && isPasswordValid()) setStep(3);
        else if (step === 3 && phoneNumber && !phoneExists) setStep(4);
    };

    // ✅ 최종 회원가입 제출 함수
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
        } catch (err) {
            const serverMessage = err.response?.data?.detail;
            if (serverMessage) {
                setError(serverMessage);
            } else {
                setError("회원가입에 실패했습니다.");
            }
        } finally {
            setLoading(false);
        }
    };

    // ✅ 전체 signup UI 렌더링
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen text-gray-900 flex flex-col"
        >
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="w-full max-w-md bg-gray-50 rounded-md p-8">

                    {/* ✅ Step 0: 개인정보 수집 및 이용 동의 */}
                    {step === 0 && (
                        <div>
                            <h2 className="text-2xl font-normal text-center mb-6">개인정보 수집 및 이용 동의</h2>
                            {/* 개인정보 수집 동의서 */}
                            <div className="h-64 overflow-y-auto border p-4 text-sm text-gray-700 bg-white rounded mb-4">
                                <p className="mb-2">
                                    'narulab' 서비스는 취업 준비생 여러분께 개인 맞춤형 인적성 검사 보고서를 제공하고, 더 나아가 유의미한 통계 분석 자료를 제공하여 서비스 품질을 향상하기 위해 다음과 같은 개인정보를 수집 및 이용합니다.
                                </p>
                                <strong className="block mt-2 mb-1">1. 수집하는 개인정보 항목</strong>
                                <ul className="list-disc list-inside mb-2">
                                    <li>필수 정보: 이메일 주소, 휴대폰 번호, 비밀번호</li>
                                    <li>선택 정보: 소속 학교, 취업 희망 회사, 선호 지역</li>
                                </ul>
                                <strong className="block mt-2 mb-1">2. 개인정보 수집 및 이용 목적</strong>
                                <ul className="list-disc list-inside mb-2">
                                    <li>
                                        <b>필수 정보</b>: 회원 식별, 본인 확인, 서비스 이용 및 관리, 인적성 검사 결과 보고서 제공, 안내 및 불만 처리 등
                                    </li>
                                    <li>
                                        <b>선택 정보</b>: 맞춤형 보고서 내 비교 통계, 서비스 개선을 위한 비식별 통계 분석
                                    </li>
                                </ul>
                                <strong className="block mt-2 mb-1">3. 개인정보의 보유 및 이용 기간</strong>
                                <p className="mb-2">
                                    회원님의 개인정보는 회원 탈퇴 시 또는 개인정보 수집 및 이용 목적이 달성된 후에는 지체 없이 파기됩니다. 단, 관련 법령의 규정에 따라 일정 기간 보존될 수 있습니다.
                                </p>
                                <strong className="block mt-2 mb-1">4. 선택 정보 제공에 대한 안내</strong>
                                <p>
                                    선택 정보를 제공하지 않으셔도 서비스 가입 및 인적성 검사 이용이 가능합니다. 다만 일부 비교 분석 기능 이용에 제한이 있을 수 있습니다.
                                </p>
                            </div>
                            {/* 필수/선택 동의 체크박스 */}
                            <div className="mb-4">
                                <label className="flex items-center mb-2">
                                    <input
                                        type="checkbox"
                                        checked={agreed}
                                        onChange={(e) => setAgreed(e.target.checked)}
                                        className="mr-2 accent-blue-600"
                                        required
                                    />
                                    <span className="text-sm text-gray-900">
                                        개인정보 수집 및 이용에 동의합니다 <span className="text-red-500">(필수)</span>
                                    </span>
                                </label>
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={!!agreedOptional}
                                        onChange={(e) => setAgreedOptional(e.target.checked)}
                                        className="mr-2 accent-blue-600"
                                    />
                                    <span className="text-sm text-gray-900">
                                        맞춤형 통계 분석(소속/희망회사/지역 제공)에 동의합니다 <span className="text-gray-400">(선택)</span>
                                    </span>
                                </label>
                            </div>
                            {/* 필수 동의 시에만 버튼 활성화 */}
                            <button
                                onClick={() => setStep(1)}
                                disabled={!agreed}
                                className="w-full mt-2 bg-[#007AFF] text-white py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    )}

                    {/* ✅ Step 1: 이메일 입력 */}
                    {step === 1 && (
                        <div>
                            <h2 className="text-2xl font-normal text-center mb-16">Email address</h2>
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => {
                                    const value = e.target.value;
                                    setEmail(value);
                                    setEmailValid(false);
                                    setEmailExists(false);
                                    if (validateEmail(value)) checkEmailDuplicate(value);
                                }}
                                className="w-full px-4 py-2 border border-[#CCCCCC] rounded-lg text-sm"
                            />
                            {email && !validateEmail(email) && (
                                <p className="text-sm text-red-500 mt-2">올바른 이메일 형식이 아닙니다.</p>
                            )}
                            {emailValid && !emailExists && (
                                <p className="text-sm text-green-600 mt-2">사용 가능한 이메일입니다.</p>
                            )}
                            {emailExists && (
                                <p className="text-sm text-red-500 mt-2">이미 사용 중입니다.</p>
                            )}
                            <button
                                onClick={goToNextStep}
                                disabled={!validateEmail(email) || emailExists}
                                className="w-full mt-8 bg-[#007AFF] text-white py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    )}

                    {/* ✅ Step 2: 비밀번호 입력 */}
                    {step === 2 && (
                        <div>
                            <h2 className="text-2xl font-normal text-center mb-16">비밀번호 설정</h2>
                            <input
                                type="password"
                                placeholder="비밀번호 (8자 이상)"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-2 border border-[#CCCCCC] rounded-lg text-sm"
                            />
                            <input
                                type="password"
                                placeholder="비밀번호 확인"
                                value={passwordConfirm}
                                onChange={(e) => setPasswordConfirm(e.target.value)}
                                className="w-full mt-3 px-4 py-2 border border-[#CCCCCC] rounded-lg text-sm"
                            />
                            {password && password.length < 8 && (
                                <p className="text-sm text-red-500 mt-2">8자 이상 입력해주세요.</p>
                            )}
                            {passwordConfirm && password !== passwordConfirm && (
                                <p className="text-sm text-red-500 mt-2">비밀번호가 일치하지 않습니다.</p>
                            )}
                            <button
                                onClick={goToNextStep}
                                disabled={!isPasswordValid()}
                                className="w-full mt-8 bg-[#007AFF] text-white py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    )}

                    {/* ✅ Step 3: 전화번호 입력 */}
                    {step === 3 && (
                        <div>
                            <h2 className="text-2xl font-normal text-center mb-16">휴대폰 번호</h2>
                            <input
                                type="text"
                                placeholder="휴대폰 번호"
                                value={formatPhoneNumber(phoneNumber)}
                                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, ""))}
                                className="w-full px-4 py-2 border border-[#CCCCCC] rounded-lg text-sm"
                            />
                            {phoneExists && (
                                <p className="text-sm text-red-500 mt-2">이미 사용 중인 번호입니다.</p>
                            )}
                            <button
                                onClick={goToNextStep}
                                disabled={!phoneNumber || phoneExists}
                                className="w-full mt-8 bg-[#007AFF] text-white py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                            >
                                다음
                            </button>
                        </div>
                    )}

                    {/* ✅ Step 4: 닉네임 입력 */}
                    {step === 4 && (
                        <div>
                            <h2 className="text-2xl font-normal text-center mb-16">닉네임 선택</h2>
                            <div className="grid grid-cols-2 gap-2 mb-16">
                                {nicknameCandidates.map((name) => (
                                    <button
                                        key={name}
                                        onClick={() => {
                                            setSelectedNickname(name);
                                            setNickname(name);
                                            setNicknameExists(false);
                                            setError("");
                                        }}
                                        className={`border px-3 py-1 rounded-lg text-sm ${selectedNickname === name
                                                ? "bg-blue-100 border-blue-500 text-blue-600"
                                                : "bg-white border-gray-300"
                                            }`}
                                    >
                                        {name}
                                    </button>
                                ))}
                            </div>
                            <input
                                type="text"
                                placeholder="직접 입력"
                                value={nickname}
                                onChange={(e) => {
                                    setNickname(e.target.value);
                                    setSelectedNickname("");
                                }}
                                className="w-full px-4 py-2 border border-[#CCCCCC] rounded-lg text-sm"
                            />
                            {nicknameExists && (
                                <p className="text-sm text-red-500 mt-2">이미 사용 중입니다.</p>
                            )}
                            {error && <p className="text-sm text-red-500 mt-2">{error}</p>}
                            <button
                                onClick={handleSubmit}
                                disabled={loading || (!nickname && !selectedNickname) || nicknameExists}
                                className="w-full mt-8 bg-[#007AFF] text-white py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                            >
                                {loading ? "가입 중..." : "가입 완료"}
                            </button>
                        </div>
                    )}

                </div>
            </div>
        </motion.div>
    );
}
