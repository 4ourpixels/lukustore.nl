from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from .email import send_email_with_inline_logo
from .utils import cartData
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost
import uuid
from django.contrib.admin.models import LogEntry
blogs = BlogPost.objects.order_by('-pk')
# ABOUT US


def about(request):
    title_tag = "Luku Fam | About Us"
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
        return redirect('about')

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

    return render(request, 'about.html', context)
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
    remaining_slots = 43 - SpectraTalksSignUp.objects.count()

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
    products = Product.objects.all()
    # products = product.objects.filter(online=True).order_by('-priority')

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

    if brand is not None:
        products = Product.objects.filter(brand__name=brand, online=True)
    else:
        products = Product.objects.filter(online=True)

    # sorted_brands = Brand.get_brands_sorted_by_online_product()
    sorted_brands = Brand.objects.all()
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
        'products': products,
        'sorted_brands': sorted_brands,
        'active_brand': active_brand,
    }

    return render(request, 'shop.html', context)


def view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    photos = Product.objects.all()
    product_code = str(f'ls0{product.pk}')

    other_images = [
        product.img_xl,
        product.img_lg,
        product.img_md,
        product.img_sm,
        product.thumbnail,
    ]

    try:
        similar_products_codes = product.similar_products_codes.split(',')
        similar_products = Product.objects.filter(
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

    all_product_photos = ProductPhoto.objects.all()
    photos = []

    for photo in all_product_photos:
        if photo.product_code == product_code:
            photos.append(photo.image)

    try:
        product_img = photos[0]
    except:
        product_img = product.thumbnail

    try:
        sizes_object = product.size.split(',')
        sizes = [size.strip() for size in sizes_object]
    except:
        sizes = product.size

    context = {
        'product': product,
        'cartItems': cartItems,
        'photos': photos,
        'title_tag': title_tag,
        'blogs': blogs,
        'other_images': other_images,
        'brands': brands,
        'product_images': product_images,
        'photos': photos,
        'product_img': product_img,
        'sizes': sizes,
        'similar_products': similar_products,
    }

    return render(request, 'product/view_product.html', context)
# CART


def error404(request):
    page = "Error"
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

    return render(request, 'checkout/cart.html', context)

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

    return render(request, 'checkout/checkout.html', context)

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
    return render(request, 'brands/brand_list.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.order_by('-pk')
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    title_tag = brand.name
    products = Product.objects.filter(brand=brand).order_by('-priority')

    filtered_blogs = BlogPost.objects.filter(
        Q(tag__name__icontains=brand.name) |
        Q(category__name__icontains=brand.name) |
        Q(author__username__icontains=brand.name) |
        Q(content__icontains=brand.name) |
        Q(title__icontains=brand.name)
    ).distinct()

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'cartItems': cartItems,
        'filtered_blogs': filtered_blogs,
        'title_tag': title_tag,
        'brands': brands,
        'brand': brand,
        'products': products,
        'products': products,
        'blogs': blogs,
    }
    return render(request, 'brands/brand_detail.html', context)


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
    products = Product.objects.all()
    total_pieces = Product.objects.first().total_pieces()
    total_consigment = Product.objects.first().total_consigment()
    grand_total_cost = Product.objects.first().grand_total_cost()
    total_amount_T = Product.objects.first().total_amount_T()
    brands = Brand.objects.all()
    euro_exchange_rate = int(155)
    euro_converted_total_consigment = round(
        int(grand_total_cost) / euro_exchange_rate)
    amapiano_signups = AmapianoSignUp.objects.order_by('-pk')
    spectra_talks_signups = SpectraTalksSignUp.objects.all()
    num_spectra_talks_signups = SpectraTalksSignUp.objects.all().count()
    blog_posts = BlogPost.objects.all()

    product_object = Product.objects.all()
    online_products = Product.objects.filter(online=True).all()

    product_codes = []
    below_twenty = []

    online_product_codes = []
    all_online_products = []

    for product in product_object:
        if product.buying_price == 0:
            pass
        elif product.buying_price <= 25:
            below_twenty.append(product)

    for code in product_object:
        new_code = str(f"ls0{code.pk}")
        product_codes.append(new_code)

    for product in online_products:
        if product.online:
            online_product_codes.append(str(f"ls0{product.pk}"))

    for product in online_products:
        if product.online:
            all_online_products.append(product)

    title_tag = "Dashboard"
    admin_actions = LogEntry.objects.order_by('-action_time')[:10]
    context = {
        'title_tag': title_tag,
        'products': products,
        'total_pieces': total_pieces,
        'total_consigment': total_consigment,
        'grand_total_cost': grand_total_cost,
        'total_amount_T': total_amount_T,
        'euro_converted_total_consigment': euro_converted_total_consigment,
        'admin_actions': admin_actions,
        'brands': brands,
        'amapiano_signups': amapiano_signups,
        'spectra_talks_signups': spectra_talks_signups,
        'num_spectra_talks_signups': num_spectra_talks_signups,
        'blog_posts': blog_posts,
        'product_codes': product_codes,
        'online_product_codes': online_product_codes,
        'all_online_products': all_online_products,
        'below_twenty': below_twenty,
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


def view_product_details(request, slug):
    product = Product.objects.get(slug=slug)
    return HttpResponseRedirect(reverse('dashboard'))


def edit_product(request, slug):
    context = {}
    product = get_object_or_404(Product, slug=slug)
    title_tag = f"Update: {product.item}"

    all_product_photos = ProductPhoto.objects.all()
    photos = []

    for photo in all_product_photos:
        if photo.product_code == product.product_code:
            photos.append(photo.image)

    try:
        product_img = photos[0]
    except:
        product_img = product.thumbnail

    images = [
        product.img_xl,
        product.img_lg,
        product.img_md,
        product.img_sm,
        product.thumbnail,
    ]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return render(request, 'product/edit_product.html', {
                'form': form,
                'success': True
            })
        else:
            print("Errors occurred while uploading: ",
                  form.errors)
    else:
        form = ProductForm(instance=product)

    context.update({
        'form': form,
        'images': images,
        'title_tag': title_tag,
        'product_img': product_img,
        'photos': photos,
        'product': product,
    })

    return render(request, 'product/edit_product.html', context)


def delete_product(request, slug):
    if request.method == 'POST':
        product = Product.objects.get(slug=slug)
        product.delete()
    return HttpResponseRedirect(reverse('dashboard'))


def add_product_photo(request):
    brands = Brand.objects.all()
    title_tag = "Add Product Photo"

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
            photo = ProductPhoto.objects.create(
                name=data['name'],
                brand=brand,
                product_code=data['product_code'],
                similar_products_codes=data['similar_products_codes'],
                image=image,
            )
        return redirect('dashboard')

    context = {
        'brands': brands,
        'title_tag': title_tag,
    }
    return render(request, 'product/add_product_photo.html', context)

# product Logic End


# spectra Talks Signup Logic Start


def spectra_talks_signup(request):
    title_tag = "spectra Talks with Luku Store.nl & WhoWhatWhereKE Signup"
    spectra_talks_signup_form = SpectraTalksSignUpForm()
    remaining_slots = 43 - SpectraTalksSignUp.objects.count()

    if request.method == 'POST':
        spectra_talks_signup_form = SpectraTalksSignUpForm(request.POST)
        if spectra_talks_signup_form.is_valid():
            email = spectra_talks_signup_form.cleaned_data.get('email')

            if SpectraTalksSignUp.objects.filter(email=email).exists():
                messages.error(
                    request, ('Successfylly registered'))
                return redirect('index')

            if remaining_slots > 0:
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
                consent = user_signup.consent

                if consent:
                    print("New subscriber!")
                    consent_status = "Subscribed"
                elif consent == "Unknown":
                    print("Consent Unknown")
                    consent_status = "Unknown"
                else:
                    consent_status = "Unsbscribed"
                    print(f"{first_name} Unsibscribed :(")

                print(
                    f"\n\n++++++SIGNUP DETAILS START+++++\n\nTicket Number: {ticket_number}\n{first_name} {last_name} registered with {email}\nSubscription status: {consent_status}\nShort Ticket No: #{short_ticket_number}\n\n++++++SIGNUP DETAILS END+++++\n\n")

                send_email_with_inline_logo(
                    email, first_name, short_ticket_number)

                messages.success(
                    request, (f"Hey {first_name}! Your Registration to 'spectra Talks with Luku Store.nl & WhoWhatWhereKE' Was Successful! Check your email for the ticket and event details."))
                return redirect('index')
            else:
                spectra_talks_signup_form.save()
                messages.error(
                    request, ("We appreciate your interest! As we've reached full capacity, keep an eye on our announcements for details on the next event. Stay connected through our newsletter or social channels to be the first to know."))
                return redirect('index')
        else:
            spectra_talks_signup_form = SpectraTalksSignUpForm()

    context = {
        'title_tag': title_tag,
        'remaining_slots': remaining_slots,
        'spectra_talks_signup_form': spectra_talks_signup_form,
    }

    return render(request, 'events/spectra_talks.html', context)
# spectra Talks Signup Logic End


def allProductPhotos(request):
    photos = ProductPhoto.objects.all()
    title_tag = "All product Photos"

    context = {
        'photos': photos,
        'title_tag': title_tag,
    }
    return render(request, 'dashboard/all-photos.html', context)


def viewProductPhoto(request, pk):
    photo = get_object_or_404(ProductPhoto, pk=pk)
    title_tag = photo.name

    context = {
        'photo': photo,
        'title_tag': title_tag,
    }
    return render(request, 'dashboard/view-photo.html', context)


def search_result(request):
    title_tag = f'"{request.GET.get("q")}" results'
    context = {
        "title_tag": title_tag,
    }
    return render(request, "search.html", context)
