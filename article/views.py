from django.shortcuts import render
from django.contrib.auth.models import User
from account.models import Profile
from urllib.parse import unquote
from newspaper import Article
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from home.models import Article

# Create your views here.
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

        # Tách nội dung tóm tắt (nếu cần hiển thị nhiều đoạn văn)
        paragraphs = article.content.split('\n')
        
        category = article.category
        
        latest_articles = Article.objects.filter(category=category).order_by('-id')[:10]

        # Nếu không có bài báo trong danh mục, lấy các bài báo mới nhất, bao gồm những bài báo không có category
        if not latest_articles:
            latest_articles = Article.objects.filter(category__isnull=True).order_by('-id')[:10]
        # Thêm dữ liệu vào context
        
        context.update({
            'article': article,
            'image_url': article.image_url,
            'paragraphs': paragraphs,
            'latest_articles': latest_articles,
        })  

        # Trả về template hiển thị bài báo
        return render(request, 'article_detail.html', context)
    except Exception as e:
        return JsonResponse({'error': f'Lỗi: {str(e)}'})