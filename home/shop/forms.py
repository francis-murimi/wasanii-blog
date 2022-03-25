from django import forms
from orders.models import Order, Bids
from .models import Art
from home.models import ArtistProfile

class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']
    def clean_bar(self):
        return self.cleaned_data['amount'] or None

"""class ArtAddForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['category','name','image_1','bid_price','description']"""

class ArtAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ArtAddForm, self).__init__(*args, **kwargs)
        artist = self.request.user.artistprofile
        self.fields['artist'].queryset = ArtistProfile.objects.filter(user = self.request.user)
    class Meta:
        model = Art
        fields = ['category','artist','name','image_1','bid_price','description']