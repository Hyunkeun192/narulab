// src/main.jsx

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// ✅ 페이지 컴포넌트 import
import Home from "./pages/home";
import Notice from "./pages/notice";
import Product from "./pages/product";
import QnAPage from "./pages/qna";
import ContactPage from "./pages/contact";
import LoginPage from "./pages/login";
import SignupPage from "./pages/signup";
import ForgotPassword from "./pages/ForgotPassword";
import NotFound from "./pages/NotFound";
import AdminHome from "./pages/admin_home";
import QuestionForm from "./pages/admin/aptitude/QuestionForm";
import AssignQuestionsToTest from "./pages/admin/aptitude/AssignQuestionsToTest";
import TestManage from "./pages/admin/tests/TestManage";
import QuestionList from "./pages/admin/aptitude/QuestionList";
import TestEdit from "./pages/admin/tests/TestEdit";
import NormManage from "./pages/admin/norms/NormManage";
import ReportRuleManage from "./pages/admin/reports/ReportRuleManage";
import ReportResult from "./pages/user/ReportResult";
import ReportHistory from "./pages/user/ReportHistory";
import StenChart from "./pages/admin/statistics/StenChart";
import ReportListSchool from "./pages/school/reports/ReportList";
import ReportListCompany from "./pages/company/reports/ReportList";
import ProductStart from "./pages/product/ProductStart";
import ProductExample from "./pages/product/ProductExample";
import ProductExam from "./pages/product/ProductExam";

// ✅ 공통 레이아웃 import
import MainLayout from "./layouts/MainLayout";

import "./index.css";

// ✅ 라우트 정보 배열 정의 (MainLayout이 필요한 경로만)
const routes = [
  { path: "/", element: <Home /> },
  { path: "/notice", element: <Notice /> },
  { path: "/product", element: <Product /> },
  { path: "/qna", element: <QnAPage /> },
  { path: "/contact", element: <ContactPage /> },

  {
    path: "/admin",
    element: <AdminHome />,
    children: [
      // ✅ /admin 진입 시 /admin/home으로 리디렉션
      { path: "", element: <Navigate to="home" replace /> },
      { path: "home", element: <div className="text-xl font-semibold">관리자 홈입니다</div> },
      { path: "aptitude/questions", element: <QuestionForm /> },
      { path: "aptitude/assign", element: <AssignQuestionsToTest /> },
      { path: "aptitude/questions/list", element: <QuestionList /> },
      { path: "tests/manage", element: <TestManage /> },
      { path: "tests/:testId/edit", element: <TestEdit /> },
      { path: "norms", element: <NormManage /> },
      { path: "reports/manage", element: <ReportRuleManage /> },
      { path: "statistics/sten", element: <StenChart /> },
    ],
  },

  { path: "/user/report", element: <ReportResult /> },
  { path: "/user/reports", element: <ReportHistory /> },
  { path: "/school/reports", element: <ReportListSchool /> },
  { path: "/company/reports", element: <ReportListCompany /> },
  { path: "*", element: <NotFound /> },
];

// ✅ AppRoutes 컴포넌트 정의
const AppRoutes = () => (
  <Routes>
    {/* ✅ 인증 페이지 (MainLayout 없이 단독 렌더링) */}
    <Route path="/login" element={<LoginPage />} />
    <Route path="/signup" element={<SignupPage />} />
    <Route path="/forgot-password" element={<ForgotPassword />} />
    <Route path="/product/:test_id/start" element={<ProductStart />} />
    <Route path="/product/:test_id/example" element={<ProductExample />} />
    <Route path="/product/:test_id/exam" element={<ProductExam />} />


    {/* ✅ MainLayout 적용되는 나머지 경로들 */}
    <Route
      path="/*"
      element={
        <MainLayout>
          <Routes>
            {routes.map(({ path, element, children }) =>
              children ? (
                <Route key={path} path={path} element={element}>
                  {children.map((child) => (
                    <Route
                      key={`${path}/${child.path}`}
                      path={child.path}
                      element={child.element}
                    />
                  ))}
                </Route>
              ) : (
                <Route key={path} path={path} element={element} />
              )
            )}
          </Routes>
        </MainLayout>
      }
    />
  </Routes>
);

// ✅ 렌더링 시작
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </React.StrictMode>
);

