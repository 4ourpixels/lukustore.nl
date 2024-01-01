from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json
import datetime
from .models import *
from .forms import *
from .email import send_email_with_inline_logo
from .utils import cartData, guestOrder
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost

# Amapiano Slots Logic
import uuid


# History Logic Start
from django.contrib.admin.models import LogEntry
# History Logic End
# ABOUT US

blogs = BlogPost.objects.order_by('-pk')


def lukufam(request):
    title_tag = "About Us"
    data = cartData(request)
    cartItems = data['cartItems']

    object = AboutUs.objects.all()
    brands = Brand.objects.order_by('-pk')

    kendy = object[0]
    djg400 = object[1]
    fkinyash = object[2]
    tarela = object[3]

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        contact = ContactForm(
            name=name,
            email=email,
            message=message,
        )
        contact.save()
        return redirect('lukufam')

    context = {
        'kendy': kendy,
        'djg400': djg400,
        'fkinyash': fkinyash,
        'tarela': tarela,
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands
    }

    return render(request, 'lukufam.html', context)
# END OF ABOUT US

# HELP SECTION - DONE


def help(request):
    title_tag = "Help"

    data = cartData(request)
    cartItems = data['cartItems']
    brands = Brand.objects.order_by('-pk')

    help = Help.objects.first()
    context = {
        'help': help,
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'help.html', context)
# END OF HELP SECTION - DONE


def index(request):
    title_tag = "Home of Afro Streetwear Culture | Online Clothing Store"
    meta_description = "Immerse yourself in the rich tapestry of Kenyan culture with Luku Store.nl. Explore our latest blogs, diverse brands, new collections, and visually stunning images. Shop unique, handmade fashion that tells a story. Join our community of socially-conscious shoppers and experience the vibrancy of Kenyan style here in Amsterdam."
    meta_keywords = "Kenyan Culture, Fashion Blog, Unique Brands, New Collections, Vibrant Images, Streetwear, Handmade Clothing, Socially-conscious Shopping, Afro, Luku Store.nl, Cultural Fashion, Fashion Community, Online Clothing Store, Netherlands, Amsterdam, Young Men, Young Women, Local Designers, Unique Outfits, Colorful, Independent Clothing Designers, Reasonable Price, Stories Behind Designers."
    photos = Photo.objects.all()
    brands = Brand.objects.order_by('-pk')
    homepages = HomePage.objects.all()
    categories = Category.objects.all()
    mixes = Mix.objects.all()

    popular_items = Photo.objects.filter(popular=True)[:4]

    slide1 = homepages[0]
    slide2 = homepages[1]
    slide3 = homepages[2]

    collection = homepages[3]
    definition = homepages[4]
    new_release = homepages[5]
    jacket = homepages[6]
    sweater = homepages[7]
    trucker_hats = homepages[8]
    asorted_trucker_hats = homepages[9]
    green_trucker_hat = homepages[10]

    # Home page carousel slides
    slider_01 = homepages[11]
    slider_02 = homepages[12]
    slider_03 = homepages[13]

    # Lukubook image
    lukubookImage = get_object_or_404(Photo, pk=51)

    # Luku Inspo Images
    red_bucket_hat = homepages[14]
    kintsugi_top_blue = homepages[15]
    utility_jacket = homepages[16]
    kintsugi_flare = homepages[17]

    # Footer
    trucker_hat = homepages[18]

    video = Video.objects.first()
    videos = Video.objects.all()
    home_video_2 = videos[1]
    home_video_3 = videos[2]

    data = cartData(request)
    cartItems = data['cartItems']

    # Calculate remaining slots
    remaining_slots = 20 - AmapianoSignUp.objects.count()

    context = {
        'photos': photos,
        'blogs': blogs,
        'brands': brands,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'homepages': homepages,
        'slide1': slide1,
        'slide2': slide2,
        'slide3': slide3,
        'collection': collection,
        'definition': definition,
        'new_release': new_release,
        'jacket': jacket,
        'jacket': jacket,
        'trucker_hats': trucker_hats,
        'sweater': sweater,
        'asorted_trucker_hats': asorted_trucker_hats,
        'green_trucker_hat': green_trucker_hat,
        'categories': categories,

        'popular_items': popular_items,
        'mixes': mixes,

        'slider_01': slider_01,
        'slider_02': slider_02,
        'slider_03': slider_03,

        'lukubookImage': lukubookImage,
        'red_bucket_hat': red_bucket_hat,
        'kintsugi_top_blue': kintsugi_top_blue,
        'utility_jacket': utility_jacket,
        'kintsugi_flare': kintsugi_flare,
        'trucker_hat': trucker_hat,

        'video': video,
        'home_video_2': home_video_2,
        'home_video_3': home_video_3,
        'remaining_slots': remaining_slots,

    }
    return render(request, 'index.html', context)


