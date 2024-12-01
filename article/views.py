from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from account.models import Profile
from urllib.parse import unquote
from newspaper import Article
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from home.models import Article

# Create your views here.
# def article_detail(request, article_url):
#     if request.user.is_authenticated:
#         user_object = User.objects.get(username=request.user)
#         user_profile = Profile.objects.get(user=user_object)
#         context = {"user_profile": user_profile}
#     else:
#         context = {}

#     try:
#         # Giải mã URL
#         decoded_url = unquote(article_url)
        
#         # Lấy bài báo từ cơ sở dữ liệu dựa trên URL đã giải mã
#         article = get_object_or_404(Article, link=decoded_url)

#         # Tách nội dung tóm tắt (nếu cần hiển thị nhiều đoạn văn)
#         paragraphs = article.content.split('\n')
        
#         category = article.category
        
#         latest_articles = Article.objects.filter(category=category).order_by('-id')[:10]

#         # Nếu không có bài báo trong danh mục, lấy các bài báo mới nhất, bao gồm những bài báo không có category
#         if not latest_articles:
#             latest_articles = Article.objects.filter(category__isnull=True).order_by('-id')[:10]
#         # Thêm dữ liệu vào context
        
#         context.update({
#             'article': article,
#             'image_url': article.image_url,
#             'paragraphs': paragraphs,
#             'latest_articles': latest_articles,
#         })  

#         # Trả về template hiển thị bài báo
#         return render(request, 'article_detail.html', context)
#     except Exception as e:
#         return JsonResponse({'error': f'Lỗi: {str(e)}'})

from home.models import Comment
from article.form import CommentForm

def article_detail(request, article_url):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}

    try:
        # Giải mã URL
        decoded_url = unquote(article_url)

        # Lấy bài báo từ cơ sở dữ liệu dựa trên URL đã giải mã
        article = get_object_or_404(Article, link=decoded_url)

        # Tách nội dung tóm tắt
        paragraphs = article.content.split('\n')
        
        category = article.category
        
        latest_articles = Article.objects.filter(category=category).order_by('-id')[:10]

        if not latest_articles:
            latest_articles = Article.objects.filter(category__isnull=True).order_by('-id')[:10]

        # Xử lý form bình luận
        comment_form = CommentForm()
        if request.method == "POST" and 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
                return redirect('article_detail', article_url=article_url)

        # Lấy danh sách bình luận của bài báo
        comments = article.comments.all().order_by('-created_at')

        # Thêm dữ liệu vào context
        context.update({
            'article': article,
            'image_url': article.image_url,
            'paragraphs': paragraphs,
            'latest_articles': latest_articles,
            'comments': comments,
            'comment_form': comment_form,
        })

        return render(request, 'article_detail.html', context)
    except Exception as e:
        return JsonResponse({'error': f'Lỗi: {str(e)}'})
