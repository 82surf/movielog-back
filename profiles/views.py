from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Review, Comment
from .serializers import ReviewListSerializer, ReviewSerializer, CommentSerializer, ReviewRecommendSerializer, ReviewQuoteSerializer


@api_view(['GET', 'POST'])
def review_list_or_create(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == 'GET':
        reviews = Review.objects.filter(user=user.pk)
        serializer = ReviewListSerializer(reviews, many=True)
        
        return Response(serializer.data)

    else:
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_or_update_or_delete(request, username, review_pk):
    user = get_object_or_404(get_user_model(), username=username)
    review = get_object_or_404(Review, pk=review_pk, user=user)

    if request.method == 'GET':
        # serializer = ReviewSerializer(review)
        # return Response(serializer.data)
        if review.like_users.filter(pk=request.user.pk).exists():
            is_like = True
        else:
            is_like = False
        context = {
            'is_like' : is_like,
        }
        return JsonResponse(context, safe=True)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        data = {
            'delete': f'{user.username} 유저의 {review_pk}번 리뷰가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def comment_create(request, username, review_pk):
    # 댓글을 남길 리뷰의 작성자
    user = get_object_or_404(get_user_model(), username=username)
    # 댓글을 남길 리뷰
    review = get_object_or_404(Review, pk=review_pk, user=user.pk)
    # 직렬화
    serializer = CommentSerializer(data=request.data)
    # 유효성 검사
    if serializer.is_valid(raise_exception=True):
        serializer.save(review=review, user_id=request.user.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, comment_pk):
    # 수정, 삭제 할 댓글
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 수정
    if request.method == 'PUT':
        # 수정된 댓글 정보 직렬화
        serializer = CommentSerializer(instance=comment, data=request.data)
        # 유효성 검사 후 저장 & 반환
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 삭제
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': f'{comment_pk}번 댓글이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_likes(request, username, review_pk):
    user = get_object_or_404(get_user_model(), username=username)
    review = get_object_or_404(Review, pk=review_pk, user=user.pk)

    if request.method == 'GET':
        if review.like_users.filter(pk=request.user.pk).exists():
            is_like: True
        else:
            is_like: False
        return Response({'is_like':is_like})

    else:
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
            data = {
                'is_like': False,
                'unlike': f'{username}님의 {review_pk}번 게시글의 좋아요를 해제했습니다.'
            }
        else:
            review.like_users.add(request.user)
            data = {
                'is_like': True,
                'like': f'{username}님의 {review_pk}번 게시글에 좋아요를 눌렀습니다.'
            }
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def comment_likes(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        data = {
            'unlike': f'{comment_pk}번 댓글의 좋아요를 해제했습니다.'
        }
    else:
        comment.like_users.add(request.user)
        data = {
            'like': f'{comment_pk}번 댓글에 좋아요를 눌렀습니다.'
        }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recommendation_base_likes(request):
    # 내가 작성한 리뷰 목록 가져오기
    mymovies = request.user.review_set.values('tmdb_movie_id')
    # 영화 id 저장해놓을 list
    movies = request.user.like_reviews.exclude(tmdb_movie_id__in=mymovies)    # 안 본 영화
    serializer = ReviewRecommendSerializer(movies, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def recommendation_base_follows(request):
    mymovies = request.user.review_set.values('tmdb_movie_id')
    users = request.user.followings.all()
    if users:
        movielist = users[0].review_set.exclude(tmdb_movie_id__in=mymovies)

        for user in users:
            data = user.review_set.exclude(tmdb_movie_id__in=mymovies)
            movielist |= data
        serializer = ReviewRecommendSerializer(movielist,  many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'result':False},status=status.HTTP_200_OK)

@api_view(['GET'])
def recommendation_base_followings_likes(request):
    mymovies = request.user.review_set.values('tmdb_movie_id')
    users = request.user.followings.all()
    if users:
        movielist = users[0].like_reviews.exclude(tmdb_movie_id__in=mymovies)
        for user in users:
            data = user.like_reviews.exclude(tmdb_movie_id__in=mymovies)
            movielist |= data
        serializer = ReviewRecommendSerializer(movielist.distinct(), many=True) # 중복 리뷰 제거
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'result':False},status=status.HTTP_200_OK)

@api_view(['GET'])
def recommended_movie_by_likes_reviewinfo(request, tmdb_movie_id):
    movies = Review.objects.filter(tmdb_movie_id=tmdb_movie_id)
    serializer = ReviewRecommendSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
