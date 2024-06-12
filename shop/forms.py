from django import forms

from .models import Reviews,CustomUser

class ReviewForm(forms.ModelForm):
    class Meta:
        fields=['rating','review']
        model=Reviews

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['min'] = 0
        self.fields['rating'].widget.attrs['max'] = 5

class EditProfileForm(forms.ModelForm):
    class Meta:
        fields=['first_name','last_name','email','phone','gender','profile']
        model=CustomUser

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['profile'].required = True

