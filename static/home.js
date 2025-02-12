document.addEventListener("DOMContentLoaded", function () {
    checkLoginStatus(); // 페이지 로드 시 로그인 상태 확인
});

// ✅ 햄버거 메뉴 열기
document.getElementById("menu-toggle").addEventListener("click", function () {
    document.getElementById("side-menu").style.right = "0";
});

// ✅ 메뉴 닫기
document.getElementById("close-menu").addEventListener("click", function () {
    document.getElementById("side-menu").style.right = "-300px";
});

// 로그인 폼 제출 이벤트
document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/auth/signin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                login_id: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error("서버 응답 오류");
        }

        const result = await response.json();

        if (result.jwt_token) {
            console.log("✅ 로그인 성공, 서버 응답:", result);
            alert("✅ 로그인 성공");

            // ✅ JWT 토큰 저장
            localStorage.setItem("jwt_token", result.jwt_token);

            // ✅ JWT에서 username 추출
            const decodedToken = decodeJWT(result.jwt_token);
            console.log("🔍 디코딩된 JWT:", decodedToken);

            const extractedUsername = decodedToken.username || decodedToken.name || decodedToken.sub;
            if (extractedUsername) {
                localStorage.setItem("username", extractedUsername);
                updateUIForLoggedInUser(extractedUsername);
            } else {
                console.warn("⚠️ JWT에 username 필드가 없음. 서버 응답 확인 필요.");
                alert("서버 응답에 username이 없습니다. 관리자에게 문의하세요.");
            }
        } else {
            alert("로그인 실패: " + (result.error || "잘못된 로그인 정보"));
        }
    } catch (error) {
        console.error("🔥 서버와의 통신 중 오류 발생:", error);
        console.error("🔍 오류 스택:", error.stack); // 추가
        alert("서버와의 통신 중 오류가 발생했습니다.");
    }
});

// ✅ JWT 토큰 기반으로 로그인 상태 확인
function checkLoginStatus() {
    const savedToken = localStorage.getItem("jwt_token");
    const savedUsername = localStorage.getItem("username");

    if (savedToken && savedUsername) {
        updateUIForLoggedInUser(savedUsername);
    }
}

// ✅ 로그인 후 UI 업데이트
function updateUIForLoggedInUser(username) {
    try {
        console.log("🔵 UI 업데이트 시작");

        // 요소들이 존재하는지 확인 후 스타일 변경
        const loginContainer = document.getElementById("loginContainer");
        const signupButton = document.getElementById("signupButton");
        const userActions = document.getElementById("userActions");
        const tokenDisplay = document.getElementById("tokenDisplay");

        if (loginContainer) loginContainer.style.display = "none";
        if (signupButton) signupButton.style.display = "none";
        if (userActions) userActions.style.display = "block";
        if (tokenDisplay) tokenDisplay.innerHTML = `<h2>${username}님 환영합니다!</h2>`;

        const loginLink = document.getElementById("loginLink");
        const signupLink = document.getElementById("signupLink");
        const myPlans = document.getElementById("myPlans");
        const logoutBtn = document.getElementById("logoutBtn");

        if (loginLink) loginLink.style.display = "none";
        if (signupLink) signupLink.style.display = "none";
        if (myPlans) myPlans.classList.remove("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");

        console.log("🟢 UI 업데이트 성공");
    } catch (error) {
        console.error("❌ UI 업데이트 중 오류 발생:", error);
    }
}


// ✅ JWT 디코딩 함수
function decodeJWT(token) {
    try {
        const base64Url = token.split('.')[1]; // JWT의 payload 부분 추출
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // URL-safe Base64 디코딩
        const jsonPayload = decodeBase64(base64);
        return JSON.parse(jsonPayload);
    } catch (error) {
        console.error("❌ JWT 디코딩 오류:", error);
        return {};
    }
}

// ✅ Base64 디코딩 함수
function decodeBase64(base64) {
    try {
        return atob(base64); // 브라우저의 atob() 함수 사용
    } catch (error) {
        console.error("❌ Base64 디코딩 오류:", error);
        return "{}";
    }
}

// ✅ 로그아웃 처리
document.getElementById("logoutBtn").addEventListener("click", function () {
    fetch("/auth/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
        .then(response => {
            if (response.ok) {
                // ✅ localStorage 삭제 후 새로고침
                localStorage.removeItem("jwt_token");
                localStorage.removeItem("username");
                location.reload();
                alert("✅ 로그아웃 성공");
            } else {
                console.error("❌ 로그아웃 실패");
            }
        })
        .catch(error => {
            console.error("🔥 서버와의 통신 중 오류 발생:", error);
        });
});
