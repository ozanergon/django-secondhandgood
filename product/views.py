from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from product.models import CommentForm, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    return HttpResponse("Product Page")


@login_required(login_url='/login')  # Check Login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # Access User Session information
            data = Comment()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')  # Client computer ip address
            data.save()  # veritabanına kaydet
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz")

            return HttpResponseRedirect(url)
            # return HttpResponse("Kaydedildi")
    messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)
