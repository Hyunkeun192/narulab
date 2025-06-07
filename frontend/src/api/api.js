// src/api/api.js

import axios from "axios";

// ✅ accessToken을 매 요청 시마다 동적으로 삽입하는 인터셉터 포함
const api = axios.create({
    baseURL: "", // 상대 경로 기반 요청 처리 (예: "/api/...")
});

// ✅ 요청 인터셉터 설정: Authorization 헤더 자동 삽입
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("accessToken");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
