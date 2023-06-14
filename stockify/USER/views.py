from django.shortcuts import render,redirect
from .forms import CreateUserForm,ProfileForm,LoginForm,User_UpdateForm,Update_ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

# Create your views here.
def home(request):
    return render(request,'User/home.html')
def register(request):
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your account has been created! You can Login now!')
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request,'User/register.html',context)

def login_page(request):
    if request.method =='POST':
        form = LoginForm(request,data =request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username = username,password =password)
            if user is not None:
                login(request,user)
                return redirect('profile')
            else:
                form.add_error(None,"Invalid username or Password")
            
    else:
        form = LoginForm()

    context = {'form':form}
    return render(request,'User/login.html',context)

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request,'User/profile.html')


@login_required
def profile_update(request):
    if request.method =='POST':
        u_form = User_UpdateForm(request.POST,instance=request.user)
        p_form = Update_ProfileForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    
    else:
        u_form =User_UpdateForm(instance=request.user)
        p_form = Update_ProfileForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request,'User/profile_update.html',context)
    
