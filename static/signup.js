// 폼 제출 이벤트 리스너 등록
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // 폼 기본 제출 동작 방지

    // 입력값 가져오기
    const loginId = document.getElementById('login_id').value;
    const password = document.getElementById('password').value;
    const name = document.getElementById('name').value;

    try {
        // POST 요청 전송 (엔드포인트 수정)
        const response = await fetch('/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                login_id: loginId,
                pwd: password, // 백엔드에서 pwd로 받음
                name: name
            })
        });

        // 응답 처리
        const result = await response.json();
        if (response.ok) {
            document.getElementById('message').textContent = "회원가입 성공!";
        } else {
            document.getElementById('message').textContent = `회원가입 실패: ${result.error || '알 수 없는 오류'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').textContent = "회원가입 중 에러 발생";
    }
});
