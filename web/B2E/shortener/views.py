from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from shortener import models

from shortener.my_queue import PythonQueue, RedisQueue


# py_queue = PythonQueue()
redis_queue = RedisQueue('b2e')
base_64 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'


def int_to_64(n):
    '''
        Number to base64
        n: int
        return: string
    '''
    if n == 0:
        return '0'
    r = []
    while n > 0:
        r.append(base_64[n % 64])
        n = n // 64
    return ''.join(r[::-1])


@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')


@require_http_methods(["POST"])
def create(request):
    # new_id = py_queue.get()
    # py_queue.put(new_id+py_queue.queue_len)
    # print(py_queue.qsize())
    new_id = int(redis_queue.get()[1])
    redis_queue.put(new_id+redis_queue.queue_len)

    new_row = models.ShortURL(id=new_id)
    new_row.full_url = request.POST['full_url']
    new_row.short_url = int_to_64(new_row.id)
    new_row.save()
    return redirect(f'/shortener/create/success?short_url={new_row.short_url}')


@require_http_methods(["GET"])
def create_success(request):
    short_url = request.GET.get('short_url', '')
    data = models.ShortURL.objects.filter(short_url=short_url)
    if len(data) == 0:
        return render(request, 'error.html')
    context = {'short_url': f"http://localhost:8000/shortener/{short_url}"}
    return render(request, 'create_success.html', context)


@require_http_methods(["GET"])
def short_url_redirect(request, short_url):
    # data = models.ShortURL.objects.get(short_url=short_url)
    data = models.ShortURL.objects.filter(short_url=short_url)
    if len(data) == 0:
        return render(request, 'error.html')
    return redirect(f'{data[0].full_url}')