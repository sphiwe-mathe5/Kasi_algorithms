from django import forms
from .models import Post
from submit.models import Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'url' ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
    

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True


    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024: 
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return image
