from django import forms
from django.contrib.auth.models import User


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #
    #     if commit:
    #         user.save()
    #
    #     return user
