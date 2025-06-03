// src/pages/admin/norms/NormManage.jsx

import React, { useEffect, useState } from "react";
import axios from "axios";

// ✅ 규준(STEN) 그룹 관리 페이지
export default function NormManage() {
    const [groupName, setGroupName] = useState("");
    const [description, setDescription] = useState("");
    const [message, setMessage] = useState("");
    const [norms, setNorms] = useState([]);

    const [stenRules, setStenRules] = useState([
        { min_score: 0, max_score: 9, sten: 1 },
        { min_score: 10, max_score: 19, sten: 2 },
        { min_score: 20, max_score: 29, sten: 3 },
        { min_score: 30, max_score: 39, sten: 4 },
        { min_score: 40, max_score: 49, sten: 5 },
        { min_score: 50, max_score: 59, sten: 6 },
        { min_score: 60, max_score: 69, sten: 7 },
        { min_score: 70, max_score: 79, sten: 8 },
        { min_score: 80, max_score: 89, sten: 9 },
        { min_score: 90, max_score: 100, sten: 10 },
    ]);

    const fetchNorms = async () => {
        try {
            const res = await axios.get("/api/admin/norms", {
                headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
            });
            setNorms(res.data);
        } catch {
            setMessage("규준 목록을 불러오지 못했습니다.");
        }
    };

    useEffect(() => {
        fetchNorms();
    }, []);

    const handleCreateNorm = async () => {
        if (!groupName) return;
        try {
            await axios.post(
                "/api/admin/norms",
                {
                    group_name: groupName,
                    description,
                    rules: stenRules,
                },
                {
                    headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
                }
            );
            setGroupName("");
            setDescription("");
            setMessage("규준이 등록되었습니다.");
            fetchNorms();
        } catch {
            setMessage("규준 등록 실패");
        }
    };

    const updateSten = (index, key, value) => {
        const updated = [...stenRules];
        updated[index][key] = key === "sten" ? parseInt(value) : value;
        setStenRules(updated);
    };

    return (
        <div className="max-w-5xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">규준 등록 및 STEN 설정</h1>

            {message && <p className="text-sm text-blue-600 mb-4">{message}</p>}

            <div className="mb-10 border p-4 rounded bg-gray-50">
                <h2 className="text-lg font-semibold mb-2">새 규준 등록</h2>

                <input
                    type="text"
                    placeholder="규준 그룹명"
                    className="w-full border p-2 mb-2 rounded"
                    value={groupName}
                    onChange={(e) => setGroupName(e.target.value)}
                />

                <textarea
                    placeholder="설명 (선택)"
                    className="w-full border p-2 mb-4 rounded"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={2}
                />

                {/* ✅ STEN 점수 범위 설정 */}
                <table className="w-full border text-sm mb-4">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="border p-2">최소 점수</th>
                            <th className="border p-2">최대 점수</th>
                            <th className="border p-2">STEN</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stenRules.map((rule, idx) => (
                            <tr key={idx}>
                                <td className="border p-1">
                                    <input
                                        type="number"
                                        value={rule.min_score}
                                        onChange={(e) => updateSten(idx, "min_score", parseInt(e.target.value))}
                                        className="w-full border rounded p-1"
                                    />
                                </td>
                                <td className="border p-1">
                                    <input
                                        type="number"
                                        value={rule.max_score}
                                        onChange={(e) => updateSten(idx, "max_score", parseInt(e.target.value))}
                                        className="w-full border rounded p-1"
                                    />
                                </td>
                                <td className="border p-1">
                                    <input
                                        type="number"
                                        min="1"
                                        max="10"
                                        value={rule.sten}
                                        onChange={(e) => updateSten(idx, "sten", e.target.value)}
                                        className="w-full border rounded p-1"
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* ✅ 오류 발생했던 버튼 → 수정 완료 */}
                <button
                    onClick={handleCreateNorm}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                >
                    규준 등록
                </button>
            </div>

            {/* ✅ 등록된 규준 목록 출력 */}
            <div>
                <h2 className="text-lg font-semibold mb-3">등록된 규준 그룹</h2>
                <ul className="space-y-3">
                    {norms.map((norm) => (
                        <li key={norm.norm_id} className="border p-4 rounded bg-white shadow-sm">
                            <div className="font-semibold mb-1">{norm.group_name}</div>
                            <div className="text-sm text-gray-600 mb-2">{norm.description}</div>
                        </li>
                    ))}
                    {norms.length === 0 && (
                        <p className="text-gray-500">등록된 규준이 없습니다.</p>
                    )}
                </ul>
            </div>
        </div>
    );
}
