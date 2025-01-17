from django.shortcuts import render
from .models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')    

def product(request):
    return render(request,'product.html')        

def about(request):
    return render(request,'about.html')            
from django.shortcuts import render
from .models import User  # Ensure you have imported the User model

def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email Already Registered'
            return render(request, 'login.html', {"msg": msg})
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    profile_picture=request.FILES['profile_picture'],
                )
                msg = 'User Registered Successfully'
                return render(request, 'login.html', {"msg": msg})
            else:
                msg = 'Password and Confirm Password Do Not Match'
                return render(request, 'signup.html', {"msg": msg})
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                request.session['profile_picture'] = user.profile_picture.url
                return render(request, 'index.html')
            else:
                msg = 'Incorrect Password'
                return render(request, 'login.html',{"msg": msg})
        except User.DoesNotExist:
            msg = 'Email Not Registered'
            return render(request, 'login.html',{"msg": msg})
    else:
        return render(request, 'login.html')
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
        msg='User Logged Out Successfully'
        return render(request, 'login.html',{"msg": msg}) 
    except:
        msg='User Logged Out Successfully'
        return render(request, 'login.html',{"msg": msg}) 
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        request.session['profile_picture']=user.profile_picture.url
        msg='profile updated Successfully'       
        return render(request,'profile.html',{"user":user},{"msg": msg})
    else:
         return render(request,'profile.html',{"user":user})   

