from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from order.models import Order, OrderForm, OrderProduct
from product.models import Category, Product


def index(request):
    return HttpResponse("Order App")


@login_required(login_url='/login')  # Check login
def orderproduct(request, id):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    current_user = request.user
    total = product.price

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            orderproduct = OrderProduct()
            orderproduct.order = data
            orderproduct.price = total
            orderproduct.user = current_user
            orderproduct.product = product
            orderproduct.amount = 1
            orderproduct.quantity = 1
            orderproduct.save()

            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode, 'category': category})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct/" + str(id))

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               'product': product,
               }
    return render(request, 'Order_Form.html', context)
