from django import forms
from photologue.models import Photo

class ShoeboxPhotoForm(forms.Form):
    file = forms.CharField()
    title = forms.CharField()
    slug = forms.SlugField()
    
    def __init__(self, *args, **kwargs):
        super(ShoeboxPhotoForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['readonly'] = True