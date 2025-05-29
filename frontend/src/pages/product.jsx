import React from "react";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/useUser"; // 공통 사용자 정보 훅
import { motion } from "framer-motion"; // ✅ 추가

export default function Product() {
    const user = useUser();

    // ✅ 임의의 검사 정보 배열
    const testSections = [
        {
            title: "퍼스널리티 검사",
            tests: [
                { id: 1, name: "진로 적성 검사", items: 95, time: 10 },
                { id: 2, name: "직무 성향 분석", items: 90, time: 8 },
                { id: 3, name: "AI 자기소개서 분석", items: 100, time: 12 },
            ],
        },
        {
            title: "기업 맞춤형 검사",
            tests: [
                { id: 4, name: "삼성그룹 역량 진단", items: 85, time: 7 },
                { id: 5, name: "LG 조직 적응력 테스트", items: 100, time: 9 },
                { id: 6, name: "현대차 직무 중심 검사", items: 92, time: 11 },
            ],
        },
        {
            title: "자기계발 / 취업 준비",
            tests: [
                { id: 7, name: "이력서 클리닉 진단", items: 75, time: 6 },
                { id: 8, name: "면접 피드백 분석", items: 88, time: 10 },
                { id: 9, name: "취업 마인드셋 체크리스트", items: 60, time: 5 },
            ],
        },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans"
        >

            {/* Product List */}
            <main className="max-w-4xl mx-auto px-4 py-10">
                <h1 className="text-3xl font-bold text-center mb-10">검사 / 제품 목록</h1>

                <div className="space-y-12">
                    {testSections.map((section, index) => (
                        <section key={index}>
                            <h2 className="text-xl font-semibold border-b pb-1 mb-4">{section.title}</h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                                {section.tests.map((test) => (
                                    <Link
                                        key={test.id}
                                        to={`/tests/${test.id}`}
                                        className="block border rounded-lg p-4 shadow hover:shadow-md transition bg-gray-50 hover:bg-white"
                                    >
                                        <h3 className="text-lg font-semibold mb-1">{test.name}</h3>
                                        <p className="text-sm text-gray-600">문항 수: 약 {test.items}문항</p>
                                        <p className="text-sm text-gray-600">소요 시간: 약 {test.time}분</p>
                                    </Link>
                                ))}
                            </div>
                        </section>
                    ))}
                </div>
            </main>
        </motion.div>
    );
}
