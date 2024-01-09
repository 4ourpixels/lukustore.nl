from django.urls import path
from .import views
from .checkout import updateItem, processOrder, confirmed
from blog.views import add_blog
from .account import account, account_settings, loginPage, logoutUser, registerPage

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('lukufam/', views.about, name='about'),
    path('account/', account, name='account'),
    path('settings/', account_settings, name='account_settings'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('add-blog/', add_blog, name='add_blog'),
    path('register/', registerPage, name='register'),
    path('cart/', views.cart, name='cart'),
    path('confirmed/', confirmed, name='confirmed'),
    path('checkout/', views.checkout, name='checkout'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('help/', views.help, name='help'),
    path('updateItem/', updateItem, name='updateItem'),
    path('processOrder/', processOrder, name='processOrder'),
    path('music/', views.music, name='music'),
    path('music/mix/DJ-G400/<slug:slug>/',
         views.music_player, name='music_player'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('404/', views.error404, name='error404'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('amapiano/', views.amapiano_workshop_signup,
         name='amapiano_workshop_signup'),
    path('shop/<slug:slug>/', views.view_product, name='view_product'),
    path('edit_product/<slug:slug>/', views.edit_product, name='edit_product'),
    path('delete_product/<slug:slug>/',
         views.delete_product, name='delete_product'),
    path('add_product_photo/', views.add_product_photo, name='add_product_photo'),
    path('event/Spectra-Talks-with-Luku-Store-nl-and-WhoWhatWhereKE/',
         views.spectra_talks_signup, name='spectra_talks_signup'),

    path('all-product-photos/', views.allProductPhotos, name='allProductPhotos'),
    path('view-product-photo/<int:pk>',
         views.viewProductPhoto, name='viewProductPhoto'),

    path('search/', views.search_result, name='search_result'),
]
