from django import forms
from recommender.models import User, UserProfile, RoommatePreference
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('gender', 'picture')

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = RoommatePreference
        fields = ('gender_prefer', 'smoke', 'party', 'sleep_late', 'pet', 'description')
        labels = {
            'gender_prefer': _('Preferred Gender'),
            'smoke': _('Accept Smoke'),
            'party': _('Accept Party'),
            'sleep_late': _('Accept Stay up late'),
            'pet': _('Accept Pet'),
            'description': _('Others'),
        }