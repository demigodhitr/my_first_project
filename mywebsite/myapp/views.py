from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
import requests
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
import random
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.

def custom404(request, exception):
    return render(request, '404.html', {}, status=404)

def custom403(request, exception):
    return render(request, '404.html', {}, status=403)

def custom500(request, exception):
    return render(request, '404.html', {}, status=500)





def home(request):
        # CoinGecko API key
    
    coin_gecko_api_key = 'CG-ijyB17U95TbbzxurdFzBKi6H'


    coin_gecko_endpoint = 'https://api.coingecko.com/api/v3/coins/markets'
    

    crypto_ids =['bitcoin', 'ethereum', 'litecoin', 'ripple', 'cardano', 'tether', 'polygon', 'solana', 'polkadot', 'dogecoin', 'chainlink', 'avalanche']
    
    # parameters for the API request
    coin_gecko_params = {
        'vs_currency': 'usd',
        'ids': ','.join(crypto_ids),
        'order': 'market_cap_desc',
        'sparkline': 'false',
        'price_change_percentage': '24h',
        'key': coin_gecko_api_key,
    }

    coin_gecko_response = requests.get(coin_gecko_endpoint, params=coin_gecko_params)


    if coin_gecko_response.status_code == 200:
        coins_data = coin_gecko_response.json()
    else:
        coins_data = []
    return render(request, 'index.html', {'coins_data':coins_data})

def about(request):
    return render(request, 'about.html')

def broker(request):
    return render(request, 'broker.html')


