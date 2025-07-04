import React from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import ExampleQuestion from "../../components/ExampleQuestion";

function ProductExample() {
    const { test_id } = useParams();  // ✅ 라우트 파라미터에 맞게 수정
    const navigate = useNavigate();
    const location = useLocation();
    const testName = location.state?.testName;

    const handleStartTest = () => {
        navigate(`/product/${test_id}/exam`);  // ✅ 경로도 test_id로 맞춤
    };

    return (
        <div className="min-h-screen bg-gray-100 py-10 px-4 flex flex-col items-center">
            <ExampleQuestion testName={testName} onNext={handleStartTest} />
        </div>
    );
}

export default ProductExample;
