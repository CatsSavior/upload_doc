from django import forms


class UploadDocumentForm(forms.Form):
    video = forms.FileField()
    image = forms.ImageField()

class Img(forms.Form):
    image = forms.ImageField()

class Video(forms.Form):
    video = forms.FileField()
