# pnuMiniBootcampPrj
여행 플랜 서비스 트리플 벤치마킹 서비스

### 개발 전
1. venv를 만들어주세요. 이때 파이썬 버전은 3.13.0으로 지정해주세요. 만들고 활성화시켜주세요.
2. requirements.txt에 있는 모듈들로 설치해주세요. ```pip install -r requirements.txt```
3. 만약 모듈을 install하게 된다면 반드시 커밋 전에 ```pip freeze > requirememts.txt```로 의존성 문서를 최신화하고 같이 커밋해주세요.
4. **반드시 브랜치를 만들기 전** 다음 두가지를 확인합시다. 현재 dev인가? 그렇다면 ```git pull --ff-only origin dev```로 dev를 최신화한 상태인가?
5. 자신이 맡을 기능개발에 맞게 dev에서 브랜치를 분기시킵시다. 이 때 브랜치명은 feature/기능명 으로 가급적 해주세요. _Ex:feature/getPostApi_

### 개발 후
1. 커밋 후 push는 반드시 다음처럼 해주세요. ```git push origin feature/기능명``` 자신이 만든 브랜치명 그대로 적는게 포인트입니다
2. push할 때 -f 옵션은 반드시 세번 네번 생각합시다. 협업 간 재앙의 원인 1티어입니다.
