from django.shortcuts import render, get_object_or_404, redirect
from comment.models import Post
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote

def article_detail(request, article_url):
    decoded_url = unquote(article_url)  # Giải mã URL
    post = get_object_or_404(Post, url=decoded_url)  # Điều chỉnh logic nếu cần
    comments = post.comments.all()  # Lấy danh sách bình luận của bài viết
    form = CommentForm()

    # Xử lý khi người dùng gửi bình luận
    if request.method == 'POST':
        form = CommentForm(request.POST)
        try:
          if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Thêm người dùng hiện tại vào bình luận
            comment.save()
        except Exception as e:
    # Ghi lỗi vào log hoặc hiển thị thông báo lỗi cho người dùng
                print(f"Error saving comment: {str(e)}")
    else:
        form=CommentForm()
    comments=post.comments.all()

    return render(request, 'article_detail.html',{'post': post,'form': form, 'comments': comments})

