document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // 기본 폼 제출 동작 방지

    // 사용자 입력값 추출
    const loginId = document.getElementById('login_id').value;
    const password = document.getElementById('password').value;

    try {
        // POST 요청 전송 (엔드포인트: /auth/signin)
        const response = await fetch('/auth/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                login_id: loginId,
                pwd: password  // 백엔드에서 pwd로 받음
            })
        });

        const result = await response.json();

        if (response.ok) {
            // 로그인 성공 시 서버에서 전달된 사용자 이름을 활용하여 화면 전체를 환영 메시지로 변경
            const userName = result.username; // 서버 응답 JSON에 name 필드가 있어야 합니다.

            document.body.innerHTML = `<div class="welcome-container"><h2>${userName}님 환영합니다</h2></div>`;
            console.log(result)
        } else {
            document.getElementById('login-message').textContent = `로그인 실패: ${result.error || '알 수 없는 오류'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('login-message').textContent = "로그인 중 에러 발생";
    }
});
