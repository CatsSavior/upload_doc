import datetime
import os

from django.conf import settings
from django.shortcuts import render

from .forms import Img, Video


# Название переменных должны отображать суть
# Было:
# def img_file(f, time):
# Стало:
def generate_html_by_file(file, time: datetime) -> dict:
    '''Для каждой функции пиши описание

    Функция, которая сохраняет файл картинки и возвращает HTML
    '''

    # Не исподльзуй глобальные переменные - это очень плохо
    # Лучше сделать return из функции *1
    global now, data

    # Название переменных должны отображать суть (+fstring)
    # Было:
    # i = str(now.strftime("%d-%m-%Y-%H-%M-%S"))+'.jpg'
    # Стало:

    filename = f'{time.strftime("%d-%m-%Y-%H-%M-%S")}.jpg'

    with open(os.path.join(settings.MEDIA_ROOT, filename), "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Используй f strings
    # https://realpython.com/python-f-strings/

    # file:// - это не должно так работать
    # давай пока статику будет возращать django
    # т.е. для начала

    # Было:
    # i = '<img src=\"file://path/'+i+'\" style="width: 100%; height: 100%"/>'
    # Стало:

    # *1 вот так
    return {'text': f'''<div class='my-class'>
        <img src="/static/{filename}">
    </div>'''}


def video_file(f):
    '''Пофикси функцию на подобии img_file'''
    global now, data
    i = str(now.strftime("%d-%m-%Y-%H-%M-%S")) + '.mp4'
    with open(os.path.join(settings.MEDIA_ROOT, i), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    i = '<video src=\"file://path/' + i + '\" width="100%" height="100%" autoplay/>'
    data = {'text': i}


def index(request):
    return render(request, 'index.html', locals())


# Название переменных должны отображать суть
def img(request):
    # Не исподльзуй глобальные переменные - это очень плохо
    global now, data

    # Убери глобальную переменную, добавь как аргумент к функции
    now = datetime.datetime.now()

    form = Img()

    if request.method == 'POST':
        form = Img(request.POST, request.FILES)  # Do not forget to add: request.FILES

        # Сделай 2 функции в 1
        # if form (которая Img).is_valid
        # else
        # if form2 (которая Video).is_valid
        if form.is_valid():
            # Тут я обошелся без глобальных переменных и все хорошо
            # Это просто)
            data = generate_html_by_file(request.FILES['image'], now)

            return render(request, 'after.html', context=data)

    return render(request, 'upload_doc.html', locals())


# Название переменных должны отображать суть
# Убери эту функцию и обьядени с img
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
