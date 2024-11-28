from django.shortcuts import render ,HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
import urllib
from urllib.parse import unquote
from urllib.parse import urljoin
import feedparser
from newspaper import Article
from django.http import JsonResponse
from urllib.parse import quote, urljoin
import re
from bs4 import BeautifulSoup
    
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
        
        # Tạo đối tượng Article với URL đã giải mã
        article = Article(decoded_url)
        article.download()
        article.parse()
        
        paragraphs = article.text.split('\n')

        # Kiểm tra nếu ảnh có trong bài báo
        image_url = article.top_image if article.top_image else None

        # Thêm dữ liệu vào context
        context.update({
            'article': article,
            'image_url': image_url,
            'paragraphs': paragraphs
        })

        # Trả về nội dung bài báo cho template
        return render(request, 'article_detail.html', context)
    except Exception as e:
        return JsonResponse({'error': f'Lỗi: {str(e)}'})



def index(request):
    # Kiểm tra nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}

    # URL của RSS Feed từ VnExpress
    rss_url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:51]:  # Lấy 51 bài báo mới nhất
        # Mã hóa URL của bài báo
        encoded_url = quote(entry.link)

        image_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None
    
    # Nếu không có enclosure, tìm ảnh trong phần description
        if not image_url and 'description' in entry:
            img_match = re.search(r'<img src="([^"]+)"', entry.description)
            if img_match:
                image_url = img_match.group(1)
                
        if not image_url:
            image_url = "/static/images/news.webp" 
            
        
        if 'description' in entry:
            soup = BeautifulSoup(entry.description, 'html.parser')
            # Xóa các thẻ <a> và <img>
            for tag in soup.find_all(['a', 'img']):
                tag.decompose()  # Xóa thẻ khỏi DOM

            # Lấy lại tóm tắt đã xử lý
            summary_text = soup.get_text()


        # Thêm bài báo vào danh sách articles
        articles.append({
            'title': entry.title,
            'link': encoded_url,  # Sử dụng URL đã mã hóa
            'published': entry.published,
            'summary': summary_text,
            'image_url': image_url  # Truyền URL ảnh vào template
        })

    # Cập nhật context để chứa cả thông tin người dùng và bài báo
    context['articles'] = articles

    # Trả về template với dữ liệu người dùng và bài báo
    return render(request, 'home.html', context)

def category_view(request, category):
    
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}
    
    # Định nghĩa các RSS feed cho từng hạng mục
    rss_urls = {
        "Thời Sự": "https://vnexpress.net/rss/thoi-su.rss",
        "Thế Giới": "https://vnexpress.net/rss/the-gioi.rss",
        "Thư Giãn": "https://vnexpress.net/rss/cuoi.rss",
        "Kinh Doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
        "Bất Động Sản": "https://vnexpress.net/rss/bat-dong-san.rss",
        "Khoa Học": "https://vnexpress.net/rss/khoa-hoc.rss",
        "Giải Trí": "https://vnexpress.net/rss/giai-tri.rss",
        "Thể Thao": "https://vnexpress.net/rss/the-thao.rss",
        "Pháp Luật": "https://vnexpress.net/rss/phap-luat.rss",
        "Giáo Dục": "https://vnexpress.net/rss/giao-duc.rss",
        "Sức Khỏe": "https://vnexpress.net/rss/suc-khoe.rss",
        "Đời Sống": "https://vnexpress.net/rss/doi-song.rss",
        "Du Lịch": "https://vnexpress.net/rss/du-lich.rss",
        "Số Hóa": "https://vnexpress.net/rss/so-hoa.rss",
        "Xe": "https://vnexpress.net/rss/oto-xe-may.rss"
    }

    # Lấy URL của category từ danh sách RSS
    rss_url = rss_urls.get(category)
    if not rss_url:
        # Trả về trang 404 nếu không tìm thấy chuyên mục
        return render(request, '404.html', status=404)

    # Tải và phân tích RSS feed
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:51]:  # Lấy 51 bài báo mới nhất
        # Mã hóa URL của bài báo
        encoded_url = quote(entry.link)

        # Kiểm tra và lấy ảnh từ enclosure (nếu có)
        image_url = None
        if 'enclosures' in entry and entry.enclosures:
            image_url = entry.enclosures[0].href
        
        # Nếu không có enclosure, tìm ảnh trong phần description
        if not image_url and 'description' in entry:
            img_match = re.search(r'<img src="([^"]+)"', entry.description)
            if img_match:
                image_url = img_match.group(1)
        
        # Nếu không có ảnh, sử dụng ảnh mặc định
        if not image_url:
            image_url = "/static/images/news.webp" 

        # Xử lý tóm tắt bài báo bằng BeautifulSoup
        summary_text = ''
        if 'description' in entry:
            soup = BeautifulSoup(entry.description, 'html.parser')
            # Xóa các thẻ <a> và <img>
            for tag in soup.find_all(['a', 'img']):
                tag.decompose()  # Xóa thẻ khỏi DOM

            # Lấy lại tóm tắt đã xử lý
            summary_text = soup.get_text()

        # Thêm bài báo vào danh sách articles
        articles.append({
            'title': entry.title,
            'link': encoded_url,  # Sử dụng URL đã mã hóa
            'published': entry.published,
            'summary': summary_text,
            'image_url': image_url  # Truyền URL ảnh vào template
        })

    # Cập nhật context để chứa cả thông tin người dùng và bài báo
    context.update({'articles': articles, 'category': category})

    # Trả về template với dữ liệu người dùng và bài báo
    return render(request, 'home.html', context)
