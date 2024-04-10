from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #home urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('broker/', views.broker, name='broker'),
    path('contact/', views.contact, name='contact'),
    path('forgotpassword/', views.forgetpassword, name='forgetpassword'),
    path('login/', views.signin, name='login'),
    path('login', views.signin, name='login'),
    path('policy/', views.policy, name='policy'),
    path('register/', views.register, name='register'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('trading/', views.trading, name='trading'),
    path('terms/', views.terms, name='terms'),

    #dashboard urls
    path('dashboard/', views.dashboard, name='dashboard'),
    path('invoice/', views.invoice, name='invoice'),
    path('deposit_invoice', views.deposit_invoice, name='deposit_invoice'),
    path('deposit/', views.deposit, name='deposit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
    path('mywallet/', views.wallet, name='mywallet'),
    path('faqs/', views.faqs, name='faqs'),
    path('profile/', views.profile, name='myprofile'),
    path('investmentplans/', views.plans, name='plans'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('logout/', views.signout, name='logout'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('verification/', views.verification, name='verification'),

   
    #passReset
    #passReset
    path('reset_password/', views.custom_password_reset, name='password_reset'),
    path('reset_password_done/', views.custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', views.custom_password_reset_complete, name='password_reset_complete'),
    #passreset



    path('microplan/', views.account_upgrade, name='microplan'),
    path('exclusiveplan/', views.account_upgrade1, name='exclusiveplan'),
    path('premiumplan/', views.account_upgrade2, name='premiumplan'),
    path('strategicplan/', views.account_upgrade3, name='strategicplan'),
    path('premierplan/', views.account_upgrade4, name='premierplan'),
    path('acceleratorplan/', views.account_upgrade5, name='acceleratorplan'),
    path('apexpremiumplan/', views.account_upgrade6, name='apexpremiumplan'),
    path('elitemasterplan/', views.account_upgrade7, name='elitemasterplan'),

]