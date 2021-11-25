from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'accounts'
urlpatterns = [
    # 회원가입
    path('signup/', views.signup),

    # 로그인
    path('api-token-auth/', obtain_jwt_token),

    # 유저정보
    path('info/<username>/', views.userinfo),

    # 유저 프로필 이미지 저장
    path('info/profile-image/<username>/', views.user_profile_image),

    # 아이디 중복 확인
    path('check-username/<username>/', views.check_username),

    # 비밀번호 확인
    path('check-password/<username>/', views.check_password),

    # 유저 정보 업데이트
    path('update/<username>/', views.update_user),

    # 유저 검색
    path('search/<username>/', views.search_user),

    # 추천 유저 정보
    path('recommend/search/', views.recommend_user),

    # 팔로우
    path('follow/<username>/', views.follow),
]
