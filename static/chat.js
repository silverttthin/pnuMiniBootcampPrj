//chatbot 관련  
// 역할: 사용자가 입력하면 FastAPI 서버(/v1/chat/message)로 요청
// 서버 응답을 받아 채팅창에 추가
// Enter 키 입력 시 전송 기능 추가

// 사용자가 Enter 키를 누르면 메시지 전송
document.addEventListener("DOMContentLoaded", () => {
    // 현재 페이지 경로 확인
    const currentPage = window.location.pathname;
    console.log("현재 페이지:", currentPage);

    
    // /chat 또는 /chat/ 로 시작하는지 확인
    if (!currentPage.startsWith("/chat")) {
        console.log("이 페이지는 /chat이 아니므로 채팅 기능을 로드하지 않음");
        return;
    }

    console.log("Chatbot script loaded!");

    // --- DOM 요소 가져오기 ---
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");

    // 안전장치: 혹시라도 요소가 없으면(오타 등) 바로 return
    if (!userInput || !sendButton || !chatBox) {
        console.error("채팅 관련 DOM 요소가 없습니다!");
        return;
    }
    

    // --- 채팅창에 메시지를 추가하는 함수 ---
    function addMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", sender);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);

        // 스크롤을 가장 아래로
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // --- 메시지를 서버로 보내는 함수 ---
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        // 사용자 메시지 추가
        addMessage("user", message);

        // 입력 필드 비우기
        userInput.value = "";

        // 서버로 전송 (x-www-form-urlencoded 예시)
        const formData = new URLSearchParams();
        formData.append("user_input", message);

        fetch("/v1/chat/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData.toString(), // e.g. "user_input=Hello"
        })
            .then((response) => response.json())
            .then((data) => {
                // 봇 응답 추가
                if (data?.response) {
                    addMessage("bot", data.response);
                } else {
                    addMessage("bot", "오류가 발생했습니다.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("bot", "오류가 발생했습니다. 다시 시도해 주세요.");
            });
    }

    // --- 엔터 키로 메시지 전송 ---
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // --- 전송 버튼 클릭으로 메시지 전송 ---
    sendButton.addEventListener("click", sendMessage);
});
