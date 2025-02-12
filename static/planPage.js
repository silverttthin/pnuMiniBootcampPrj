
// ───────────────────────────────────────────────
// 1. "장소 추가" 버튼 클릭 시 해당 Day에 새로운 장소 입력 필드를 추가하는 함수
// ───────────────────────────────────────────────
function attachPlaceEvent(dayElement) {
    dayElement.querySelector('.add-place').addEventListener('click', () => {
        const placesContainer = dayElement.querySelector('.places-container');
        // 새로운 장소의 인덱스는 현재 존재하는 .place의 개수
        const placeIndex = placesContainer.children.length;
        // 새 장소 입력 영역 생성 (input name은 서버로 보내기 전에 JSON으로 직접 조합하므로 생략)
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place';
        placeDiv.innerHTML = `
                <input type="text" placeholder="장소명" required>
                <input type="datetime-local" required>
            `;
        placesContainer.appendChild(placeDiv);
    });
}
// 초기 Day의 "장소 추가" 버튼에 이벤트 연결
document.querySelectorAll('#days-container .day').forEach(attachPlaceEvent);

// ───────────────────────────────────────────────
// 2. "Day 추가" 버튼 클릭 시 새로운 Day 컨테이너를 추가하는 함수
// ───────────────────────────────────────────────
document.getElementById('add-day').addEventListener('click', () => {
    const daysContainer = document.getElementById('days-container');
    const newDayIndex = daysContainer.children.length;  // 현재 Day 개수를 새 Day의 인덱스로 사용
    const dayDiv = document.createElement('div');
    dayDiv.className = 'day';
    dayDiv.setAttribute('data-day-index', newDayIndex);
    dayDiv.innerHTML = `
            <h3>Day ${newDayIndex + 1}</h3>
            <div class="places-container">
                <div class="place">
                    <input type="text" placeholder="장소명" required>
                    <input type="datetime-local" required>
                </div>
            </div>
            <button type="button" class="add-place">장소 추가</button>
        `;
    daysContainer.appendChild(dayDiv);
    attachPlaceEvent(dayDiv);
});

