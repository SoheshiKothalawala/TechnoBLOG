from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment

@api_view(['POST'])
def login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        token = RefreshToken.for_user(user)
        return Response({"token": str(token.access_token)})
    return Response({"error":"Invalid"}, status=401)

@api_view(['GET'])
def posts(request):
    data = Post.objects.all().order_by('-id')[:3]
    result = []
    for p in data:
        result.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "comments": [{"text": c.text} for c in p.comments.all()]
        })
    return Response(result)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    Post.objects.create(
        title=request.data['title'],
        content=request.data['content'],
        user=request.user
    )
    return Response({"msg":"created"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, id):
    post = Post.objects.get(id=id)
    Comment.objects.create(post=post, text=request.data['text'])
    return Response({"msg":"comment added"})
