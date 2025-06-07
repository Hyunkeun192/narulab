import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"; // ✅ Navigate 추가

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

// ✅ 공통 레이아웃 import
import MainLayout from "./layouts/MainLayout";

import "./index.css";

// ✅ 라우트 정보 배열 정의
const routes = [
  { path: "/", element: <Home /> },
  { path: "/notice", element: <Notice /> },
  { path: "/product", element: <Product /> },
  { path: "/qna", element: <QnAPage /> },
  { path: "/contact", element: <ContactPage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/signup", element: <SignupPage /> },
  { path: "/forgot-password", element: <ForgotPassword /> },

  {
    path: "/admin",
    element: <AdminHome />,
    children: [
      // ✅ /admin 진입 시 /admin/home으로 리디렉션
      { path: "", element: <Navigate to="home" replace /> },

      // ✅ /admin/home 명시적 등록
      {
        path: "home",
        element: <div className="text-xl font-semibold">관리자 홈입니다</div>,
      },
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

// ✅ Routes만 그대로 렌더링
const AppRoutes = () => (
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
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </React.StrictMode>
);
