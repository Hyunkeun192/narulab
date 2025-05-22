// src/hooks/useUser.js

export function useUser() {
    return {
        id: 1,
        email: "admin@example.com",
        nickname: "관리자",
        is_super_admin: true,
        is_external_admin: false,
        is_content_admin: false,
    };
}