def shop(request):
    brand = request.GET.get('brand')
    title_tag = "Shop Unique Kenyan Fashion at Luku Store.nl | Accessible and Stylish Clothing"
    meta_description = "Explore our collection of vibrant and accessible Kenyan fashion at Luku Store.nl. From handcrafted pieces to curated designs, discover the latest trends for unisex, men and women. Make a statement with our socially-conscious clothing. Shipping within Netherlands."
    meta_keywords = "Kenyan Fashion, Accessible Clothing, Stylish Outfits, Online Fashion Store, Handmade Clothes, Curated Designs, Socially-conscious Shopping, Men's Fashion, Women's Fashion, Unisex, Luku Store.nl, Netherlands Fashion, Shipping."
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('pk')
    stocks = Stock.objects.all()
    # stocks = Stock.objects.filter(online=True).order_by('-priority')

    unique_product_codes = Photo.objects.filter(
        product_code__isnull=False).values_list('product_code', flat=True).distinct()
    unique_photos = []

    for product_code in unique_product_codes:
        latest_photo = Photo.objects.filter(
            product_code=product_code).order_by('pk').first()
        unique_photos.append(latest_photo)

    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']

    sorted_brands = Brand.get_brands_sorted_by_online_stock()

    if brand is not None:
        stocks = Stock.objects.filter(brand__name=brand, online=True)
    else:
        stocks = Stock.objects.filter(online=True)

    sorted_brands = Brand.get_brands_sorted_by_online_stock()

    active_brand = request.GET.get('brand', None)

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'latest_photo': latest_photo,
        'unique_photos': unique_photos,
        'categories': categories,
        'blogs': blogs,
        'brands': brands,
        "meta_description": meta_description,
        'meta_keywords': meta_keywords,
        'stocks': stocks,
        'sorted_brands': sorted_brands,
        'active_brand': active_brand,
    }

    return render(request, 'shop.html', context)


def view_stock(request, slug):
    product = get_object_or_404(Stock, slug=slug)
    photos = Stock.objects.all()

    other_images = [
        product.image_original_size,
        product.image_large_size,
        product.image_medium_size,
        product.image_thumbnail_size,
    ]

    try:
        similar_products_codes = product.similar_products_codes.split(',')
        similar_products = Stock.objects.filter(
            Q(product_code__in=similar_products_codes) | Q(
                item__in=similar_products_codes)
        )
    except:
        pass

    data = cartData(request)
    cartItems = data['cartItems']
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    product_images = []

    for image in other_images:
        if image.name == "placeholder.png":
            pass
        else:
            product_images.append(image)

    title_tag = product.item

    context = {
        'product': product,
        'cartItems': cartItems,
        'photos': photos,
        'title_tag': title_tag,
        'blogs': blogs,
        'other_images': other_images,
        'brands': brands,
        'product_images': product_images,
        'similar_products': similar_products,
    }

    return render(request, 'view_stock.html', context)
# CART


def error404(request):
    page = "- Error"

    context = {
        'page': page,
    }
    return render(request, '404.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    title_tag = f"Cart({cartItems})"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'title_tag': title_tag,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'cart.html', context)

# END OF CART

# CHECKOUT


def checkout(request):
    title_tag = "Checkout"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    # data = cartData(request)
    # cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'title_tag': title_tag,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'checkout.html', context)

# END OF CHECKOUT
# Brands Start


def brand_list(request):
    title_tag = "Brands"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'title_tag': title_tag,
        'brands': brands,
    }
    return render(request, 'brand_list.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.order_by('-pk')
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    title_tag = brand.name
    # Filter stocks based on the specified brand
    stocks = Stock.objects.filter(brand=brand).order_by('-priority')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'blogs': blogs,
        'title_tag': title_tag,
        'brands': brands,
        'brand': brand,
        'products': products,
        'stocks': stocks,
    }
    return render(request, 'brand_detail.html', context)


