from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile


#NOTE: UserCreation form e only username, password field thake, 
# oita overwrite kore email field add korte ei forms.py use kora hoise
# inherits UserCreationForm

class SignUpForm(UserCreationForm):
    # collect email from input
    email = forms.EmailField(label="Email Address", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # default django fields, see documentation




# NOTE: UserChangeFormat just mail r pass change kore,
# eta overwrite kore aro field add korbo

class UserProfileChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')



# modify UserProfile
class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic',]