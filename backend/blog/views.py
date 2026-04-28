from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment

# LOGIN (NO AUTH REQUIRED)
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )

    if user:
        token = RefreshToken.for_user(user)
        return Response({"token": str(token.access_token)})

    return Response({"error": "Invalid"}, status=401)


# GET POSTS (PUBLIC)
@api_view(['GET'])
def posts(request):
    data = Post.objects.all().order_by('-id')[:3]

    return Response([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "comments": [{"text": c.text} for c in p.comments.all()]
        }
        for p in data
    ])


#  CREATE POST (PROTECTED)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_post(request):
    print(request.user)  # DEBUG

    Post.objects.create(
        title=request.data['title'],
        content=request.data['content'],
        user=request.user
    )

    return Response({"msg": "Created Successfully! "})


# COMMENT (PROTECTED)
@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def comment(request, id):
    post = Post.objects.get(id=id)

    Comment.objects.create(
        post=post,
        text=request.data['text']
    )

    return Response({"msg": "Comment Added Successfully ! "})

# UPDATE POST
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, id):
    try:
        post = Post.objects.get(id=id, user=request.user)  
    except Post.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    post.title = request.data.get("title", post.title)
    post.content = request.data.get("content", post.content)
    post.save()

    return Response({"msg": "Updated Successfully! "})

# DELETE POST
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    try:
        post = Post.objects.get(id=id, user=request.user)
    except Post.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    post.delete()
    return Response({"msg": "deleted"})


