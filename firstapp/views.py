from django.shortcuts import render
from .forms import UploadDocumentForm, Img, Video
from django.conf import settings
import os

import datetime

def img_file(f):
    global now, data
    i = str(now.strftime("%d-%m-%Y-%H-%M-%S"))+'.jpg'
    with open(os.path.join(settings.MEDIA_ROOT, i), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    i = '<img src=\"file://path/'+i+'\" style="width: 100%; height: 100%"/>'
    data = {'text': i}

def video_file(f):
    global now, data
    i = str(now.strftime("%d-%m-%Y-%H-%M-%S"))+'.mp4'
    with open(os.path.join(settings.MEDIA_ROOT, i), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    i = '<video src=\"file://path/'+i+'\" width="100%" height="100%" autoplay/>'
    data = {'text': i}

def index(request):
    return render(request, 'index.html', locals())

def img(request):
    global now, data
    now = datetime.datetime.now()
    form = Img()
    if request.method == 'POST':
        form = Img(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if form.is_valid():
            img_file(request.FILES['image'])
            return render(request, 'after.html', context=data)
    return render(request, 'upload_doc.html', locals())

def video(request):
    global now, data
    now = datetime.datetime.now()
    form = Video()
    if request.method == 'POST':
        form = Video(request.POST, request.FILES)
        if form.is_valid():
            video_file(request.FILES['video'])
            return render(request, 'after.html', context=data)
    return render(request, 'upload_doc.html', locals())

