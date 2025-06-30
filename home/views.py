from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Category, Post, subscriber
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests
from .forms import PostForm
from django.contrib.auth.models import User
# Create your views here.
def post(request, name):
    category = get_object_or_404(Category, cat_name = name)
    post = Post.objects.filter(cat = category)
    return render(request, 'post.html', {'category':category, 'post':post})

def home(request):
    post = Post.objects.all()
    return render(request, "home.html", {'post':post})

def post_detail(request, url):
    post = get_object_or_404(Post, url=url)
    return render(request, 'post_detail.html', {'post': post})

def post_by_category(request, cat_name):
    category = get_object_or_404(Category, category = cat_name)
    posts = Post.objects.filter(cat = category)
    return render(request, "post_by_category.html", {'category': category, 'posts': posts})

@login_required
def add_post(request):
    if not request.user.is_authenticated | request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to add post")
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, "add_post.html", {'form': form})
    

@login_required
def esewa_request(request):
    amt = 100
    pid = f"{request.user.id}-{timezone.now().timestamp()}"
    success_url = request.build_absolute_uri('/esewa_verify/')
    failed_url = request.build_absolute_uri('/payment_failed/')

    esewa_url = (
        f"https://rc-epay.esewa.com.np/api/epay/main?"
        f"amt={amt}&pdc=0&psc=0&txAmt=0&tAmt={amt}"
        f"&pid={pid}&scd=EPAYTEST"
        f"&su={success_url}&fu={failed_url}"
    )

    request.session['pid'] = pid
    return redirect(esewa_url)


@login_required
def esewa_verify(request):
    ref_id = request.GET.get('refid')
    pid = request.session.get('pid')
    amt = 100
    data = {
        'pid' : pid,
        'amt' : amt,
        'scd' : 'EPAYTEST',
        'rid' : ref_id,
    }

    resp = requests.post('https://rc-epay.esewa.com.np/api/epay/verify/', data=data)

    if 'Success' in resp.text:
        sub, created = subscriber.objects.get_or_create(user=request.user)
        sub.subscribe = True
        sub.paid = True
        sub.save()
        return HttpResponse("Payment successful! You are now subscribed.")
    else:
        return HttpResponse("Payment failed or invalid.")
    
@login_required
def post_delete(request, pid):
    post =  Post.objects.filter(pid =pid)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    
    return render (request, "post_delete.html", {'post':post})


@login_required
def post_edit(request, pid):
    post = get_object_or_404(Post, pid=pid)
    print(post.pid)
    print("Pradip")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, "post_edit.html", {'form':form, 'post':post})
