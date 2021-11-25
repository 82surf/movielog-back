from django.db import models
from datetime import date
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    # 요청시 입력해야할 field
    ## 사용자 입력 field
    # 내가주는 평점
    rank = models.IntegerField(default=5)
    # 한줄평
    oneline_review = models.CharField(max_length=100, blank=True)
    # 명대사
    quote = models.CharField(max_length=100, blank=True)
    # 리뷰내용
    content = models.TextField(blank=True)
    # 관람일자
    watched_at = models.DateField(default=date.today())

    movie_title = models.CharField(max_length=200, blank=True)
    # 썸네일 URI >> 영화사진?(charfield) 커스텀사진(imagefield)?
    thumbnail_path = models.CharField(max_length=200, blank=True)

    ## tmdb api response field
    # tmdb movie_id
    tmdb_movie_id = models.IntegerField(blank=True)
    
    
    # 자동생성 field
    # review author
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 리뷰 create time
    created_at = models.DateTimeField(auto_now_add=True)
    # 리뷰 update time
    updated_at = models.DateTimeField(auto_now=True)
    # # 좋아요 누른 user
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    # 팔로워 공개여부
    is_private = models.BooleanField(default=False)


class Comment(models.Model):
    # comment author
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Review
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # comment content
    content = models.TextField()
    # 좋아요 누른 user
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    # 댓글 created time
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글 updated time
    updated_at = models.DateTimeField(auto_now=True)

    # ###################################################################
    # 추가예정기능 : 대댓글
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    # if comment.parent_comment: 일때 대댓글 보여주는방식.

