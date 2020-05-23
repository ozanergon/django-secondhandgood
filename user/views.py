from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.safestring import mark_safe

from home.models import UserProfile, Setting
from order.models import Order, OrderProduct
from product.models import Category, Comment, Product, ProductForm, ProductImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')  # Check login
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'setting': setting,

               }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'setting': setting,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # Check login
def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {
                          'form': form,
                          'category': category,
                          'setting': setting,
        })


@login_required(login_url='/login')  # Check login
def orders(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    orders = OrderProduct.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
        'setting': setting,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # Check login
def orderdetail(request, id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = OrderProduct.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'profile': profile,
        'setting': setting,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment delete..')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')  # Check login
def products(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    products = Product.objects.filter(user_id=current_user.id, status='True')
    context = {
        'category': category,
        'products': products,
        'setting': setting,
    }
    return render(request, 'user_products.html', context)


@login_required(login_url='/login')  # Check login
def addproduct(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Product()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.price = form.cleaned_data['price']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()  # veritabanına kaydet
            messages.success(request, 'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/products')
        else:
            messages.success(request, 'Content Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/addproduct')
    else:
        category = Category.objects.all()
        form = ProductForm()
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addproduct.html', context)


@login_required(login_url='/login')  # Check login
def productedit(request, id):
    setting = Setting.objects.get(pk=1)
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Product Updated Successfuly')
            return HttpResponseRedirect('/user/products')
        else:
            messages.success(request, 'Product Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/addproduct/' + str(id))
    else:
        category = Category.objects.all()
        form = ProductForm(instance=product)
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addproduct.html', context)


@login_required(login_url='/login')  # Check login
def productdelete(request, id):
    current_user = request.user
    Product.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Product deleted...')
    return HttpResponseRedirect('/user/products')


def productaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.product_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfuly uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error: ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        product = Product.objects.get(id=id)
        images = Images.objects.filter(product_id=id)
        form = ProductImageForm()
        context = {
            'product': product,
            'images': images,
            'form': form,
        }
        return render(request, 'product_gallery.html', context)