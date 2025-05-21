import React from "react";

export default function Notice() {
    return (
        <div className="max-w-3xl mx-auto px-4 py-10">
            <h1 className="text-3xl font-bold mb-6">공지사항</h1>
            <ul className="space-y-4">
                <li className="border-b pb-4">
                    <h2 className="text-xl font-semibold">[안내] 심리검사 시스템 점검 예정 (5/25)</h2>
                    <p className="text-sm text-gray-500">2025.05.20</p>
                    <p className="mt-2 text-gray-700">
                        안정적인 서비스 제공을 위해 시스템 점검이 진행될 예정입니다.
                    </p>
                </li>
                <li className="border-b pb-4">
                    <h2 className="text-xl font-semibold">[신규] 검사 리포트 요약 기능 출시</h2>
                    <p className="text-sm text-gray-500">2025.05.15</p>
                    <p className="mt-2 text-gray-700">
                        GPT 기반 리포트 요약 기능이 정식 출시되었습니다.
                    </p>
                </li>
            </ul>
        </div>
    );
}
