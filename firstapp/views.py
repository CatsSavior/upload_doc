import datetime
import os

from PIL import Image
from django.conf import settings
from django.shortcuts import render

from .forms import UploadDocumentForm


def generate_html_img(file, time: datetime) -> dict:
    # Функция, которая сохраняет файл картинки и возвращает HTML

    filename = f'{time.strftime("%d-%m-%Y-%H-%M-%S")}.jpg'
    with open(os.path.join(settings.MEDIA_ROOT, filename), "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return {'text': f'''<div class='my-class'>
        <img src="/static/{filename}">
    </div>'''}


def generate_html_video(f, time: datetime) -> dict:
    # функция, которая сохраняет файл видео и возвращает HTML

    filename = f'{time.strftime("%d-%m-%Y-%H-%M-%S")}.mp4'

    with open(os.path.join(settings.MEDIA_ROOT, filename), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return {'text': f'''<div class='my-class'>
            <video src="/static/{filename}">
        </div>'''}


def upload_doc(request):
    now = datetime.datetime.now()
    form = UploadDocumentForm()

    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                image = Image.open(request.FILES['file'])
                data = generate_html_img(request.FILES['file'], now)
            except Exception as e:
                print(e)
                if request.FILES['file'].size < 200000000:
                    data = generate_html_video(request.FILES['file'], now)
                else:
                    return render(request, "error.html", locals())

            return render(request, 'after.html', context=data)
    return render(request, 'upload_doc.html', locals())
