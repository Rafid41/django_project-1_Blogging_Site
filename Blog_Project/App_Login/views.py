from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from App_Login.forms import SignUpForm, UserProfileChange, ProfilePic

#default kisu form use kora holo
# authentication form doc  https://docs.djangoproject.com/en/4.2/topics/auth/default/
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout


# for logout helper
from django.contrib.auth.decorators import login_required



# Create your views here.


def sign_up(request):
    form = SignUpForm()
    registered = False

    # submit korle
    if request.method == 'POST':
        form = SignUpForm(data=request.POST) # save info on form variables

        if form.is_valid():
            form.save()  # db e save hbe
            registered = True

    dict= {'form': form, 'registered': registered}

    return render(request, 'App_Login/signup.html', context= dict)




def login_page(request):
    form = AuthenticationForm()

    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            # default form fields
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # authentication
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)

                # send to another page
                return HttpResponseRedirect(reverse('index'))
            
    return render(request, 'App_Login/login.html',context= {'form':form })



@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    return render(request, 'App_Login/profile.html', context= {})



@login_required
def user_change(request):
    current_user = request.user
    
    form = UserProfileChange(instance=current_user)  # j value change korbo, seta "instance=" e diye dte hbe

    if request.method == 'POST':
        # change current_user value with submitted value
        form = UserProfileChange(request.POST ,instance=current_user)

        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user) # ager value change hoise, new value load korte hbe context e send korar jnno

    return render(request, 'App_Login/change_profile.html', context = {'form': form})




@login_required
def pass_change(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)

    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data= request.POST)

        if form.is_valid():
            form.save()
            changed = True
    
    return render(request, 'App_Login/pass_change.html', context={'form': form, 'changed': changed})



@login_required
def add_pro_pic(request):
    form = ProfilePic()

    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)      # form e file thakle 'request.FILES' dte hbe

        if form.is_valid():
            user_obj = form.save(commit=False)     # commit false, cz new pic kon user er under e jabe ta bola hoynay
            
            # NOTE: user_obj e form er info ashse
            # etay 2 ta field ache //as per models.py
            # segula : 'user' and 'profile_pic'
            # 'profile_pic' set kora hoise
            # 'user' set korte hbe

            user_obj.user = request.user  # request.user holo j current user, mane j ei request ta send korse
            user_obj.save()

            return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/pro_pic_add.html', context={'form': form,})



@login_required
def change_pro_pic(request):

    # updating pic, so have to pass existing info
    #'user_profile' holo models.py er related name
    # eta models.py er 'UserProfile' er sathe 'User' class er relation k call korbe
    form = ProfilePic(instance= request.user.user_profile)

    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance= request.user.user_profile)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('App_Login:profile'))

    # same template as add_pro_pic()
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form,})
