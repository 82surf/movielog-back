from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import  status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, UserListSerializer, ProfileImageSerializer, UserFollowSerializer
from .forms import UserUpdateForm

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def userinfo(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if user.followers.filter(pk=request.user.pk).exists():
        isfollowing = True
    else:
        isfollowing = False
    followers = UserFollowSerializer(user.followers,many=True).data
    followings = UserFollowSerializer(user.followings,many=True).data
    my_follower = UserFollowSerializer(request.user.followers,many=True).data
    context = {
        'id' : user.pk,
        'username' : user.username,
        'follower_count' : user.followers.count(),
        'following_count' : user.followings.count(),
        'name': user.name,
        'isFollowing' : isfollowing,
        'is_private': user.is_private,
        'followers': followers,
        'followings': followings,
        'my_follower': my_follower,
    }
    return JsonResponse(context, safe=True)


@api_view(['GET'])
def user_profile_image(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = ProfileImageSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(response, username):
    User = get_user_model()
    data = {'isUnique': not User.objects.filter(username=username).exists()}
    return JsonResponse(data)


@api_view(['POST'])
def check_password(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    data = {
        'isValid': user.check_password(request.data.get('password')),
        'errMsgFlag': True,
        'email': user.email,
        'name': user.name,
        'isPrivate': user.is_private
    }
    return JsonResponse(data, safe=True)


@api_view(['POST'])
def update_user(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.FILES:
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
    else:
        form = UserUpdateForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        data = {
            'update': f'{username}님의 회원정보가 수정되었습니다.'
        }
        return Response(data)
    data = {
        'error': f'{username}님의 회원정보 수정에 실패했습니다.'
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_user(request, username):
    User = get_user_model()
    search_result = User.objects.filter(username__startswith=username)
    if search_result:
        serializer = UserListSerializer(search_result, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    data = {
        'search_result': '일치하는 유저가 없습니다.'
    }
    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
def follow(request, username):
    me = request.user
    you = get_object_or_404(get_user_model(), username=username)

    if me != you:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
            data = {
                'isFollowing': False,
                'unfollow': f'{me.username}님이 {you.username}님을 언팔로우 했습니다.'
            }
        else:
            you.followers.add(me)
            data = {
                'isFollowing': True,
                'follow': f'{me.username}님이 {you.username}님을 팔로우 했습니다.'
            }
        return Response(data, status=status.HTTP_200_OK)
    data = {
        'error': '자기 자신을 팔로우 할 수 없습니다.'
    }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def recommend_user(request):
    followings=request.user.followers.values('pk')
    users = get_user_model().objects.exclude(pk__in=followings)
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)