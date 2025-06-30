// src/api/testApi.js

import axios from "axios";

/**
 * 특정 검사에 연결된 문항 리스트를 불러옵니다.
 * @param {string} testId - 검사 ID
 * @returns {Promise<Array>} - 문항 + 보기 리스트
 */
export const getTestQuestions = async (testId) => {
    try {
        const response = await axios.get(`/api/admin/tests/${testId}/questions`);
        return response.data;
    } catch (error) {
        console.error("검사 문항 불러오기 실패:", error);
        throw error;
    }
};
