from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    # SERVER_URL/profiles/<username>/  GET - 전체 리뷰목록 반환(프로필), POST - 리뷰생성
    path('reviews/<username>/', views.review_list_or_create),

    # SERVER_URL/profiles/<username>/<review_pk>   GET - 상세 리뷰 반환, PUT - 상세 리뷰 수정, DELETE - 상세 리뷰 삭제
    path('review_detail/<username>/<int:review_pk>/', views.review_detail_or_update_or_delete),

    # SERVER_URL/profiles/<username>/<review_pk>/likes/ POST - 리뷰 좋아요 토글
    path('review_detail/<username>/<int:review_pk>/likes/', views.review_likes),

    # SERVER_URL/profiles/<username>/<review_pk>/comments/   POST - 댓글생성
    path('comments/<username>/<int:review_pk>/', views.comment_create),

    # SERVER_URL/profiles/comment_detail/<comment_pk>/     PUT - 댓글수정  DELETE - 댓글삭제
    path('comment_detail/<int:comment_pk>/', views.comment_update_or_delete),

    # SERVER_URL/profiles/comment_detail/<comment_pk>/likes/     POST - 댓글 좋아요 토글
    path('comment_detail/<int:comment_pk>/likes/', views.comment_likes),

    # SERVER_URL/profiles/recommendation/likes/     GET - 좋아요 기반 추천 영화데이터 반환
    path('recommendation/likes/', views.recommendation_base_likes),

    # SERVER_URL/profiles/recommendation/follows/   GET - 팔로우 기반 추천 영화 데이터 반환
    path('recommendation/follows/', views.recommendation_base_follows),

    # SERVER_URL/profiles/recommendation/follows/   GET - 팔로잉한 사람들의 좋아요 한 영화 기반 추천 영화 데이터 반환
    path('recommendation/followings_likes/', views.recommendation_base_followings_likes),

    # 발생한 이슈 : url에 string type의 username이 들어오기 때문에 리뷰 상세페이지와 충돌발생
    # 예를들면 username이 comments인 사람이 있다면 그사람의 프로필페이지로 요청이 전송된다.(Top Down process 이기때문에)
    # 해결책 : variable routing을 int형으로만 사용하자. (나중에 회원가입은 숫자아이디로 가입 불가능하게)
]
