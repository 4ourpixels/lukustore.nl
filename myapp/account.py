from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Brand, ShippingAddress, Photo, Product, Order, OrderItem
from blog.models import BlogPost
from django.contrib import messages
from .utils import cartData
from .forms import RegisterUserForm, CustomerForm

blogs = BlogPost.objects.order_by('-pk')
brands = Brand.objects.order_by('-pk')


@login_required(login_url='login')
def account_settings(request):
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    shippings = ShippingAddress.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    customer = request.user.customer
    form = CustomerForm(instance=customer)

    title_tag = "Account Settings"
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            print(f"Succesfully updated {first_name}'s account.")
            messages.success(
                request, ('Succesfully updated account settings.'))
            return redirect('account_settings')
        else:
            form = CustomerForm(instance=customer)

    context = {
        'shippings': shippings,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'blogs': blogs,
        'brands': brands,
        'form': form,
    }

    return render(request, 'account/account_settings.html', context)


def loginPage(request):
    title_tag = "Log In"
    data = cartData(request)
    cartItems = data['cartItems']
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff:
                    messages.info(request, f'Welcome back {user.first_name}')
                    return redirect('index')
                else:
                    messages.info(
                        request, 'Register an account with us today.')
                    return redirect('register')
            else:
                messages.info(request, 'Username Or Password is incorrect')

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    meta_keywords = "Luku Store.nl Signup, Account Registration, Exclusive Offers, Fashion Updates, Socially-conscious Shopping, Personalized Account, Kenyan Fashion, Streetwear, Community Membership, Stay Connected, Diverse Style."
    title_tag = "Create Your Luku Account - Sign Up for Exclusive Offers and Fashion Updates"
    meta_description = "Join the Lukustore.nl community! Sign up for an account to access exclusive offers, stay updated on the latest Kenyan fashion trends, and be part of our socially-conscious shopping experience. Register now for a personalized shopping journey that celebrates diversity and style."
    form = RegisterUserForm()
    data = cartData(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request, ("Account registration successful, you've officially joined the cool club! Welcome aboard!"))
                return redirect('index')
        else:
            form = RegisterUserForm()
    context = {
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'cartItems': cartItems,
        'form': form,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'account/register.html', context)


@login_required(login_url='login')
def account(request):
    photos = Photo.objects.all()
    products = Product.objects.all()
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    shippings = ShippingAddress.objects.all()
    orders = Order.objects.order_by('-pk')
    order_item_list = OrderItem.objects.all()
    # title Tag
    title_tag = "Account Settings | Manage Your Luku Profile and Preferences"
    meta_description = "Customize your Lukustore.nl experience with our account settings. Update your profile, manage preferences, and stay connected with the latest Kenyan fashion. Shop consciously with Lukustore.nl."
    meta_keywords = "Lukustore, Account Settings, Profile Management, Preferences, Kenyan Fashion, Online Clothing Store, Socially-conscious Shopping, Vibrant Outfits, Handmade Clothes, Free Shipping Netherlands."
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'order_item_list': order_item_list,
        'shippings': shippings,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'photos': photos,
        'products': products,
        'orders': orders,
        'order': order,
        'items': items,
        'blogs': blogs,
        'brands': brands,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,

    }

    return render(request, 'account/account.html', context)
