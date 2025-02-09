// script.js
function generatePlan() {
    const destination = document.getElementById("destination").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

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
