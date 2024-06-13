from django import forms
from .models import Video
from django.core.exceptions import ValidationError

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                raise ValidationError('Unsupported file format.')
            if file.size > 104857600:  # 100 MB лимит
                raise ValidationError('File too large. Size should not exceed 100 MB.')
        return file



class VideoEditForm(forms.Form):
    video_id = forms.IntegerField(widget=forms.HiddenInput())
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)