def newsletter(request):
    title_tag = "Newsletter"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data.get('email')
            if Newsletter.objects.filter(email=email).exists():
                messages.info(
                    request, "Hey superstar, you're already one of our favorites! Keep an eye on your inbox for more amazing content. You're officially ahead of the curve!")
            else:
                newsletter_form.save()
                print(f"{email} subscribed to our newsletter from the homepage!")
                messages.success(
                    request, "You just unlocked VIP access to our exclusive updates! Stay tuned for the hottest news and insider tips we've got lined up just for you.")
            # Get the referring page's URL
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer or 'index')
    else:
        newsletter_form = NewsletterForm()

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'brands': brands,
        'newsletter_form': newsletter_form,
    }

    return render(request, 'newsletter.html', context)

# cart update item view


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# end of cart update item view


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    messages.success(request, ("Payment Complete!"))
    return JsonResponse('Payment Complete!', safe=False)

# Trial cart update item view


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(f'{action}ed the product {productId}')

    customer = request.user.customer
    product = Product.objects.get(product_code=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# end of cart update item view


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print("TRANSACTION ID: ==>> ", transaction_id)
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    messages.success(request, ("Payment Complete!"))
    return JsonResponse('Payment Complete!', safe=False)

# customer


def confirmed(request):
    title_tag = "Order Complete!"
    data = cartData(request)
    cartItems = data['cartItems']
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'success': True,
        'blogs': blogs,
        'brands': brands,
    }

    return render(request, 'confirmed.html', context)


def music(request):
    title_tag = "DJ G400 Mixes"
    mixes = Mix.objects.all()
    latest_mix = mixes[2]
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'title_tag': title_tag,
        'mixes': mixes,
        'latest_mix': latest_mix,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music.html', context)


def music_player(request, slug):
    mix = Mix.objects.get(slug=slug)
    mixes = Mix.objects.all()
    title_tag = f"Playing {mix.title}"
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    context = {
        'title_tag': title_tag,
        'mix': mix,
        'mixes': mixes,
        'blogs': blogs,
        'brands': brands,
    }
    return render(request, 'music_player.html', context)


@login_required(login_url='index')
def dashboard(request):
    stocks = Stock.objects.all()
    total_pieces = Stock.objects.first().total_pieces()
    total_consigment = Stock.objects.first().total_consigment()
    grand_total_cost = Stock.objects.first().grand_total_cost()
    total_amount_T = Stock.objects.first().total_amount_T()
    brands = Brand.objects.all()
    euro_exchange_rate = int(155)
    euro_converted_total_consigment = round(
        int(grand_total_cost) / euro_exchange_rate)
    amapiano_signups = AmapianoSignUp.objects.all()
    spectra_talks_signups = SpectraTalksSignUp.objects.all()
    blog_posts = BlogPost.objects.all()

    title_tag = "Dashboard"
    admin_actions = LogEntry.objects.order_by('-action_time')[:10]
    context = {
        'title_tag': title_tag,
        'stocks': stocks,
        'total_pieces': total_pieces,
        'total_consigment': total_consigment,
        'grand_total_cost': grand_total_cost,
        'total_amount_T': total_amount_T,
        'euro_converted_total_consigment': euro_converted_total_consigment,
        'admin_actions': admin_actions,
        'brands': brands,
        'amapiano_signups': amapiano_signups,
        'spectra_talks_signups': spectra_talks_signups,
        'blog_posts': blog_posts,
    }

    return render(request, 'dashboard.html', context)


# Amapiano Workshop Signup Logic Start


def amapiano_workshop_signup(request):
    title_tag = "Amapiano Workshop Signup"
    form = AmapianoSignUpForm()
    remaining_slots = 20 - AmapianoSignUp.objects.count()

    if request.method == 'POST':
        form = AmapianoSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if the email already exists in the database
            if AmapianoSignUp.objects.filter(email=email).exists():
                messages.error(
                    request, ('This email is already registered. Please use a different email.'))
                return redirect('index')

            if remaining_slots > 0:
                user_signup = form.save(commit=False)
                user_signup.consent = form.cleaned_data.get('consent')
                user_signup.ticket_number = str(uuid.uuid4())[:8]
                user_signup.save()

                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                consent = user_signup.consent
                ticket_number = user_signup.ticket_number
                short_ticket_number = ticket_number[:8]

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nConsent: {consent}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                # Send email with inline logo
                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Amapiano Workshop Registration Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            else:
                form.save()
                messages.error(
                    request, ('Sorry, all slots have been filled.'))
                return redirect('index')
        else:
            form = AmapianoSignUpForm()

    context = {
        'title_tag': title_tag,
        'form': form,
        'remaining_slots': remaining_slots,
    }

    return render(request, 'events/amapiano.html', context)
