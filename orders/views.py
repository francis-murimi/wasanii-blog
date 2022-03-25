from django.shortcuts import render, get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from shop.models import Category,Art
from .models import Order, Bids
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import OrderUpdateForm


@login_required(login_url='/login/')
def my_orders(request):
    username = request.user.id
    orders = Order.objects.filter(orderer = request.user)
    paid_orders = Order.objects.filter(orderer=username,paid=True)
    unpaid_orders = Order.objects.filter(orderer=username,paid=False)
    context = {'paid_orders':paid_orders,'unpaid_orders':unpaid_orders}
    template = loader.get_template('orders/orders.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'orders/detail.html',{'order': order})

@login_required(login_url='/login/')
def order_update(request,order_id):
    order = get_object_or_404(Order, id= order_id) 
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST,request.FILES,instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:my_orders')
    else:
        form = OrderUpdateForm(instance=order)
    template = loader.get_template('orders/order_update.html')
    context = {'form':form}
    return HttpResponse(template.render(context,request))  