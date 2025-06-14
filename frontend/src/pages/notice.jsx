import React, { useEffect, useState } from "react";
import { useUser } from "../hooks/useUser"; // ✅ 로그인 사용자 정보 가져오는 훅
import axios from "axios";
import { motion } from "framer-motion"; // ✅ 페이지 전환 애니메이션

export default function Notice() {
    const user = useUser();

    // ✅ 로그인 여부와 super admin 여부를 명확하게 분리해서 판별
    const isLoggedIn = !!user?.id;
    const isSuperAdmin = !!user?.is_super_admin;

    const [notices, setNotices] = useState([]); // ✅ 공지사항 목록 상태
    const [showModal, setShowModal] = useState(false); // ✅ 모달 표시 여부
    const [editingNotice, setEditingNotice] = useState(null); // ✅ 수정 중인 공지 저장
    const [form, setForm] = useState({ title: "", content: "" }); // ✅ 폼 입력 상태

    // ✅ 공지사항 전체 조회
    useEffect(() => {
        axios
            .get("/api/notices")
            .then((res) => setNotices(res.data))
            .catch((err) => {
                console.error("공지사항 불러오기 실패:", err);
                setNotices([]);
            });
    }, []);

    // ✅ 공지 등록 모달 열기 (등록 모드)
    const openCreateModal = () => {
        setEditingNotice(null);
        setForm({ title: "", content: "" });
        setShowModal(true);
    };

    // ✅ 공지 수정 모달 열기
    const openEditModal = (notice) => {
        setEditingNotice(notice);
        setForm({ title: notice.title, content: notice.content });
        setShowModal(true);
    };

    // ✅ 등록 또는 수정 요청 처리
    const handleSubmit = async () => {
        try {
            if (editingNotice) {
                // ✅ 수정 요청
                const res = await axios.put(`/api/notices/${editingNotice.id}`, form);
                setNotices((prev) =>
                    prev.map((n) => (n.id === editingNotice.id ? res.data : n))
                );
            } else {
                // ✅ 신규 등록 요청
                const res = await axios.post("/api/notices", form);
                setNotices((prev) => [res.data, ...prev]);
            }
            setShowModal(false);
        } catch (err) {
            console.error("등록/수정 실패:", err);
        }
    };

    // ✅ 삭제 요청
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

                {/* ✅ 로그인 + super admin만 공지 등록 버튼 표시 */}
                {isLoggedIn && isSuperAdmin && (
                    <div className="mb-6 text-right">
                        <button
                            onClick={openCreateModal}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            + 공지 등록
                        </button>
                    </div>
                )}

                {/* ✅ 공지 목록 출력 */}
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

                                {/* ✅ 로그인 + super admin만 수정/삭제 버튼 표시 */}
                                {isLoggedIn && isSuperAdmin && (
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

            {/* ✅ 모달은 로그인 + super admin만 접근 가능 */}
            {isLoggedIn && isSuperAdmin && showModal && (
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
