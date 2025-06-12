// src/hooks/useUser.js

import { useEffect, useState } from "react";

export const useUser = () => {
    const [user, setUser] = useState(null); // ✅ 초기값은 null (비로그인 상태)

    useEffect(() => {
        try {
            // ✅ localStorage에 저장된 사용자 정보를 불러옴
            const userData = localStorage.getItem("userInfo");
            if (userData) {
                setUser(JSON.parse(userData)); // ✅ JSON 파싱 후 상태로 설정
            }
        } catch (err) {
            console.error("사용자 정보 파싱 오류:", err);
            setUser(null); // 오류 시 비로그인 처리
        }
    }, []);

    return user;
};
