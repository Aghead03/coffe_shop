from django.shortcuts import render , redirect
from .models import UserProfile
import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from products.models import Product

# Create your views here.
def sign_in(request):
    if request.method == 'POST' and 'btnlogin' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(
            username = username,
            password = password)
        if user is not None :
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request , user) 
        else:
            messages.error(request, 'username or password invalid ')    
        
        return redirect('sign_in')
    else:
        return render(request,'accounts/sign_in.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')    


def sign_up(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None
        zip = None
        email = None
        username = None
        password = None
        terms = None
        is_added = None
        
        if 'fname' in request.POST: fname = request.POST['fname']
        else:messages.error(request , 'error in first name')
        if 'lname' in request.POST: lname = request.POST['lname']
        else:messages.error(request , 'error in last name')
        if 'address' in request.POST: address = request.POST['address']
        else:messages.error(request , 'error in address')
        if 'address2' in request.POST: address2= request.POST['address2']
        else:messages.error(request , 'error in address2')
        if 'city' in request.POST: city = request.POST['city']
        else:messages.error(request , 'error in city')
        if 'state' in request.POST: state = request.POST['state']
        else:messages.error(request , 'error in state')
        if 'zip' in request.POST: zip = request.POST['zip']
        else:messages.error(request , 'error in zip')
        if 'email' in request.POST: email= request.POST['email']
        else:messages.error(request , 'error in email')
        if 'username' in request.POST: username = request.POST['username']
        else:messages.error(request , 'error in username')
        if 'password' in request.POST: password = request.POST['password']
        else:messages.error(request , 'error in password')
        if 'terms' in request.POST: terms = request.POST['terms']
        #check the values
        
        if fname and lname and address and address2 and city and state and zip and email and username and password:
            if terms == 'on':
                #check if user taken
                if User.objects.filter(username=username).exists():
                    messages.error(request,'this user is taken')
                else:
                    #chek if email taken
                    if User.objects.filter(email = email).exists():
                        messages.error(request,'this email is token')
                    else:
                        patt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if re.match(patt,email):
                            #add user 
                            user = User.objects.create_user(
                                first_name = fname ,
                                last_name = lname,
                                email = email ,
                                username = username,
                                password = password)
                            user.save()
                            #add user profile 
                            userprofile = UserProfile(
                                user = user ,
                                address = address,
                                address2 = address2 ,
                                city = city ,
                                state = state ,
                                zip_number = zip)
                            userprofile.save()
                            #clear field 
                            fname = ''
                            lname = ''
                            address = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None
                            ##succes messages
                            messages.success(request , 'signin succesed')
                            is_added = True
                        else:
                            messages.error(request,'invaild email')    
            else:
                messages.error(request,'you must agree to the terms ' )    
        else:
            messages.error(request, 'check empity field')
        
        return render(request,'accounts/sign_up.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'city':city,
            'state':state,
            'zip':zip,
            'email':email,
            'username':username,
            'password':password,
            'is_added':is_added,
        })
    else:
        return render(request,'accounts/sign_up.html')

def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['username'] and request.POST['password']:
                request.user.first_name=request.POST['fname']
                request.user.last_name=request.POST['lname']
                userprofile.address=request.POST['address']
                userprofile.address2=request.POST['address2']
                userprofile.city=request.POST['city']
                userprofile.state=request.POST['state']
                userprofile.zip_number=request.POST['zip']
                #request.user.email=request.POST['email']
                #request.user.username=request.POST['username']
                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                request.user.save()
                userprofile.save() 
                auth.login(request,request.user)
                messages.success(request, 'your data has been saved')
            else:
                messages.error(request,'check you value')
        return redirect('profile')
    else:
        if request.user is not None :
            context = None
            if not request.user.is_anonymous:
                userprofile =UserProfile.objects.get(user=request.user)
                context = {
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip':userprofile.zip_number,
                    'email':request.user.email,
                    'username':request.user.username,
                    'password':request.user.password,
                }
            return render(request,'accounts/profile.html', context)
        else:   
            return redirect('profile')
        
def product_favorites(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user , product_favorites=pro_fav).exists():
            messages.info(request,'the product already favorites')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request,'product has been favorites')
    else:
        messages.error(request,"you must be loged")
    return redirect('/products/' + str(pro_id))    
    
def show_product_favorites(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user_info = UserProfile.objects.get(user = request.user)
        pro = user_info.product_favorites.all()
        context ={
            'products' :pro
            }
    return render(request,'products/products.html',context)