from enum import Enum


# TripStyle Enum 정의
class TripStyle(str, Enum):
    ACTIVITY = "체험/액티비티"
    SNS_HOT_PLACE = "SNS 핫플레이스"
    NATURE = "자연과 함께"
    FAMOUS_SPOTS = "유명 관광지는 필수"
    HEALING = "여유롭게 힐링"
    CULTURE_ART_HISTORY = "문화/예술/역사"
    FEEL_LIKE_TRIP_SPOT = "여행지 느낌. 물씬"
    SHOPPING = "쇼핑은 열정적으로"
    FOOD = "관광보다 먹방"