def contact(request):
    if request.method == "POST":
        fullName = request.POST.get("fullName")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not (fullName and email and message):
            messages.error(request, 'Please fill all the fields to send your message', extra_tags='message')
            return render(request, 'contact.html')
        if len(fullName) < 5:
            messages.error(request, 'Please enter your Full Name', extra_tags='message')
            return render(request, 'contact.html')

        message = ClientMessages(
            fullName=fullName,
            email=email,
            message=message,
        ) 
        message.save()

        subject = f'Thank you {message.fullName}!'
        context = {'name': fullName, 'email':email}
        html_message = render_to_string('message_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'info@bitprofitonline.com' 
        recipient_list = [message.email]

        email_backend = get_connection(backend=settings.EMAIL_BACKEND)
        email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list,connection=email_backend)
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {message.fullName} Just sent you a message!'
        email_message = f'A user named {message.fullName} Just sent you a message on your website, the user said: {message.message}. To reply, tap on the user\'s email address {message.email}'
        from_email = 'alerts@propipmarkets.com' 
        recipient_list = ['support@propipmarkets.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()

        messages.success(request, 'Your message has  been sent. you will receive a response via the provided email address. stay tuned!', extra_tags='message')
        return render(request, 'contact.html')
    

    return render(request, 'contact.html')



def forgetpassword(request):
    return render(request, 'password_reset_form_custom.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful...', extra_tags='login')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password, check your details and try again.', extra_tags='login')

    return render(request, 'login.html')

def policy(request):
    return render(request, 'policy.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_image = request.FILES.get('profile_image')
        nationality = request.POST.get('country')
        bio = 'None'

        if not (first_name and last_name and username and email and password1 and password2):
            messages.error(request, 'All fields are required.', extra_tags='registration')
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.', extra_tags='registration')
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.', extra_tags='registration')
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.', extra_tags='registration')
            return render(request, 'register.html')


        user = CustomUser.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        AccountInfo.objects.create(user=user, profile_image=profile_image, nationality=nationality, bio=bio)
        login(request, user)

        subject = 'You have a new registered user!'
        email_message = f'A user named {first_name} Just registered on your website with the following details. Email address: {email}, Full name: {first_name} {last_name}, Nationality: {nationality}, & Username: {username}. To see or manipulate user\'s full details, log into your administrator account.'
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = ['support@bitprofitonline.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        messages.success(request, 'Registration successful. Loading your dashboard...', extra_tags='registration')

        return redirect('dashboard')

    return render(request, 'register.html')



def roadmap(request):
    return render(request, 'roadmap.html')

def trading(request):
    return render(request, 'tarding.html')

def terms(request):
    return render(request, 'terms-condition.html')


# dashboard


@login_required
def dashboard(request):
    logged_in_user = request.user
    user_info = CustomUser.objects.get(pk=logged_in_user.pk)
    notifications = newNotifications.objects.filter(user=logged_in_user)
    account_info = AccountInfo.objects.get(user=logged_in_user)




    coin_gecko_api_key = 'CG-ijyB17U95TbbzxurdFzBKi6H'


    coin_gecko_endpoint = 'https://api.coingecko.com/api/v3/coins/markets'
    

    crypto_ids = ['bitcoin', 'ethereum', 'litecoin', 'ripple', 'cardano', 'tether', 'polygon', 'solana', 'polkadot', 'dogecoin', 'chainlink', 'avalanche', 'uniswap', 'monero', 'tron', 'stellar', 'eos']

    coin_gecko_params = {
        'vs_currency': 'usd',
        'ids': ','.join(crypto_ids),
        'order': 'market_cap_desc',
        'sparkline': 'false',
        'price_change_percentage': '24h',
        'key': coin_gecko_api_key,
    }

    coin_gecko_response = requests.get(coin_gecko_endpoint, params=coin_gecko_params)

    if coin_gecko_response.status_code == 200:
        coins_data = coin_gecko_response.json()
    else:
        coins_data = []

    return render(request, 'index-3.html', {
        'user': logged_in_user,
        'user_info': user_info,
        'notifications': notifications,
        'account_info': account_info,
        'profile_image': account_info.profile_image,
        'coins_data': coins_data,
    })


def comingsoon(request):
    return render(request, 'coming-soon.html')


@login_required
def wallet(request):
    return render(request, 'crypto-wallet.html')

def faqs(request):
    if request.method == "POST":
        fullName = request.POST.get("fullName")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not (fullName and email and message):
            messages.error(request, 'Please fill all the fields to send your message', extra_tags='message')
            return render(request, 'faqs.html')
        if len(fullName) < 5:
            messages.error(request, 'Please enter your Full Name', extra_tags='message')
            return render(request, 'faqs.html')
        
        if len(message) < 20:
            messages.error(request,'Add more informations to your message to help us understand you better', extra_tags='message')
            return render(request, 'faqs.html')

        message = ClientMessages(
            fullName=fullName,
            email=email,
            message=message,
        ) 
        message.save()
        subject = f'Thank you {message.fullName}!'
        context = {'name': fullName, 'email':email}
        html_message = render_to_string('message_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'info@bitprofitonline.com' 
        recipient_list = [message.email]

        email_backend = get_connection(backend=settings.EMAIL_BACKEND)
        email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list,connection=email_backend)
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {message.fullName} Just sent you a message!'
        email_message = f'A user named {message.fullName} Just sent you a message on your website, the user said: "{message.message}". To reply, tap on the user\'s email address {message.email}'
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = ['support@bitprofitonline.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()

        messages.success(request, 'Your message has  been sent. you will receive a response via the provided email address. stay tuned!', extra_tags='message')
        return render(request, 'faqs.html')
        
        
    return render(request, 'faqs.html')


@login_required
def profile(request):
    logged_in_user = request.user
    notifications = newNotifications.objects.filter(user=logged_in_user)
    info = CustomUser.objects.get(pk=logged_in_user.pk)
    account_info = AccountInfo.objects.get(user=logged_in_user)

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        oldpassword = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        bio = request.POST.get('bio')
        photo = request.FILES.get('photo') 

        if oldpassword and not logged_in_user.check_password(oldpassword):
            messages.error(request, 'Invalid old password.')
            return render(request, 'profile.html', {
                'user': logged_in_user,
                'info': info,
                'profile_image': account_info.profile_image,
                'notifications': notifications,
                'account_info':account_info,
            })

        if  password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'profile.html', {
                'user': logged_in_user,
                'info': info,
                'profile_image': account_info.profile_image,
                'notifications': notifications,
                'account_info':account_info,
            })

        if firstname:
            info.first_name = firstname
        if lastname:
            info.last_name = lastname
        if bio:
            account_info.bio = bio

        if password1:
            logged_in_user.set_password(password1)
            logged_in_user.save()

        if photo:
            account_info.profile_image = photo

        info.save()
        account_info.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('myprofile')

    return render(request, 'profile.html', {
        'user': logged_in_user,
        'info': info,
        'profile_image': account_info.profile_image,
        'notifications': notifications,
        'account_info':account_info,
    })




def plans(request):
    return render(request, 'pricing.html')

def changepassword(request):
    return render(request, 'changepassword.html')


def signout(request):
    logout(request)
    return redirect('home')

# PASSWORD RESET VIEWS

def custom_password_reset(request):
    return PasswordResetView.as_view(
        template_name='password_reset_form_custom.html'
    )(request)

def custom_password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm_custom.html'
    )(request, uidb64=uidb64, token=token)

def custom_password_reset_done(request):
    return PasswordResetDoneView.as_view(
        template_name='password_reset_done_custom.html'
    )(request)

def custom_password_reset_complete(request):
    return PasswordResetCompleteView.as_view(
        template_name='password_reset_complete_custom.html'
    )(request)


# WITHDRAWAL FUNCTIONS


@login_required
def withdrawal(request):
    user = request.user
    account_info = AccountInfo.objects.get(user=user)
    user_info = CustomUser.objects.get(pk=user.pk)
    notifications = newNotifications.objects.filter(user=user)
    

    if account_info.TradeIsActive:
        messages.error(request, "You cannot make withdrawals while your trade is active. Please wait until your trade is completed.", extra_tags='withdrawal')
        return render(request, 'index-3.html',  {
            'user': user,
            'user_info': user_info,
            'notifications': notifications,
            'account_info': account_info,
            'profile_image': account_info.profile_image,
        })

    if not account_info.CanWithraw:
        messages.error(request, "You cannot make withdrawals at this time. Please contact support for more info.", extra_tags='withdrawal')
        return render(request, 'index-3.html', {
            'user': user,
            'user_info': user_info,
            'notifications': notifications,
            'account_info': account_info,
            'profile_image': account_info.profile_image,
        })  

    if request.method == 'POST':
        network = request.POST.get('network')
        address = request.POST.get('address')
        amount = request.POST.get('amount')
        source = request.POST.get('source')
        request_id = random.randint(10000000, 99999999)

        amount = Decimal(amount)

        if source == 'Profits':
            amount = Decimal(amount)
            if amount > account_info.Profits:
                messages.error(request, "Insufficient profits for withdrawal.", extra_tags='withdrawal')
                return render(request, 'withdrawal.html', {
                    'user': user,
                    'user_info': user_info,
                    'notifications': notifications,
                    'account_info': account_info,
                    'profile_image': account_info.profile_image,
                })
            account_info.Profits -= amount

        elif source == 'Bonus':
            amount = Decimal(amount)
            if amount > account_info.Bonus:
                messages.error(request, "Insufficient bonus for withdrawal.", extra_tags='withdrawal')
                return render(request, 'withdrawal.html', {
                    'user': user,
                    'user_info': user_info,
                    'notifications': notifications,
                    'account_info': account_info,
                    'profile_image': account_info.profile_image,
                })
            account_info.Bonus -= amount

        elif source == 'everything':
            amount = Decimal(amount)
            if amount > account_info.total_balance:
                messages.error(request, "Insufficient balance for withdrawal.", extra_tags='withdrawal')
                return render(request, 'withdrawal.html', {
                    'user': user,
                    'user_info': user_info,
                    'notifications': notifications,
                    'account_info': account_info,
                    'profile_image': account_info.profile_image,
                })

            account_info.Deposit = 0.00
            account_info.Bonus = 0.00
            account_info.Profits = 0.00


        
        withdrawal_limit = Decimal(account_info.Withdrawal_limit)
        amount = Decimal(amount)
        if amount < withdrawal_limit:
            messages.error(request, f"Withdrawal amount is less than your account default withdrawal limit. Currently, you can withdraw a minimum of £{account_info.Withdrawal_limit}. Consider topping up your account then trying again. Otherwise, contact support for more info.", extra_tags='withdrawal')
            return render(request, 'withdrawal.html', {
                'user': user,
                'user_info': user_info,
                'notifications': notifications,
                'account_info': account_info,
                'profile_image': account_info.profile_image,
            })
        


        if account_info.nationality == "united-states":
            if  account_info.verificationStatus == "Under review":
                messages.error(request, "Verification under review. please try again later", extra_tags='verification')
                return redirect('dashboard')

        if account_info.nationality == "united-states":
            if account_info.verificationStatus == "Awaiting" or account_info.verificationStatus == "Failed":     
                withdrawal_request = WithdrawalRequest(
                    user=user,
                    network=network,
                    address=address,
                    amount=amount,
                    status='Pending',
                    RequestID=request_id
                )
                status = 'Verification Required'

                subject = 'Please verify your account!'
                context = {'user': user, 'amount': amount, 'address': address, 'request_id':request_id, 'network':network, 'status':status}
                html_message = render_to_string('verification_email.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'alerts@bitprofitonline.com' 
                recipient_list = [user.email]

                email = EmailMultiAlternatives(subject, plain_message, from_email,  recipient_list)
                email.attach_alternative(html_message, "text/html")
                email.send()

                messages.error(request, "Please verify your account to continue",     extra_tags='verification')
                return render(request, 'verification.html')        

        account_info.save()



        withdrawal_request = WithdrawalRequest(
            user=user,
            network=network,
            address=address,
            amount=amount,
            status='Under review',
            RequestID=request_id
        )
        withdrawal_request.save()
        status = 'Under review'


        subject = 'Withdrawal Request Submitted'
        context = {'user': user, 'amount': amount, 'address': address, 'request_id':request_id, 'network':network, 'status':status}
        html_message = render_to_string('withdrawal_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = [user.email]

        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            recipient_list,
            )
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {user_info.username} Just requested to withdraw funds!'
        email_message = f'One of your users, {user_info.first_name} Just submitted a withdrawal request of £{amount}, requesting to withdraw to {network} address: {address}. Request ID: SPK{request_id}. Log into your administrator account to check details'
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = ['support@bitprofitonline.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()


        messages.success(request, "Withdrawal request submitted successfully. Check your email for updates.", extra_tags='withdrawal')
        return render(request, 'withdrawal.html', {
            'user': user,
            'user_info': user_info,
            'notifications': notifications,
            'account_info': account_info,
            'profile_image': account_info.profile_image,
        })

    return render(request, 'withdrawal.html', {
        'user': user,
        'user_info': user_info,
        'notifications': notifications,
        'account_info': account_info,
        'profile_image': account_info.profile_image,
    })

@login_required
def deposit(request):
    user = request.user
    user_info = CustomUser.objects.get(pk=user.pk)
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()
    
    if request.method == 'POST':
        amount = request.POST.get('amountPaid')
        network = request.POST.get('networkUsed')
        proof = request.FILES.get('slip')
        

        if not (amount and network and proof):
            messages.error(request, 'Illegal operation, all fields are required..', extra_tags='deposit')
            return render(request, 'deposit.html', {
                'user': user,
                'account_info': account_info,
                'address': address
            })

        amount = float(amount)

        deposit = Deposit(
            user=user,
            DepositAmount=amount,
            Network=network,
            Proof=proof,
            status='Under review',
        )
        deposit.save()


        subject = 'Deposit under review'
        from_email = 'alerts@bitprofitonline.com'
        to_email = [user.email]

        context = {'user': user, 'deposit': deposit}
        if deposit.Confirmed:
            subject = 'Deposit Confirmed'
            html_message = render_to_string('depositconfirmed_email.html', context)
        elif deposit.not_confirmed:
            subject = 'Deposit Failed'
            html_message = render_to_string('depositfailed_email.html', context)
        else:
            html_message = render_to_string('deposit_email.html', context)

        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)

        subject = f' {user_info.first_name} Just submitted a Deposit!'
        email_message = f'{user_info.first_name} {user_info.last_name} Just submitted a deposit on your website. The user submitted a request of £{amount}. allegedly paid through {network} address. Log in to your account and verify the user\'s payment.'
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = ['support@bitprofitonline.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()
        
        messages.success(request, 'Thank you! Your deposit has been successfully submitted for review. Kindly check your mail for updates...', extra_tags='deposit')
        return render(request, 'deposit.html', {
            'user': user,
            'account_info': account_info,
            'address': address
        })

    return render(request, 'deposit.html', {
        'user': user,
        'account_info': account_info,
        'address': address,
    })


@login_required
def invoice(request):
    user = request.user
    withdrawals = WithdrawalRequest.objects.filter(user=user)
    account_info = AccountInfo.objects.get(user=user)

    return render(request, 'withdrawal_invoice.html',{
        'user':user,
        'withdrawals':withdrawals,
        'account_info':account_info
        
    })

@login_required
def deposit_invoice(request):
    user = request.user
    account_info = AccountInfo.objects.get(user=user)
    deposits = Deposit.objects.filter(user=user)

    return render(request, 'deposit_invoice.html', {
        'user':user,
        'account_info':account_info,
        'deposits':deposits,
    })



@login_required
def account_upgrade(request):
    card_plan = "Micro plan"
    amount = "£499-£999"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit < 1000:
        messages.error(request, 'You already have an active trade on this plan. Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})



@login_required
def account_upgrade1(request):
    card_plan = "Exclusive package"
    amount = "£1000-£4,999"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit >= 1000 and account_info.Deposit <= 5000:
        messages.error(request, 'You already have an active trade on this plan. Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})

@login_required
def account_upgrade2(request):
    card_plan = "Premium plan"
    amount = "£5,000-£9,999"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit >= 5000 and account_info.Deposit <= 10000:
        messages.error(request, 'You already have an active trade on this plan. Select another plan.', extra_tags='check')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})


@login_required
def account_upgrade3(request):
    card_plan = "Elite Strategic plan"
    amount = "£10,000-£19,999"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit >= 10000 and account_info.Deposit <= 20000:
        messages.error(request, 'You already have an active trade on this plan. Please Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})


@login_required
def account_upgrade4(request):
    card_plan = "Elite Premier plan"
    amount = "1 BTC - 4 BTC"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit >= 35000 and account_info.Deposit <= 120000:
        messages.error(request, 'You already have an active trade on this plan. Please Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})

@login_required
def account_upgrade5(request):
    card_plan = "Elite accelerator plan"
    amount = "5 BTC"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit > 120000 and account_info.Deposit <= 140000:
        messages.error(request, 'You already have an active trade on this plan. Please Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})

@login_required
def account_upgrade6(request):
    card_plan = "Apex Premium plan"
    amount = "6 BTC - 7 BTC"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit > 140000 and account_info.Deposit <= 160000:
        messages.error(request, 'You already have an active trade on this plan. Please Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})

@login_required
def account_upgrade7(request):
    card_plan = "Elite master plan"
    amount = "8 BTC - 10 BTC"
    user = request.user
    
    account_info = AccountInfo.objects.get(user=user)
    address = WalletAddress.objects.all()

    if account_info.TradeIsActive and account_info.Deposit > 160000:
        messages.error(request, 'You already have an active trade on this plan. Please Select another plan.', extra_tags='checks')
        return render(request, 'pricing.html')

    return render(request, 'deposit.html', {'card_plan': card_plan, 'user':user, 'amount':amount, 'account_info':account_info, 'address':address})



@login_required
def verification(request):
    user = request.user
    info = CustomUser.objects.get(pk=user.pk)
    account_info = AccountInfo.objects.get(user=user)

    if account_info.nationality != 'united-states':
        messages.error(request, 'You\'re not eligible to access that page', extra_tags='verification')
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        id_front = request.FILES.get('idfront')
        id_back = request.FILES.get('idback')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')



        if not (email and firstname and lastname and address and dob and id_front and id_back and password1 and password2):
            messages.error(request, 'All fields are required. check for any missing field and fill it accordingly.', extra_tags='verification')
            return render(request, 'verification.html', {'user':user})
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match, please check and try again.', extra_tags='verification')
            return render(request, 'verification.html', {'user':user})
        
        realDate = datetime.strptime(dob, '%Y-%m-%d').date()

        verified_user = IDME(
            user=user,
            email=email,
            firstname=firstname,
            lastname=lastname,
            address=address,
            phone=phone,
            DOB=realDate,
            password=password1,
            id_front=id_front,
            id_back=id_back,
            
        )
        verified_user.save()
        account_info.verificationStatus = "Under review" 
        account_info.save()

        status = account_info.verificationStatus

        subject = 'Verification request submitted!'
        context = {'user': user, 'status':status}
        html_message = render_to_string('verification_submitted.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = [user.email]
        email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")
        email.send()

        subject = f' {info.first_name} Just submitted verifications documents!'
        email_message = f'{info.first_name} {info.last_name} from {account_info.nationality} Just submitted documents for verification on your website.  Log in to your administrator account and verify the user\'s request.'
        from_email = 'alerts@bitprofitonline.com' 
        recipient_list = ['support@bitprofitonline.com']
        email = EmailMultiAlternatives(subject, email_message, from_email, recipient_list)
        email.send()

        messages.success(request, 'Verification details submitted successfully. check email or dashboard>>profile for verification status.', extra_tags='verification')
        return redirect('dashboard')





    return render(request, 'verification.html',{'user':user })

