import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

// ✅ 관리자 - 문항 등록 페이지
export default function QuestionForm() {
    const navigate = useNavigate();

    // ✅ 상태 정의
    const [instruction, setInstruction] = useState(""); // 지시문
    const [questionText, setQuestionText] = useState(""); // 문항 텍스트
    const [questionType, setQuestionType] = useState("text"); // 문항 유형
    const [isMultipleChoice, setIsMultipleChoice] = useState(false); // 복수 정답 여부
    const [questionImageUrl, setQuestionImageUrl] = useState(""); // 이미지 문항 URL
    const [questionImageFile, setQuestionImageFile] = useState(null); // 이미지 파일
    const [correctExplanation, setCorrectExplanation] = useState(""); // 정답 해설
    const [wrongExplanation, setWrongExplanation] = useState(""); // 오답 해설
    const [questionName, setQuestionName] = useState(""); // 문항 이름
    const [options, setOptions] = useState([
        { option_text: "", is_correct: false },
        { option_text: "", is_correct: false },
    ]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAddOption = () => {
        if (options.length < 5) {
            setOptions([...options, { option_text: "", is_correct: false }]);
        }
    };

    const handleRemoveOption = (index) => {
        if (options.length > 2) {
            const updated = [...options];
            updated.splice(index, 1);
            setOptions(updated);
        }
    };

    const handleOptionTextChange = (index, value) => {
        const updated = [...options];
        updated[index].option_text = value;
        setOptions(updated);
    };

    const handleCorrectToggle = (index) => {
        const updated = [...options];
        if (isMultipleChoice) {
            updated[index].is_correct = !updated[index].is_correct;
        } else {
            updated.forEach((opt, i) => {
                opt.is_correct = i === index;
            });
        }
        setOptions(updated);
    };

    // ✅ 이미지 S3 업로드 처리
    const uploadImageToS3 = async (file) => {
        const formData = new FormData();
        formData.append("file", file);
        try {
            const response = await axios.post("/api/admin/questions/upload-image", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });
            return response.data.image_url;
        } catch (err) {
            console.error("이미지 업로드 실패", err);
            alert("이미지 업로드 중 오류가 발생했습니다.");
            return null;
        }
    };

    // ✅ 문항 등록 제출 처리
    const handleSubmit = async () => {
        setLoading(true);
        setError("");

        try {
            const payload = {
                instruction,
                question_text: questionText,
                question_type: questionType,
                is_multiple_choice: isMultipleChoice,
                question_image_url: questionImageUrl || null,
                correct_explanation: correctExplanation,
                wrong_explanation: wrongExplanation,
                question_name: questionName,
                options: options.map((opt, idx) => ({
                    ...opt,
                    option_order: idx + 1  // ✅ 보기 순서 추가
                })),
                usage_type: "aptitude",
            };

            await axios.post("/api/admin/questions", payload, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            });

            alert("문항이 등록되었습니다.");
            navigate("/admin");
        } catch (err) {
            setError("문항 등록 중 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="max-w-3xl mx-auto px-4 py-10">
            <h1 className="text-2xl font-bold mb-6">문항 등록</h1>

            {/* 지시문 입력 */}
            <label className="block text-sm font-medium mb-1">지시문</label>
            <textarea
                className="w-full border rounded p-2 mb-4"
                value={instruction}
                onChange={(e) => setInstruction(e.target.value)}
                rows={2}
            />

            {/* 문항 텍스트 입력 */}
            <label className="block text-sm font-medium mb-1">문항 텍스트</label>
            <textarea
                className="w-full border rounded p-2 mb-4"
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                rows={2}
            />

            {/* 문항 이름 */}
            <label className="block text-sm font-medium mb-1">문항 이름</label>
            <input
                type="text"
                className="w-full border rounded p-2 mb-4"
                value={questionName}
                onChange={(e) => setQuestionName(e.target.value)}
                placeholder="예: 문항_001"
            />

            {/* 문항 유형 선택 */}
            <label className="block text-sm font-medium mb-1">문항 유형</label>
            <select
                className="w-full border rounded p-2 mb-4"
                value={questionType}
                onChange={(e) => setQuestionType(e.target.value)}
            >
                <option value="text">텍스트</option>
                <option value="image">이미지</option>
            </select>

            {/* 이미지 업로드 필드 */}
            {questionType === "image" && (
                <div className="mb-4">
                    <label className="block text-sm font-medium mb-1">이미지 업로드</label>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={async (e) => {
                            const file = e.target.files[0];
                            if (file) {
                                setQuestionImageFile(file);
                                const imageUrl = await uploadImageToS3(file);
                                if (imageUrl) {
                                    setQuestionImageUrl(imageUrl);
                                }
                            }
                        }}
                    />
                    {questionImageUrl && (
                        <img src={questionImageUrl} alt="preview" className="mt-2 max-h-48" />
                    )}
                </div>
            )}

            {/* 복수 정답 여부 */}
            <label className="flex items-center mb-4">
                <input
                    type="checkbox"
                    checked={isMultipleChoice}
                    onChange={(e) => setIsMultipleChoice(e.target.checked)}
                    className="mr-2"
                />
                복수 정답 허용
            </label>

            {/* 선택지 입력 */}
            <div className="mb-4">
                <label className="block text-sm font-medium mb-2">선택지</label>
                {options.map((opt, index) => (
                    <div key={index} className="flex items-center gap-2 mb-2">
                        <input
                            type="text"
                            className="flex-1 border rounded p-2"
                            placeholder={`선택지 ${index + 1}`}
                            value={opt.option_text}
                            onChange={(e) => handleOptionTextChange(index, e.target.value)}
                        />
                        <label className="flex items-center">
                            <input
                                type="checkbox"
                                checked={opt.is_correct}
                                onChange={() => handleCorrectToggle(index)}
                                className="mr-1"
                            />
                            정답
                        </label>
                        {options.length > 2 && (
                            <button
                                type="button"
                                className="text-red-500 text-sm"
                                onClick={() => handleRemoveOption(index)}
                            >
                                삭제
                            </button>
                        )}
                    </div>
                ))}
                {options.length < 5 && (
                    <button
                        type="button"
                        onClick={handleAddOption}
                        className="text-blue-500 text-sm mt-1"
                    >
                        + 선택지 추가
                    </button>
                )}
            </div>

            {/* 정답 해설 입력 */}
            <label className="block text-sm font-medium mb-1">정답 해설</label>
            <textarea
                className="w-full border rounded p-2 mb-4"
                value={correctExplanation}
                onChange={(e) => setCorrectExplanation(e.target.value)}
                rows={2}
            />

            {/* 오답 해설 입력 */}
            <label className="block text-sm font-medium mb-1">오답 해설</label>
            <textarea
                className="w-full border rounded p-2 mb-4"
                value={wrongExplanation}
                onChange={(e) => setWrongExplanation(e.target.value)}
                rows={2}
            />

            {/* 에러 메시지 */}
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            {/* 제출 버튼 */}
            <button
                onClick={handleSubmit}
                disabled={loading}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
            >
                {loading ? "등록 중..." : "문항 등록"}
            </button>
        </div>
    );
}
