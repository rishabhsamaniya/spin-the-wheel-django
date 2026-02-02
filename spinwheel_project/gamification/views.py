from django.shortcuts import render, redirect
import random
from .models import User, Category, Spin, Product, Address, Order


# Create your views here.

def mobile_input(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = random.randint(1000, 9999)

        request.session['otp'] = otp
        request.session['mobile'] = mobile

        print("OTP is ", otp)

        return redirect('verify_otp')
    return render(request, 'gamification/mobile.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        mobile = request.session.get('mobile')

        if str(session_otp) == entered_otp:
            user, created = User.objects.get_or_create(
                mobile_number = mobile
            )
            user.is_varified = True
            user.save()

            if Order.objects.filter(user=user).exists():
                return redirect('order_already_done')

            return redirect('welcome')
        
    return render(request, 'gamification/otp.html')

def order_already_done(request):
    return render(request, 'gamification/order_already_done.html')

def welcome(request):
    return render(request, 'gamification/welcome.html')


def spin_wheel(request):
    mobile = request.session.get('mobile')

    if not mobile:
        return redirect('mobile')
    
    user = User.objects.get(mobile_number = mobile)


    if Spin.objects.filter(user=user).exists():
        return redirect('already_spin')

    category = Category.objects.first()

    if request.method == 'POST':
        user_mobile = request.session.get('mobile')
        user = User.objects.get(mobile_number=user_mobile)

        Spin.objects.create(
            user=user,
            category=category,
            is_winner = True
        )

        return redirect('products') 
    
    return render(request, 'gamification/spin.html', {
        'category': category
    })

def already_spin(request):
    return render(request, 'gamification/already_spin.html')

def products(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'gamification/products.html', {
        'products': products
    })

def select_product(request, product_id):
    request.session['selected_product'] = product_id
    return redirect('address')


def address(request):
    if request.method == 'POST':
        print("POST DATA:", request.POST)
        full_name = request.POST.get('full_name')
        address_line = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        mobile = request.session.get('mobile')
        product_id = request.session.get('selected_product')

        user = User.objects.get(mobile_number=mobile)
        product = Product.objects.get(id=product_id)

        address = Address.objects.create(
            user=user,
            full_name=full_name,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode
        )

        Order.objects.create(
            user=user,
            product=product,
            address=address,
            is_confirmed=True
        )

        print("📦 Order placed successfully!")

        return redirect('order_success')
    
    return render(request, 'gamification/address.html')


def order_success(request):
    return render(request, 'gamification/order_success.html')
