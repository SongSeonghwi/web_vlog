from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            image = request.FILES['image']
            post = Post(
                author=request.user if request.user.is_authenticated else None,  # 确保处理未认证用户
                title=request.data.get('title', 'Uploaded Image'),
                text=request.data.get('text', 'This is an uploaded image.'),
                image=image
            )
            post.save()
            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
