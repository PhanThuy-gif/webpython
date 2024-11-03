from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile
# Create your views here.

def register(request):
    
    if request.user.is_authenticated:
        return redirect('profile',request.user.username)
    
    if request.method == "POST" :
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        
        if password == repeatpassword:
            # check email 
        
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Used.')
                return redirect('register') # quay trở lại trang register 
            
            # check email
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken.')
                return redirect('register')
            
            else:
                #create user
                user = User.objects.create_user(username=username,password=password)
                user.save()
                #login in the user
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                #create profile for new  user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('profile',user_model.username)
        else:
            messages.info(request,'Password Not Matching')
            return redirect('register')
    
    context={}
    return render(request,'register.html',context)

@login_required(login_url='login')
def profile(request,username):
    
    user_object2 = User.objects.get(username=username)
    user_profile2 = Profile.objects.get(user = user_object2)
    
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    
    context = {"user_profile": user_profile, "user_profile2" : user_profile2}
    return render(request,'profile.html',context)


@login_required(login_url='login')
def editProfile(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method == "POST":
        #image
        if request.FILES.get('profile_img')!= None :
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()
        
        #email
        if request.POST.get('email') !=None:
            u = User.objects.filter(email = request.POST.get('email')).first()
            
            if u == None:
                user_object.email = request.POST.get('email')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request ,"Email Already Used")
                    return redirect('edit_profile')
        
        #username
        if request.POST.get('username') !=None:
            u = User.objects.filter(username = request.POST.get('username')).first()
            
            if u == None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request ,"Username Already Taken")
                    return redirect('edit_profile')
        
        #firstname, lastname
        user_object.first_name = request.POST.get('firstname')
        user_object.last_name = request.POST.get('lastname')
        user_object.save()
        
        #gender
        user_profile.gender = request.POST.get('gender')
        user_object.email = request.POST.get('email')
        user_profile.sdt = request.POST.get('sdt')
        user_profile.save()
        
        return redirect('profile' , user_object.username)
    
    context = {'user_profile' : user_profile}
    return render(request , 'profile-edit.html' , context)

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