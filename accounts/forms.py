from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(max_length=254, help_text='eg. youremail@anyemail.com')
#     address = forms.CharField(max_length=250, required=True)
#     state = forms.CharField(max_length=25, required=True)
#     city = forms.CharField(max_length=25, required=True)
#     phone = forms.IntegerField(required=True)
    
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = (
# 			'username',
# 			'first_name',
# 			'last_name',
# 			'email',
# 			'address', 
# 			'city',
# 			'state',
# 			'phone',
# 			)
#     def save(self, commit=True):
#         user = super(CustomUserCreationForm, self).save(commit=False)
#         user.address = self.cleaned_data['address']
#         user.state = self.cleaned_data['state']
#         user.city = self.cleaned_data['city']
#         user.phoneNo = self.cleaned_data['phone']
#         if commit:
#             user.save()
#         return user


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email     = forms.EmailField(required=True, max_length=200, help_text='eg. sumtin@gmail.com')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'password', 'password1')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'phone_number', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]