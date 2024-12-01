from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ReadingList
from home.models import Article
from .models import ReadingList
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import Profile
from django.shortcuts import get_object_or_404

@login_required
def add_to_reading_list(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        reading_item, created = ReadingList.objects.get_or_create(user=request.user, article=article)
    except Article.DoesNotExist:
        messages.error(request, 'Không tìm thấy bài báo.')
    return redirect('reading_list')


@login_required
def remove_from_reading_list(request, article_id):
    # Kiểm tra xem bài báo có tồn tại hay không
    article = get_object_or_404(Article, id=article_id)

    # Xóa bài báo khỏi danh sách đọc sau của người dùng
    ReadingList.objects.filter(user=request.user, article=article).delete()

    # Chuyển hướng về trang chủ
    return redirect('reading_list')  # Thay 'home' bằng tên URL của trang chủ của bạn



@login_required
def reading_list_view(request):
    # Lấy thông tin user profile nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        try:
            user_object = User.objects.get(username=request.user)
            user_profile = Profile.objects.get(user=user_object)
        except (User.DoesNotExist, Profile.DoesNotExist):
            user_profile = None  # Xử lý nếu không tìm thấy user hoặc profile

    # Lấy danh sách đọc sau của người dùng
    reading_list = ReadingList.objects.filter(user=request.user).select_related('article')

    # Kết hợp dữ liệu vào context
    context = {
        'user_profile': user_profile,
        'reading_list': reading_list,
    }
    
    return render(request, 'reading_list.html', context)

