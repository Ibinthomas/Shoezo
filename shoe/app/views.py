from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta


# Create your views here.

def e_shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=uname  #Create Session
                return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid Username or Password")
            return redirect(e_shop_login)
    else:
        return render(req,'login.html')
    
# -------------------------admin-------------

def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'products':data})
    else:
        return redirect(e_shop_login)
    
def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            brand=req.POST['brand']
            name=req.POST['name']
            dis=req.POST['dis']
            price=req.POST['price']
            off_price=req.POST['offer_price']
            stock=req.POST['stock']
            file=req.FILES['img']
            data=Product.objects.create(pid=pid,brand=brand,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock,img=file,)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(e_shop_login)
    
def e_shop_logout(req):
    logout(req)
    req.session.flush() #Delete session
    return redirect(e_shop_login)

def edit_product(req,pid):
    if req.method=='POST':
        p_id=req.POST['pid']
        brand=req.POST['brand']
        name=req.POST['name']
        dis=req.POST['dis']
        price=req.POST['price']
        off_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES.get('img')
        if file:
            Product.objects.filter(pk=pid).update(pid=p_id,brand=brand,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()
        else:
            Product.objects.filter(pk=pid).update(pid=p_id,brand=brand,name=name,
                                        dis=dis,price=price,
                                        offer_price=off_price,
                                        stock=stock)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit.html',{'data':data})
    
def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/view_bookings.html',{'buy':buy})

# ---------------------------user------------------

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        # send_mail('Eshop Registration', 'EShop account created sucssfully', settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=uname,email=email,
                                        username=email,password=pswd)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(register)
        return redirect(e_shop_login)
    else:
        return render(req,'user/register.html')
    

def about(req):
    return render(req,'user/about.html')
    
def contact(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        phone = req.POST['phone']
        message = req.POST['message']

        # Debug print statements for confirmation
        print(name, email, phone,message)

        try:
            # Save data to the database
            data = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            data.save()
            return render(req, 'user/contact.html')
        except Exception as e:
            return render(req,'user/contact.html')
    
    return render(req,'user/contact.html')

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        adidas = Product.objects.filter(brand='Adidas')
        nike=Product.objects.filter(brand='Nike')
        puma=Product.objects.filter(brand='Puma')
        newbalance=Product.objects.filter(brand='Newbalance')
        

        return render(req,'user/home.html',{'products':data,'adidas': adidas,'nike':nike,'puma':puma,'newbalance': newbalance,})
    else:
        return redirect(e_shop_login)
    
    
def view_product(req,pid):
    if 'user' in req.session:
        data=Product.objects.get(pk=pid)
        return render(req,'user/view_product.html',{'product':data})
    else:
        return render(req,'user/home.html')
    
def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    total_price = sum(item.product.offer_price * item.qty for item in data) 
    return render(req,'user/cart.html',{'cart':data , 'total_price': total_price})

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)

def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def bookings(req):
    user = User.objects.get(username=req.session['user'])
    buy = Buy.objects.filter(user=user).order_by('-id')  # Simplified ordering
    return render(req, 'user/bookings.html', {'bookings': buy})

def cancel_order(req, pid):
    if 'user' in req.session:
        try:
            data = Buy.objects.get(pk=pid)
            # Check if the order is within the 2-day cancellation period
            if now() - data.created_at <= timedelta(days=2):
                data.delete()
                return redirect(bookings)
            else:
                # Provide feedback that the order cannot be canceled
                return render(req, 'user/error.html', {'error': 'Cannot cancel order after 2 days.'})
        except Buy.DoesNotExist:
            return redirect(bookings)  # Handle case if the order doesn't exist
    else:
        return redirect(user_home)