# Amapiano Workshop Signup Logic End

# ACCOUNT


def view_stock_details(request, slug):
    stock = Stock.objects.get(slug=slug)
    return HttpResponseRedirect(reverse('dashboard'))


def edit_stock(request, slug):
    stock = get_object_or_404(Stock, slug=slug)
    title_tag = f"Update: {stock.item}"

    images = [
        stock.image_original_size,
        stock.image_large_size,
        stock.image_medium_size,
        stock.image_thumbnail_size,
        stock.thumbnail,
    ]

    if request.method == 'POST':
        form = StockForm(request.POST, request.FILES, instance=stock)

        if form.is_valid():
            form.save()
            return render(request, 'edit_stock.html', {
                'form': form,
                'success': True
            })
        else:
            print("Errors occurred while uploading: ",
                  form.errors)
    else:
        form = StockForm(instance=stock)

    context = {
        'form': form,
        'images': images,
        'title_tag': title_tag,
        'stock': stock,
    }

    return render(request, 'edit_stock.html', context)


def delete_stock(request, slug):
    if request.method == 'POST':
        stock = Stock.objects.get(slug=slug)
        stock.delete()
    return HttpResponseRedirect(reverse('dashboard'))


def add_stock_photo(request):
    brands = Brand.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['brand'] != 'none':
            brand = Brand.objects.get(slug=data['brand'])
        elif data['brand_new'] != '':
            brand, created = Brand.objects.get_or_create(
                name=data['brand_new'])
        else:
            brand = None

        for image in images:
            photo = StockPhoto.objects.create(
                name=data['name'],
                brand=brand,
                product_code=data['product_code'],
                similar_products_codes=data['similar_products_codes'],
                image=image,
            )
        return redirect('dashboard')

    context = {
        'brands': brands,
    }
    return render(request, 'add_stock_photo.html', context)

# Stock Logic End


# spectra Talks Signup Logic Start


def spectra_talks_signup(request):
    title_tag = "spectra Talks with Luku Store.nl & WhoWhatWhereKE Signup"
    spectra_talks_signup_form = SpectraTalksSignUpForm()

    if request.method == 'POST':
        spectra_talks_signup_form = SpectraTalksSignUpForm(request.POST)
        if spectra_talks_signup_form.is_valid():
            email = spectra_talks_signup_form.cleaned_data.get('email')

            # Check if the email already exists in the database
            if SpectraTalksSignUp.objects.filter(email=email).exists():
                messages.error(
                    request, ('The email you entered is already registered. Please use a different one.'))
                return redirect('spectra_talks')

            try:
                user_signup = spectra_talks_signup_form.save(commit=False)
                user_signup.consent = spectra_talks_signup_form.cleaned_data.get(
                    'consent')
                user_signup.ticket_number = str(uuid.uuid4())[:8]
                user_signup.save()

                first_name = spectra_talks_signup_form.cleaned_data.get(
                    'first_name')
                last_name = spectra_talks_signup_form.cleaned_data.get(
                    'last_name')
                email = spectra_talks_signup_form.cleaned_data.get('email')
                consent = user_signup.consent
                ticket_number = user_signup.ticket_number
                short_ticket_number = ticket_number[:8]

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nConsent: {consent}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                # Send email with inline logo
                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Registration to 'spectra Talks with Luku Store.nl & WhoWhatWhereKE' Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            except:
                spectra_talks_signup_form.save()
                messages.error(
                    request, ('Unable to register. Your details were correct, but we could not save them due to a technical issue on our end. Please registering again. If the issue keeps happening, contact us at info@lukustore.nl'))
                return redirect('spectra_talks')
        else:
            spectra_talks_signup_form = SpectraTalksSignUpForm()

    context = {
        'title_tag': title_tag,
        'spectra_talks_signup_form': spectra_talks_signup_form,
    }

    return render(request, 'events/spectra_talks.html', context)
# spectra Talks Signup Logic End
