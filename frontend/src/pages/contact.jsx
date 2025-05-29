import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";  // ✅ motion import 추가

export default function ContactPage() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans"
        >

            {/* ✅ 본문 */}
            <main className="max-w-3xl mx-auto px-4 py-12">
                <h1 className="text-3xl font-bold mb-6">Contact</h1>
                <ul className="text-lg space-y-3">
                    <li><strong>회사명:</strong> ACG</li>
                    <li><strong>주소:</strong> 서울특별시 중구 을지로 123, 10층</li>
                    <li><strong>전화번호:</strong> 02-1234-5678</li>
                    <li><strong>이메일:</strong> contact@acg.co.kr</li>
                </ul>
            </main>
        </motion.div>
    );
}
