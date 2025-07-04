// ✅ 기존 파일 기반으로 수정 적용 완료
// ✅ 하드코딩된 지문 제거 + ExampleQuestion 컴포넌트 연동

import React from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import ExampleQuestion from "../../components/ExampleQuestion";

function ProductExample() {
    const { testId } = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const testName = location.state?.testName;

    const handleStartTest = () => {
        navigate(`/product/${testId}/exam`);
    };

    return (
        <div className="min-h-screen bg-gray-100 py-10 px-4 flex flex-col items-center">
            <ExampleQuestion testName={testName} onNext={handleStartTest} />
        </div>
    );
}

export default ProductExample;
