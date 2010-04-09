from django import forms
from photologue.models import Photo

class ShoeboxPhotoForm(forms.Form):
    file = forms.CharField()
    title = forms.CharField()
    slug = forms.SlugField()
    
    class Media:
        js = {
            'all': ('/media/js/urlify.js',)
        }
    
    def __init__(self, *args, **kwargs):
        super(ShoeboxPhotoForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['readonly'] = True
        self.fields['title'].widget.attrs['class'] = 'title-field'
        self.fields['slug'].widget.attrs['class'] = 'slug-field'