// ───────────────────────────────────────────────
// 3. 계획 작성 폼 제출 시(계획 저장 버튼 클릭) 서버 API에 POST 요청하는 이벤트 핸들러
//    (fetch를 이용하여 비동기 요청을 보내고, 성공하면 DOM에 새로운 계획을 추가)
// ───────────────────────────────────────────────
document.getElementById('plan-form').addEventListener('submit', async function(e) {
    e.preventDefault(); // 기본 폼 제출(페이지 새로고침) 동작 차단

    // [1] 사용자가 입력한 기본 정보(작성자, 지역명, 시작일, 종료일, 여행 스타일)를 추출
    const form = e.target;
    const writerId = parseInt(form.querySelector('input[name="writer_id"]').value, 10);
    const localName = form.querySelector('input[name="local_name"]').value.trim();
    const startDate = form.querySelector('input[name="start_date"]').value.trim();
    const endDate = form.querySelector('input[name="end_date"]').value.trim();
    const tripStyle = form.querySelector('select[name="trip_style"]').value;

    // [2] 각 Day 영역에서 장소 정보를 추출하여 days 배열로 조합
    const days = [];
    // #days-container 내의 모든 .day 엘리먼트를 선택
    const dayElements = document.querySelectorAll('#days-container .day');
    dayElements.forEach((dayElement, dayIndex) => {
        // day_number는 1부터 시작 (dayIndex + 1)
        const dayNumber = dayIndex + 1;
        const places = [];
        // 각 Day 내의 모든 .place 엘리먼트를 선택
        const placeElements = dayElement.querySelectorAll('.place');
        placeElements.forEach(placeElement => {
            // 해당 장소의 이름과 방문 시간 추출
            const placeNameInput = placeElement.querySelector('input[type="text"]');
            const placeVisitInput = placeElement.querySelector('input[type="datetime-local"]');
            if (placeNameInput && placeVisitInput) {
                const placeName = placeNameInput.value.trim();
                const placeVisitTime = placeVisitInput.value.trim();
                // 두 값 모두 입력되어 있을 경우에만 배열에 추가
                if (placeName && placeVisitTime) {
                    places.push({
                        place_name: placeName,
                        place_visit_time: placeVisitTime
                    });
                }
            }
        });
        // 한 Day에 하나 이상의 장소가 있을 경우 days 배열에 추가
        if (places.length > 0) {
            days.push({
                day_number: dayNumber,
                places: places
            });
        }
    });

    // [3] API에 전달할 최종 JSON 객체 구성
    const planData = {
        writer_id: writerId,
        local_name: localName,
        start_date: startDate,
        end_date: endDate,
        trip_style: tripStyle,
        days: days
    };

    // [4] fetch 함수를 사용해 '/plans' 엔드포인트에 POST 요청 전송
    try {
        const response = await fetch('/plans', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // 요청 본문이 JSON임을 명시
            },
            body: JSON.stringify(planData)  // planData 객체를 JSON 문자열로 변환하여 전송
        });

        if (!response.ok) {
            // 응답이 성공적이지 않은 경우 에러 메시지 추출 후 사용자에게 알림
            const errorData = await response.json();
            alert("계획 생성 실패: " + errorData.detail);
            return;
        }

        const responseData = await response.json();
        // 응답에는 생성된 plan의 ID가 포함되어 있음 (responseData.plan_id)

        // [5] 새로고침 없이 작성한 계획 목록을 DOM에 업데이트하는 과정:
        //     (사용자가 입력한 planData를 바탕으로 새 plan 항목을 생성)
        const planList = document.getElementById('plan-list');
        const planItem = document.createElement('div');
        planItem.className = 'plan-item';

        // 각 Day와 그에 속하는 장소들을 HTML로 조합
        let daysHtml = "";
        planData.days.forEach(day => {
            let placesHtml = "";
            day.places.forEach(place => {
                placesHtml += `<li>${place.place_name} - ${place.place_visit_time}</li>`;
            });
            daysHtml += `
                    <div class="day">
                        <h4>Day ${day.day_number}</h4>
                        <ul>${placesHtml}</ul>
                    </div>
                `;
        });
        planItem.innerHTML = `
                <h3>${planData.local_name} (${planData.start_date} ~ ${planData.end_date})</h3>
                <p>스타일: ${planData.trip_style}</p>
                ${daysHtml}
            `;

        // "작성된 계획이 없습니다." 메시지가 있다면 제거
        const noPlansMessage = planList.querySelector('p');
        if (noPlansMessage && noPlansMessage.textContent.includes('작성된 계획이 없습니다.')) {
            noPlansMessage.remove();
        }
        // 새로 생성한 plan 항목을 계획 목록에 추가
        planList.appendChild(planItem);

        // [6] 계획 생성에 성공하면 폼을 초기화 (입력 필드 및 Day 영역 초기 상태 복원)
        form.reset();
        document.getElementById('days-container').innerHTML = '';
        const defaultDay = document.createElement('div');
        defaultDay.className = 'day';
        defaultDay.setAttribute('data-day-index', 0);
        defaultDay.innerHTML = `
                <h3>Day 1</h3>
                <div class="places-container">
                    <div class="place">
                        <input type="text" placeholder="장소명" required>
                        <input type="datetime-local" required>
                    </div>
                </div>
                <button type="button" class="add-place">장소 추가</button>
            `;
        document.getElementById('days-container').appendChild(defaultDay);
        attachPlaceEvent(defaultDay);

    } catch (error) {
        console.error("Error creating plan:", error);
        alert("계획 생성 중 오류가 발생했습니다.");
    }
});


// 계획 삭제 후 dom 처리
document.getElementById('plan-list').addEventListener('click', async function(e){
    // 삭제 버튼인 경우에만 처리
    if(e.target.classList.contains('delete-plan-btn')) {
        // 1. 삭제 API request에 필요한 값 구하기
        const planItem = e.target.closest('.plan-item');
        console.log(planItem)
        const planId = parseInt(planItem.dataset.planId);
        const writerId = parseInt(document.querySelector('input[name="writer_id"]').value, 10)

        // 2. 삭제 요청 보내기
        try {
            const response = await fetch('/plans',
                {
                    method: 'DELETE',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        plan_id: planId,
                        user_id: writerId
                    })
                }
            )

            if (!response.ok) {
                const errorData = await response.json();
                alert("삭제실패: " + errorData.detail);
                return;
            }

            // 3. 삭제 완료 시 DOM에서 제거
            planItem.remove();

        } catch(err){
            console.log("삭제 오류: "+ err);
            alert("계획 삭제 중 오류가 발생했습니다;")
        }





    }
})