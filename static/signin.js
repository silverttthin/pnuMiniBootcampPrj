   document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault(); // 기본 폼 제출 동작 방지

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const data = {
                login_id: username,
                password: password
            };


            fetch('/auth/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.jwt_token) {

                     // 로그인 폼 숨기기
                    document.getElementById('loginContainer').style.display = 'none';
                    document.getElementById('signupButton').style.display = 'none';

                    // JWT 토큰 디코딩 (Base64 -> JSON)
                    const decodedToken = decodeJWT(data.jwt_token);


                    // HTML에서 토큰 표시
                    document.getElementById('tokenDisplay').innerHTML = ` ${decodedToken.username}님 환영합니다!`;

                    // 로그아웃 버튼 표시
                    document.getElementById('logoutButton').style.display = 'block';

                } else {
                    // 토큰이 없거나 로그인 실패 시 처리
                    alert("ID와 PW를 확인하세요")
                    location.reload(true);
                    console.error('로그인 실패:', data.message);

                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('서버와의 통신 중 오류가 발생했습니다.');
            });
        });



 // JWT 디코딩 함수 (Base64로 인코딩된 부분을 디코딩)
        function decodeJWT(token) {
            const base64Url = token.split('.')[1];  // JWT의 payload 부분 추출
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // URL-safe Base64 디코딩을 위한 변환
            const jsonPayload = decodeBase64(base64);
            return JSON.parse(jsonPayload);
        }

           // Base64 디코딩 함수
        function decodeBase64(base64) {
            const decodedData = atob(base64);  // 브라우저에서 제공하는 atob() 함수 사용
            return decodedData;
        }

          // 로그아웃 버튼 클릭 시 처리
    document.getElementById('logoutBtn').addEventListener('click', function() {
        // 로그아웃 요청을 보내기 위한 fetch 호출
        fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                // 로그아웃 성공 시, 홈 화면으로 리다이렉트
                window.location.href = '/';  // 홈 화면으로 리다이렉트
            } else {
                console.error('로그아웃 실패');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });