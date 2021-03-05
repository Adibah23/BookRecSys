from django import forms
from BookRecSys_App.models import User, Rating, Dislike


class RegisterUser(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class FavouriteBook(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

class DislikeBook(forms.ModelForm):
    class Meta:
        model = Dislike
        fields = '__all__'