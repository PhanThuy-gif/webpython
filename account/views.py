from django.shortcuts import render,redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# def register(request):
    
#     if request.user.is_authenticated:
#         return redirect('profile',request.user.username)
    
#     if request.method == "POST" :
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         repeatpassword = request.POST['repeatpassword']
        
#         if password == repeatpassword:
#             # check email 
        
#             if User.objects.filter(email=email).exists():
#                 messages.info(request,'Email Already Used.')
#                 return redirect('register') # quay trở lại trang register 
            
#             # check email
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request,'Username Already Taken.')
#                 return redirect('register')
            
#             else:
#                 #create user
#                 user = User.objects.create_user(username=username,password=password)
#                 user.save()
#                 #login in the user
#                 user_login = auth.authenticate(username=username,password=password)
#                 auth.login(request,user_login)
                
#                 #create profile for new  user
#                 user_model = User.objects.get(username=username)
#                 new_profile = Profile.objects.create(user=user_model)
#                 new_profile.save()
#                 return redirect('profile',user_model.username)
#         else:
#             messages.info(request,'Password Not Matching')
#             return redirect('register')
    
#     context={}
#     return render(request,'register.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        first_name = request.POST.get('first_name')  # Nhận first name từ form
        last_name = request.POST.get('last_name')  # Nhận last name từ form
        
        # Kiểm tra mật khẩu
        if password == repeatpassword:
            # Kiểm tra email đã tồn tại chưa
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use.')
                return redirect('register')
            
            # Kiểm tra username đã tồn tại chưa
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken.')
                return redirect('register')
            
            else:
                # Tạo người dùng
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                user.save()

                # Đăng nhập người dùng vừa tạo
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Tạo profile cho người dùng mới
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()

                # Chuyển hướng đến trang profile của người dùng
                return redirect('profile', user_model.username)
        else:
            messages.info(request, 'Passwords do not match.')
            return redirect('register')
    
    return render(request, 'register.html')


@login_required(login_url='login')
# def profile(request,username):
    
#     user_object2 = User.objects.get(username=username)
#     user_profile2 = Profile.objects.get(user = user_object2)
    
#     user_object = User.objects.get(username=request.user)
#     user_profile = Profile.objects.get(user=user_object)
    
    
#     context = {"user_profile": user_profile, "user_profile2" : user_profile2}
#     return render(request,'profile.html',context)
def profile(request, username):
    # Lấy thông tin người dùng theo username từ URL và xử lý trường hợp không tồn tại
    user_object2 = get_object_or_404(User, username=username)
    user_profile2 = get_object_or_404(Profile, user=user_object2)

    # Lấy thông tin người dùng hiện tại từ request
    user_object = request.user
    user_profile = get_object_or_404(Profile, user=user_object)

    context = {
        "user_profile": user_profile,
        "user_profile2": user_profile2
    }
    
    return render(request, 'profile.html', context)

@login_required(login_url='login')
# def editProfile(request):
#     user_object = User.objects.get(username=request.user)
#     user_profile = Profile.objects.get(user=user_object)
    
#     if request.method == "POST":
#         #image
#         if request.FILES.get('profile_img')!= None :
#             user_profile.profile_img = request.FILES.get('profile_img')
#             user_profile.save()
        
#         #email
#         if request.POST.get('email') !=None:
#             u = User.objects.filter(email = request.POST.get('email')).first()
            
#             if u == None:
#                 user_object.email = request.POST.get('email')
#                 user_object.save()
#             else:
#                 if u != user_object:
#                     messages.info(request ,"Email Already Used")
#                     return redirect('edit_profile')
        
#         #username
#         if request.POST.get('username') !=None:
#             u = User.objects.filter(username = request.POST.get('username')).first()
            
#             if u == None:
#                 user_object.username = request.POST.get('username')
#                 user_object.save()
#             else:
#                 if u != user_object:
#                     messages.info(request ,"Username Already Taken")
#                     return redirect('edit_profile')
        
#         #firstname, lastname
#         user_object.first_name = request.POST.get('firstname')
#         user_object.last_name = request.POST.get('lastname')
#         user_object.save()
        
#         #gender,sdt
#         user_profile.gender = request.POST.get('gender')
#         user_profile.sdt = request.POST.get('sdt')
#         user_profile.save()
        
#         return redirect('profile' , user_object.username)
    
#     context = {'user_profile' : user_profile}
#     return render(request , 'profile-edit.html' , context)

def editProfile(request):
    # Lấy người dùng hiện tại và profile của họ
    user_object = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user_object)

    if request.method == "POST":
        # Cập nhật ảnh đại diện nếu có
        if request.FILES.get('profile_img'):
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()
        
        # Cập nhật email nếu có thay đổi
        email = request.POST.get('email')
        if email and email != user_object.email:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used")
                return redirect('edit_profile')
            user_object.email = email
            user_object.save()
        
        # Cập nhật username nếu có thay đổi
        username = request.POST.get('username')
        if username and username != user_object.username:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect('edit_profile')
            user_object.username = username
            user_object.save()
        
        # Cập nhật firstname và lastname
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        if firstname:
            user_object.first_name = firstname
        if lastname:
            user_object.last_name = lastname
        user_object.save()
        
        # Cập nhật gender và sdt (nếu có)
        gender = request.POST.get('gender')
        sdt = request.POST.get('sdt')
        if gender:
            user_profile.gender = gender
        if sdt:
            user_profile.sdt = sdt
        user_profile.save()

        # Thông báo thành công và chuyển hướng về trang profile
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile', user_object.username)
    
    context = {'user_profile': user_profile}
    return render(request, 'profile-edit.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('profile',request.user.username)
    
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect!')
            return redirect('login')
        
    return render(request,'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')