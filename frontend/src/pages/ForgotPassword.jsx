import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // ✅ 실제 API 요청을 위한 axios 사용

const ForgotPassword = () => {
    const navigate = useNavigate();

    // ✅ 이메일 입력 상태
    const [email, setEmail] = useState('');
    // ✅ 사용자에게 보여줄 메시지 (성공 또는 오류)
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(false); // ✅ 요청 중 여부

    // ✅ 이메일 입력 핸들러
    const handleChange = (e) => {
        setEmail(e.target.value);
    };

    // ✅ 비밀번호 찾기 제출 핸들러
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email) {
            setMessage('이메일을 입력해주세요.');
            return;
        }

        try {
            setLoading(true);
            setMessage(null);

            // ✅ 실제 비밀번호 재설정 요청 API 호출
            const response = await axios.post('/api/password/forgot', { email });

            // ✅ 성공 메시지 표시
            setMessage(response.data.message || '입력하신 이메일로 재설정 링크를 보냈습니다.');
        } catch (error) {
            // ✅ 에러 메시지 처리
            if (error.response && error.response.data && error.response.data.message) {
                setMessage(error.response.data.message);
            } else {
                setMessage('오류가 발생했습니다. 다시 시도해주세요.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#FAFAFA] px-4">
            {/* ✅ 중앙 정렬된 카드 */}
            <div className="bg-white w-full max-w-md p-8 shadow-sm rounded">
                {/* ✅ 상단 제목 */}
                <h2 className="text-2xl font-semibold mb-6 text-center">비밀번호 찾기</h2>

                {/* ✅ 이메일 입력 폼 */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="email" className="block text-sm text-gray-600 mb-1">
                            이메일 주소
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={handleChange}
                            placeholder="your@email.com"
                            className="w-full px-3 py-2 border border-[#CCCCCC] rounded-sm text-sm focus:outline-none focus:ring focus:border-blue-300"
                        />
                    </div>

                    {/* ✅ 메시지 영역 (성공/실패 모두 포함) */}
                    {message && (
                        <p className="text-sm text-gray-500 mt-1">{message}</p>
                    )}

                    {/* ✅ 제출 버튼 */}
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-2 text-white text-sm rounded-sm transition ${loading ? 'bg-blue-300' : 'bg-[#007AFF] hover:bg-blue-600'
                            }`}
                    >
                        {loading ? '전송 중...' : '비밀번호 재설정 메일 보내기'}
                    </button>
                </form>

                {/* ✅ 로그인 페이지로 돌아가기 */}
                <div className="mt-6 text-center text-sm text-gray-600">
                    <span>로그인 화면으로 돌아가기 </span>
                    <button
                        type="button"
                        onClick={() => navigate('/login')}
                        className="text-[#007AFF] hover:underline"
                    >
                        로그인
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
