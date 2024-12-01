from django.shortcuts import render 
from django.contrib.auth.models import User
from account.models import Profile
import feedparser
from newspaper import Article
import re
from bs4 import BeautifulSoup
from django.utils.dateparse import parse_datetime
from .models import Article
from newspaper import Article as NewspaperArticle
from article.views import article_detail
from django.db.models import Q


def fetch_and_save_new_articles():
    """
    Lấy bài báo mới từ RSS feed và lưu vào cơ sở dữ liệu nếu chưa tồn tại.
    """
    rss_url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:5]:  # Lấy tối đa 50 bài báo
        # Kiểm tra bài báo đã tồn tại hay chưa
        if not Article.objects.filter(link=entry.link).exists():
            # Lấy URL ảnh
            image_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else None

            # Nếu không có enclosure, tìm ảnh trong phần description
            if not image_url and 'description' in entry:
                img_match = re.search(r'<img src="([^"]+)"', entry.description)
                if img_match:
                    image_url = img_match.group(1)

            # Nếu không tìm thấy ảnh, dùng ảnh mặc định
            if not image_url:
                image_url = "/static/images/news.webp"

            # Xử lý phần tóm tắt
            summary_text = ""
            if 'description' in entry:
                soup = BeautifulSoup(entry.description, 'html.parser')
                for tag in soup.find_all(['a', 'img']):  # Loại bỏ thẻ <a> và <img>
                    tag.decompose()
                summary_text = soup.get_text()

            # Lấy nội dung đầy đủ của bài báo từ liên kết
            try:
                full_article = NewspaperArticle(entry.link)  # Tạo đối tượng Article từ URL
                full_article.download()  # Tải bài báo
                full_article.parse()  # Phân tích bài báo
                full_content = full_article.text  # Lấy nội dung đầy đủ
            except Exception:
                full_content = ""  # Nếu không thể tải nội dung bài báo, để trống

            # Lưu bài báo vào cơ sở dữ liệu
            Article.objects.create(
                title=entry.title,
                link=entry.link,
                published=parse_datetime(entry.published),
                summary=summary_text,
                content=full_content,  # Lưu nội dung đầy đủ
                image_url=image_url,
            )
def get_articles_from_database(limit=51):
    return Article.objects.all().order_by('-id')[:limit]

def index(request):
    """
    Hàm xử lý request của trang chủ.
    """
    # Kiểm tra nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}

    # Lấy và lưu các bài báo mới
    fetch_and_save_new_articles()

    # Lấy danh sách bài báo từ cơ sở dữ liệu
    articles = get_articles_from_database()
    context['articles'] = articles

    # Trả về template với dữ liệu bài báo
    return render(request, 'home.html', context)



def fetch_new_articles(category):
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
        return None  # Trả về None nếu không tìm thấy chuyên mục

    # Tải và phân tích RSS feed
    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:5]:  # Lấy 50 bài báo mới nhất
        # Kiểm tra xem bài báo đã tồn tại trong cơ sở dữ liệu chưa
        if Article.objects.filter(link=entry.link).exists():
            continue  # Nếu bài báo đã tồn tại thì bỏ qua

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
            for tag in soup.find_all(['a', 'img']):  # Loại bỏ thẻ <a> và <img>
                tag.decompose()
            summary_text = soup.get_text()

        # Lấy nội dung đầy đủ của bài báo
        try:
            full_article = NewspaperArticle(entry.link)  # Tạo đối tượng Article từ URL
            full_article.download()  # Tải bài báo
            full_article.parse()  # Phân tích bài báo
            full_content = full_article.text  # Lấy nội dung đầy đủ
        except Exception as e:
            full_content = ""  # Nếu có lỗi, không có nội dung đầy đủ

        # Lưu bài báo vào cơ sở dữ liệu
        Article.objects.create(
            title=entry.title,
            link=entry.link,
            published=parse_datetime(entry.published),
            summary=summary_text,
            content=full_content,  # Lưu nội dung đầy đủ
            image_url=image_url,
            category=category
        )

def get_articles_from_db(category):
    # Lấy các bài báo từ cơ sở dữ liệu và sắp xếp theo thời gian
    return Article.objects.filter(category=category).order_by('-id')[:51]

def category_view(request, category):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}

    # Lấy bài báo mới từ RSS feed và cập nhật database
    fetch_new_articles(category)

    # Lấy các bài báo từ cơ sở dữ liệu
    articles = get_articles_from_db(category)

    # Nếu không tìm thấy bài báo nào, trả về trang 404
    if not articles:
        return render(request, '404.html', status=404)

    context['articles'] = articles

    # Trả về template với dữ liệu người dùng và bài báo
    return render(request, 'home.html', context)



def search(request):
    # Kiểm tra nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}

    # Xử lý tìm kiếm
    if request.method == "POST":
        searched = request.POST.get("searched", "").strip()
        
        if searched:
            # Sử dụng Django ORM để tìm kiếm trong cơ sở dữ liệu
            filtered_articles = Article.objects.filter(
                Q(title__icontains=searched) |  # Tìm trong tiêu đề
                Q(summary__icontains=searched) |  # Tìm trong tóm tắt
                Q(content__icontains=searched)  # Tìm trong nội dung bài viết
            ).order_by('-published')  # Sắp xếp theo ngày xuất bản mới nhất
            
            context.update({
                'searched': searched,
                'articles': filtered_articles,
            })
        else:
            # Trường hợp không nhập từ khóa
            context['searched'] = searched
            context['articles'] = []
    else:
        context['articles'] = []

    return render(request, 'home.html', context)

