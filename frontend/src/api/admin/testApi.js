// src/api/admin/testApi.js

import api from "../api";

// ✅ 전체 검사 목록 불러오기
export const getTests = async () => {
    const res = await api.get("/api/admin/tests");
    return res.data;
};

// ✅ 개별 검사 조회 (수정 등)
export const getTestById = async (testId) => {
    const res = await api.get(`/api/admin/tests/${testId}`);
    return res.data;
};

// ✅ 검사 등록
export const createTest = async (testData) => {
    const res = await api.post("/api/admin/tests", testData);
    return res.data;
};

// ✅ 검사 수정
export const updateTest = async (testId, testData) => {
    const res = await api.put(`/api/admin/tests/${testId}`, testData);
    return res.data;
};

// ✅ 특정 검사에 연결된 문항 목록 불러오기
export const getTestQuestions = async (testId) => {
    const res = await api.get(`/api/admin/tests/${testId}/questions`);
    return res.data;
};

// ✅ 특정 검사에 문항 연결하기
export const assignQuestionsToTest = async (testId, questionIds) => {
    const res = await api.post(`/api/admin/tests/${testId}/assign-questions`, {
        question_ids: questionIds,
    });
    return res.data;
};
