// src/pages/notice.jsx

import React, { useEffect, useState } from "react";
import { useUser } from "../hooks/useUser"; // ✅ 로그인 사용자 정보 훅
import axios from "axios";
import { motion } from "framer-motion"; // ✅ 페이지 전환 애니메이션

export default function Notice() {
    const user = useUser();
    const isAdmin = user?.is_super_admin;

    const [notices, setNotices] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [editingNotice, setEditingNotice] = useState(null);
    const [form, setForm] = useState({ title: "", content: "" });

    // ✅ 공지사항 목록 불러오기
    useEffect(() => {
        axios
            .get("/api/notices")
            .then((res) => setNotices(res.data))
            .catch((err) => {
                console.error("공지사항 불러오기 실패:", err);
                setNotices([]);
            });
    }, []);

    // ✅ 공지 등록 버튼 클릭 시 초기화
    const openCreateModal = () => {
        setEditingNotice(null);
        setForm({ title: "", content: "" });
        setShowModal(true);
    };

    // ✅ 공지 수정 버튼 클릭 시 값 세팅
    const openEditModal = (notice) => {
        setEditingNotice(notice);
        setForm({ title: notice.title, content: notice.content });
        setShowModal(true);
    };

    // ✅ 공지 등록/수정 전송
    const handleSubmit = async () => {
        try {
            if (editingNotice) {
                // 수정
                const res = await axios.put(`/api/notices/${editingNotice.id}`, form);
                setNotices((prev) =>
                    prev.map((n) => (n.id === editingNotice.id ? res.data : n))
                );
            } else {
                // 새 공지 등록
                const res = await axios.post("/api/notices", form);
                setNotices((prev) => [res.data, ...prev]);
            }
            setShowModal(false);
        } catch (err) {
            console.error("등록/수정 실패:", err);
        }
    };

    // ✅ 공지 삭제
    const handleDelete = async (id) => {
        if (window.confirm("정말로 삭제하시겠습니까?")) {
            try {
                await axios.delete(`/api/notices/${id}`);
                setNotices((prev) => prev.filter((n) => n.id !== id));
            } catch (err) {
                console.error("삭제 실패:", err);
            }
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-white text-gray-900 font-sans"
        >
            {/* ✅ 공지사항 타이틀 */}
            <main className="max-w-3xl mx-auto px-4 py-10">
                <h1 className="text-3xl font-bold mb-6 text-center">공지사항</h1>

                {/* ✅ 관리자만 공지 등록 가능 */}
                {isAdmin && (
                    <div className="mb-6 text-right">
                        <button
                            onClick={openCreateModal}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            + 공지 등록
                        </button>
                    </div>
                )}

                {/* ✅ 공지 목록 */}
                {notices.length > 0 ? (
                    <ul className="space-y-4">
                        {notices.map((notice) => (
                            <li key={notice.id} className="border p-4 rounded shadow-sm">
                                <h2 className="text-xl font-semibold">{notice.title}</h2>
                                <p className="text-gray-700 mt-2 whitespace-pre-line">
                                    {notice.content}
                                </p>
                                <p className="text-sm text-gray-400 mt-1">
                                    작성일: {new Date(notice.created_at).toLocaleString()}
                                </p>

                                {/* ✅ 관리자에게만 수정/삭제 버튼 표시 */}
                                {isAdmin && (
                                    <div className="mt-2 flex gap-4">
                                        <button
                                            onClick={() => openEditModal(notice)}
                                            className="text-blue-600 text-sm hover:underline"
                                        >
                                            수정
                                        </button>
                                        <button
                                            onClick={() => handleDelete(notice.id)}
                                            className="text-red-500 text-sm hover:underline"
                                        >
                                            삭제
                                        </button>
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-gray-500 text-center">
                        등록된 공지사항이 없습니다.
                    </p>
                )}
            </main>

            {/* ✅ 공지 등록/수정 모달 */}
            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
                        <h2 className="text-xl font-bold mb-4">
                            {editingNotice ? "공지 수정" : "공지 등록"}
                        </h2>
                        <input
                            type="text"
                            placeholder="제목"
                            value={form.title}
                            onChange={(e) =>
                                setForm({ ...form, title: e.target.value })
                            }
                            className="w-full border px-3 py-2 rounded mb-3"
                        />
                        <textarea
                            placeholder="내용"
                            value={form.content}
                            onChange={(e) =>
                                setForm({ ...form, content: e.target.value })
                            }
                            className="w-full border px-3 py-2 rounded mb-4 h-32 resize-none"
                        />
                        <div className="flex justify-end gap-2">
                            <button
                                onClick={() => setShowModal(false)}
                                className="text-gray-500 hover:underline"
                            >
                                취소
                            </button>
                            <button
                                onClick={handleSubmit}
                                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                            >
                                {editingNotice ? "수정" : "등록"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </motion.div>
    );
}
