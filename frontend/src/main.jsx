// src/main.jsx

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

// ✅ 페이지 컴포넌트 import
import Home from "./pages/home";
import Notice from "./pages/notice";
import Product from "./pages/product";
import QnAPage from "./pages/qna";
import ContactPage from "./pages/contact";
import LoginPage from "./pages/login";
import SignupPage from "./pages/signup";
import ForgotPassword from "./pages/ForgotPassword"; // ✅ 추가: 비밀번호 찾기 페이지
import NotFound from "./pages/NotFound"; // ✅ 404 페이지

// ✅ 공통 레이아웃 import
import MainLayout from "./layouts/MainLayout";

import "./index.css";

// ✅ 라우트 정보 배열로 정의 (경로 + 렌더링 컴포넌트)
const routes = [
  { path: "/", element: <Home /> },
  { path: "/notice", element: <Notice /> },
  { path: "/product", element: <Product /> },
  { path: "/qna", element: <QnAPage /> },
  { path: "/contact", element: <ContactPage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/signup", element: <SignupPage /> },
  { path: "/forgot-password", element: <ForgotPassword /> }, // ✅ 추가된 경로
  { path: "*", element: <NotFound /> }, // ✅ 없는 경로 처리
];

// ✅ 콘텐츠 애니메이션만 감싸는 컴포넌트
const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    // ✅ 공통 Header 포함된 레이아웃으로 감쌈
    <MainLayout>
      <AnimatePresence mode="wait">
        {/* ✅ 페이지 콘텐츠 애니메이션 적용 대상 */}
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <Routes location={location}>
            {routes.map(({ path, element }) => (
              <Route key={path} path={path} element={element} />
            ))}
          </Routes>
        </motion.div>
      </AnimatePresence>
    </MainLayout>
  );
};

// ✅ React 렌더링 시작
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  </React.StrictMode>
);
