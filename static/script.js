
// script.js
function generatePlan() {
    const destination = document.getElementById("destination").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    console.log("test")

    if (!destination || !startDate || !endDate) {
        alert("모든 필드를 입력해 주세요.");
        return;
    }

    const outputSection = document.getElementById("output");
    const planDetails = document.getElementById("plan-details");

    planDetails.innerHTML = `여행지: <strong>${destination}</strong><br>
                             출발일: <strong>${startDate}</strong><br>
                             귀국일: <strong>${endDate}</strong>`;

    outputSection.classList.remove("hidden");
}



// 회원가입 요청
document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault(); // 기본 폼 제출 동작 막기
    console.log("화면누름")
    // 각 input 태그의 값을 가져옵니다.
    const login_id = document.getElementById("login_id").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    // 전송할 데이터를 객체로 구성합니다.
    const payload = {
        login_id: login_id,
        password: password,
        name: name
    };

    // auth/signup 엔드포인트로 POST 요청을 보냅니다.
    fetch("/auth/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // 요청 성공 후 응답 데이터 처리
        document.getElementById("message").innerText = data.message || "가입이 완료되었습니다.";
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("message").innerText = "가입 중 오류가 발생했습니다.";
    });
});
