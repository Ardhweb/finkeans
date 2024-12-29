from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control text-center '}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class':'form-control text-center'}))
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')
        widgets ={
                'first_name':forms.TextInput(attrs={'class':'form-control text-center '}),
                'email':forms.TextInput(attrs={'class':'form-control text-center  '}),
                'username':forms.TextInput(attrs={'class':'form-control text-center '}) , 
            }
      
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    

    

