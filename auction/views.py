from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
import datetime
from django.contrib import messages


def Home(request):
    data = 0
    error = ""
    user=""
    try:
        user = User.objects.get(username=request.user.username)
    except:
        pass
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
            return redirect('profile1')
    except:
        pass
    try:
        data = Auction_User.objects.get(user=user)
        return redirect('trainer_home')
    except:
        pass
    d = {'error':error,'data':data}
    return render(request, 'carousel.html',d)


def new():
    status = Status.objects.get(status="pending")
    new_pro = Product.objects.filter(status=status)
    return new_pro


def About(request):
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Bidder.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat"
            else:
                login(request, user)
                error = "pat1"
        else:
            error="not"

    d = {'error': error}
    return render(request, 'login.html', d)


def Login_Admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "yes"
        else:
            error = "not"

    d = {'error': error}
    return render(request, 'loginadmin.html', d)

def Signup_User(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['add']
        d2 = request.POST['dob']
        reg = request.POST['reg']
        i = request.FILES['image']
        if len(con) != 10 or not con.isdigit():
            messages.error(request, "Contact number must be exactly 10 digits.")
            return redirect('signup')
        if len(u) < 8 or len(p) < 8:
            messages.error(request,"Length of username and password must be atlest 8 characters ")
            return redirect('signup')
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        mem = Member_fee.objects.get(fee="Unpaid")
        if reg == "Bidder":
            sign = Bidder.objects.create(membership=mem,user=user,contact=con,address=add,dob=d2,image=i)
        else:
            sign = Auction_User.objects.create(membership=mem,user=user,contact=con,address=add,dob=d2,image=i)
        error = True
    d = {'error':error}
    return render(request,'signup.html',d)

def Admin_Home(request):
    if not request.user.is_staff:
        return redirect('login_user')
    
    new2 = new()  # Ensure this function or object is defined elsewhere
    count = 1 if new2 else 0

    # Get all counts
    all_p = Product.objects.count()
    all_b = Bidder.objects.count()
    all_s = Auction_User.objects.count()

    # Get current user and profile
    data1 = request.user
    data = None
    error = ""

    try:
        data = Bidder.objects.get(user=data1)
    except Bidder.DoesNotExist:
        try:
            data = Auction_User.objects.get(user=data1)
        except Auction_User.DoesNotExist:
            error = "User profile not found."

    context = {
        'data': data,
        'count': count,
        'new2': new2,
        'all_p': all_p,
        'all_b': all_b,
        'all_s': all_s,
        'error': error
    }
    return render(request, 'admin_home.html', context)

def Bidder_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user=User.objects.get(username=request.user.username)
    error=""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    d = {'error':error,'data':data}
    return render(request,'dashboard.html',d)

def Profile1(request):
    new2 = new()
    count = 0
    if new2:
        count += 1
    user = request.user
    error = ""
    data = None
    try:
        data = Bidder.objects.get(user=user)
        error = "pat"
    except Bidder.DoesNotExist:
        try:
            data = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            pass  # Handle the case where neither Bidder nor Auction_User exists, if necessary

    try:
        pro = Bidder.objects.get(user=user)
        u = "member"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user)
            u = "trainer"
        except Auction_User.DoesNotExist:
            pro = None
            u = ""

    context = {'pro': pro, 'error': error, 'data': data, 'count': count, 'new2': new2}
    return render(request, 'profile1.html', context)

def Auction_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    sign = 0
    user = User.objects.get(username=request.user.username)
    error=""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = Auction_User.objects.get(user=user)
    if sign.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    d = {'error': error,'data':sign}
    return render(request,'dashboard.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user = request.user
    error = ""
    data = None
    try:
        data = Bidder.objects.get(user=user)
        error = "pat"
    except Bidder.DoesNotExist:
        try:
            data = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            pass  # Handle the case where neither Bidder nor Auction_User exists, if necessary

    try:
        pro = Bidder.objects.get(user=user)
        u = "member"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user)
            u = "trainer"
        except Auction_User.DoesNotExist:
            pro = None
            u = ""

    context = {'pro': pro, 'error': error, 'data': data, 'count': count, 'new2': new2}
    return render(request, 'profile1.html', context)

def Logout(request):
    logout(request)
    return redirect('home')

def Change_Password(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'count':count,'new2':new2}
    return render(request,'change_password.html',d)

def Change_Password1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        sign = Bidder.objects.get(user=user)
        if sign:
            error = "pat"
    except:
        sign = Auction_User.objects.get(user=user)
    if sign.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign,'count':count,'new2':new2}
    return render(request,'change_password1.html',d)

def Edit_Profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=""
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = Auction_User.objects.get(user=user1)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user1.first_name = f
        user1.last_name = l
        user1.email = e
        user1.save()
        pro.save()
        terror = True
    d = {'terror':terror,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'edit_profile.html',d)

def Edit_Profile1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro=None
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except:
        pro = Auction_User.objects.get(user=user1)
    terror = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image=i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact=con
        user1.first_name = f
        user1.last_name = l
        user1.email = e
        user1.save()
        pro.save()
        terror = True
    d = {'terror':terror,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'edit_profile1.html',d)


def Add_Category(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        error = "Bidder profile found."
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    if request.method == 'POST':
        n = request.POST['cat']
        Category.objects.create(name=n)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'add_category.html',d)

def Edit_Category(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    category =Category.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST.get('cat', '')
        category.name = n
        category.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'edit_category.html',d)

def delete_category(request,pid):
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_category')

def view_category(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    cat = Category.objects.all()
    d= {'error': error,'pro': pro,'cat': cat,'count': count,'new2': new2}
    return render(request, 'view_category.html',d)

def view_feedback(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    pro = ""
    try:
        pro = Bidder.objects.get(user=user1)
        error = "pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
        except Auction_User.DoesNotExist:
            error = "User profile not found."
    cat = Send_Feedback.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request,'view_feedback.html',d)

def Add_SubCategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    cat = Category.objects.all()
    if request.method == 'POST':
        n = request.POST.get('cat','')
        s = request.POST['scat']
        cat1 = Category.objects.get(name=n)
        Sub_Category.objects.create(name=s,category=cat1)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request, 'add_sub_category.html',d)



def Edit_SubCategory(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    cat = Category.objects.all()
    subcat = Sub_Category.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST.get('cat', '')
        s = request.POST.get('scat', '')
        subcat.category = Category.objects.get(name=n)
        subcat.name = s
        subcat.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'subcat':subcat,'count':count,'new2':new2}
    return render(request, 'edit_subcategory.html',d)

def delete_subcategory(request,pid):
    cat = Sub_Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_subcategory')

def delete_feedback(request,pid):
    cat = Send_Feedback.objects.get(id=pid)
    cat.delete()
    return redirect('view_feedback')


def view_subcategory(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    cat = Sub_Category.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'cat':cat,'count':count,'new2':new2}
    return render(request,'view_subcategory.html',d)


def Add_Session_date(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    if request.method == 'POST':
        d = request.POST['date']
        cat1 = Session_date.objects.create(date=d)
        error = True
    d = {'error':error,'pro':pro,'data':pro,'count':count,'new2':new2}
    return render(request, 'Add_session_date.html',d)


def Edit_Session_date(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    ses = Session_date.objects.get(id=pid)
    if request.method == 'POST':
        n = request.POST['date']
        ses.date = n
        ses.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'ses':ses,'count':count,'new2':new2}
    return render(request, 'edit_session_date.html',d)

def delete_session_date(request,pid):
    cat = Session_date.objects.get(id=pid)
    cat.delete()
    return redirect('view_session_date')


def view_session_date(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    cat = Session_date.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'date1':cat,'count':count,'new2':new2}
    return render(request,'view_session_date.html',d)

def Add_Session_time(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            error = "User profile not found."
    error = False
    sed=Session_date.objects.all()
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        session_dates = Session_date.objects.filter(date=d)
        if session_dates.exists():
            d1 = session_dates.first()  # Using the first instance if there are multiple
            Session_Time.objects.create(date=d1, time=t)
            error = True
    context = {'error': error,'count': count,'new2': new2,'sed':sed}
    return render(request, 'add_session_time.html', context)

def Edit_Session_time(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    sed = Session_date.objects.all()
    sett = Session_Time.objects.get(id=pid)
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        sedd = Session_date.objects.get(id=d)
        sett.date = sedd
        sett.time = t
        sett.save()
        error = True
    d = {'error':error,'pro':pro,'data':pro,'sed':sed,'sett':sett,'count':count,'new2':new2}
    return render(request, 'edit_session_time.html',d)

def delete_session_time(request,pid):
    cat = Session_Time.objects.get(id=pid)
    cat.delete()
    return redirect('view_session_time')


def view_session_time(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    cat = Session_Time.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'time1':cat,'count':count,'new2':new2}
    return render(request,'view_session_time.html',d)

def New_product(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    st = Status.objects.get(status = "pending")
    prod = Aucted_Product.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod,'count':count,'new2':new2}
    return render(request, 'new_product.html',d)

def All_product2(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    st = Status.objects.get(status = "pending")
    prod = Aucted_Product.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod,'count':count,'new2':new2}
    return render(request, 'all_product2.html',d)


def Bidder_User(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    st = Status.objects.get(status = "pending")
    prod = Bidder.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod}
    return render(request,'new_user.html',d)

def Seller_User(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    st = Status.objects.get(status = "pending")
    prod = Auction_User.objects.all()
    d = {'error':error,'pro':pro,'data':pro,'prod':prod}
    return render(request, 'auction_user.html',d)

def result(request):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    pro1 = Participant.objects.all()
    d = {'error':error,'pro':pro1,'data':pro,'count':count,'new2':new2}
    return render(request, 'result.html',d)

def Winner(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    error = False
    pro1 = Participant.objects.get(id=pid)
    d = {'error':error,'pro':pro1,'data':pro,'count':count,'new2':new2}
    return render(request, 'winner_announced.html',d)

def Winner2(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)

    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro2 = Product.objects.get(id=pid)
    au = Aucted_Product.objects.get(product=pro2)
    re = Result.objects.get(result="Winner")
    pro1 = Participant.objects.get(aucted_product=au, result=re)
    d = {'pro': pro1, 'error': error}
    return render(request, 'winner2.html', d)

def Winner1(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro2 = Product.objects.get(id=pid)
    au = Aucted_Product.objects.get(product=pro2)
    re = Result.objects.get(result="Winner")
    pro1 = ""
    try:
        pro1 = Participant.objects.get(aucted_product=au, result=re)
    except:
        pass
    terror = False
    if not pro1:
        terror=True
    d = {'pro':pro1,'error':error,'terror':terror}
    return render(request,'winner2.html',d)

def Feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = request.user
    error = ""
    data = None
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except Bidder.DoesNotExist:
        try:
            data = Auction_User.objects.get(user=user)
        except Auction_User.DoesNotExist:
            pass 
    if data and data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    date1 = datetime.date.today()
    pro = None
    try:
        pro = Bidder.objects.filter(user=user).first()
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.filter(user=user).first()
        except Auction_User.DoesNotExist:
            pro = None
    terror= False
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        if user:
            try:
                pro = Bidder.objects.filter(user=user).first()
            except Bidder.DoesNotExist:
                try:
                    pro = Auction_User.objects.filter(user=user).first()
                except Auction_User.DoesNotExist:
                    pro = None
            if pro:
                Send_Feedback.objects.create(profile=user, date=d, message1=m)
                terror = True
    context = {'pro': pro, 'date1': date1, 'terror': terror, 'error': error}
    return render(request, 'feedback.html', context)

def Add_Product(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    date1 = datetime.date.today()
    sed = Session_date.objects.all()
    sett = Session_Time.objects.all()
    cat = Category.objects.all()
    scat = Sub_Category.objects.all()
    sell = Auction_User.objects.get(user=user)
    terror = False
    if request.method == "POST":
        c = request.POST['cat']
        s = request.POST['scat']
        p = request.POST['p_name']
        pr = request.POST['price']
        i = request.FILES['image']
        sett1 = request.POST['time']
        sed1 = request.POST['date']
        sub = Sub_Category.objects.get(id=s)
        ses = Session_Time.objects.get(id=sett1)
        sta = Status.objects.get(status="pending")
        pro1=Product.objects.create(status=sta,session=ses,category=sub,name=p, min_price=pr, images=i)
        auc=Aucted_Product.objects.create(product=pro1,user=sell)
        terror = True
    d = {'sed': sed,'sett':sett,'cat': cat,'scat':scat,'date1': date1,'terror':terror,'error':error}
    return render(request, 'add_product.html', d)

def load_courses(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    programming_id = request.GET.get('programming')
    courses = Sub_Category.objects.filter(category_id=programming_id).order_by('name')
    return render(request, 'courses_dropdown_list_options.html', {'courses': courses})

def load_courses1(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    programming_id = request.GET.get('programming')
    courses = Session_Time.objects.filter(date_id=programming_id)
    return render(request, 'courses_dropdown_list_options1.html', {'courses': courses})

def view_auction(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    terror = False
    if request.method == "POST":
        pro1 = Product.objects.get(id=pid)
        auc = Aucted_Product.objects.get(product=pro1)
        Participant.objects.create(user=data,aucted_product=auc)
        terror = True
    pid = 0
    d1 = Participant.objects.filter(user=data)
    li = []
    for i in d1:
        li.append(i.aucted_product.product.id)

    status = Status.objects.get(status="Accept")
    pro = Product.objects.filter(status=status)
    pro1 = Product.objects.all()
    message1=""
    if not pro:
        message1 = " No Any Bidding Product "
    for i in pro:
        if i.id in li:
            i.temp = 1
            i.save()
        else:
            i.temp = 0
            i.save()
    for i in pro:
        a = i.session.date.date
        li = a.split('-')
        total_time = (int(li[0]) * 365) + (int(li[1]) * 30) + (int(li[2]))
        d1 = datetime.date.today()
        d2 = datetime.datetime.now()
        c_time = d2.strftime("%H:%M")
        y = d1.year
        m = d1.month
        d = d1.day
        now_total = (int(y) * 365) + (int(m) * 30) + (int(d))
        part = Participant.objects.all()
        for l in part:
            z=l.aucted_product.product.session.date.date
            li2 = z.split('-')
            total_time_part = (int(li2[0]) * 365) + (int(li2[1]) * 30) + (int(li2[2]))
            if total_time_part < now_total:
                if l.result is None:
                    r = Result.objects.get(result="notproper")
                    l.result = r
                    l.save()
        li2 = i.session.time.split(':')
        li3 = c_time.split(':')
        time1 = (int(li2[0]) * 60) + int(li2[1])
        time2 = (int(li3[0]) * 60) + int(li3[1])
        time3 = time1 + 60
        if total_time == now_total:
            if time1 == time2:
                i.temp = 2
                i.save()
            elif time2 < time3 and time2>time1:
                i.temp = 2
                i.save()
            elif time2 > time3:
                i.temp = 3
                i.save()
        elif total_time < now_total:

            i.temp = 3
            i.save()
    d = {'pro':pro1,'error':error,'terror':terror,'message1':message1}
    return render(request,'view_auction.html',d)

def All_product(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)

    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro = Aucted_Product.objects.filter(user=data)
    d = {'pro':pro,'error':error}
    return render(request,'All_prodcut.html',d)

def product_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro = Product.objects.get(id=pid)
    end = pro.session.time.split(':')
    end1=""
    if end[0]== "23":
        end1="00"
    else:
        end1 = str(int(end[0])+1)
    end2 = end1+":"+end[1]
    pro1 = Aucted_Product.objects.get(product=pro)
    d = {'pro':pro,'pro1':pro1,'error':error,'end2':end2}
    return render(request,'product_detail.html',d)

def product_detail2(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    pro = Product.objects.get(id=pid)
    end = pro.session.time.split(':')
    end1 = ""
    if end[0] == "23":
        end1 = "00"
    else:
        end1 = str(int(end[0]) + 1)
    end2 = end1 + ":" + end[1]
    pro1 = Aucted_Product.objects.get(product=pro)
    d = {'pro':pro,'pro1':pro1,'error':error,'end2':end2}
    return render(request,'product_detail2.html',d)

def Bidding_Status(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro = Participant.objects.filter(user=data)
    d = {'pro':pro,'error':error}
    return render(request,'bidding_status.html',d)

def Bidding_Status2(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    pro1 =  Aucted_Product.objects.filter(user=data)
    d = {'pro':pro1,'error':error}
    return render(request,'bidding_status2.html',d)

def Participated_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')
    auc = Aucted_Product.objects.get(id=pid)
    pro1 =  Participant.objects.filter(aucted_product=auc)
    message1=""
    if not pro1:
        message1 = "No Bidder"
    d = {'part':pro1,'error':error,'message1':message1}
    return render(request,'particpated_user.html',d)

def Payment_mode(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')

    d = {'error':error,'pid':pid}
    return render(request,'payment_mode.html',d)

def Member_Payment_mode(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)

    d = {'error':error,'data':data}
    return render(request,'member_Payment.html',d)

def Google_pay(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    total = Participant.objects.get(id=pid)
    terror=False
    if request.method=="POST":
        pay = Payment.objects.get(pay="paid")
        total.payment=pay
        total.save()
        terror=True
    d = {'error':error,'total':total,'terror':terror}
    return render(request,'google_pay.html',d)

def Member_Google_pay(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    terror=False
    if request.method=="POST":
        mem = Member_fee.objects.get(fee="Paid")
        data.membership = mem
        data.save()
        terror=True
    d = {'error':error,'terror':terror}
    return render(request,'member_google_pay.html',d)

def Credit_Card(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    terror = False
    total = Participant.objects.get(id=pid)
    if request.method=="POST":
        pay = Payment.objects.get(pay="paid")
        total.payment=pay
        total.save()
        terror =True
    d = {'error':error,'total':total,'terror':terror}
    return render(request,'payment2.html',d)

def Member_Credit_Card(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    terror = False
    if request.method=="POST":
        mem = Member_fee.objects.get(fee="Paid")
        data.membership = mem
        data.save()
        terror =True
    d = {'error':error,'terror':terror}
    return render(request,'member_payment2.html',d)
def view_popup(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error=True
    d = {'error':error}
    return render(request,'view_popup.html',d)

def Start_Auction(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    data = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    alt=""
    try:
        data = Bidder.objects.get(user=user)
        if data:
            error = "pat"
    except:
        data = Auction_User.objects.get(user=user)
    if data.membership.fee == "Unpaid":
        return redirect('Member_Payment_mode')

    pro4 = Product.objects.get(id=pid)
    end = pro4.session.time.split(':')
    end1 = ""
    if end[0] == "23":
        end1 = "00"
    else:
        end1 = str(int(end[0]) + 1)
    end2 = end1 + ":" + end[1]
    c = Aucted_Product.objects.get(product=pro4)
    pro1=""
    try:
        pro1 = Participant.objects.get(user=data, aucted_product=c)
    except:
        return redirect('view_popup')
    pro1 = Participant.objects.get(user=data, aucted_product=c)
    pro2 = Participant.objects.filter(aucted_product=c).order_by('-new_price')
    if request.method == "POST":
        p = request.POST["price"]
        current_highest_bid = float(pro2[0].new_price) if pro2 and pro2[0].new_price is not None else 0
        min_price = float(pro4.min_price)
        try:
            bid_price = float(p)
        except ValueError:
                messages.error(request, "Invalid bid price")
                return redirect('start_auction', pid=pid)
        else:
            if bid_price > current_highest_bid and bid_price >= min_price:
                pro1.new_price = bid_price
                pro1.save()
            else:
                    messages.error(request, "Bid price must be greater than the current highest bid and the minimum price")
                    return redirect('start_auction', pid=pid)
        return redirect('start_auction', pid=pid)
    a = pro1.aucted_product.product.session.date.date
    li = a.split('-')
    total_time = (int(li[0]) * 365) + (int(li[1]) * 30) + (int(li[2]))
    d1 = datetime.date.today()
    d2 = datetime.datetime.now()
    c_time = d2.strftime("%H:%M")
    y = d1.year
    m = d1.month
    d = d1.day
    now_total = (int(y) * 365) + (int(m) * 30) + (int(d))
    li2 = pro1.aucted_product.product.session.time.split(':')
    li3 = c_time.split(':')
    time1 = (int(li2[0]) * 60) + int(li2[1])
    time2 = (int(li3[0]) * 60) + int(li3[1])
    time3 = time1 + 60
    terror = ""
    if total_time == now_total:
        if time1 == time2 or time2 < time3:
            pro1.aucted_product.product.temp = 2
            pro1.aucted_product.product.save()
        elif time2 > time3:
            pro1.aucted_product.product.temp = 3
            pro1.aucted_product.product.save()
            terror = "expire"
    elif total_time < now_total:
        pro1.aucted_product.product.temp = 3
        pro1.aucted_product.product.save()
        terror = "expire"
    win = Participant.objects.filter(aucted_product=c).order_by('-new_price')
    list1 = []
    for i in win:
        list1.append(i.id)
    win1 = Participant.objects.get(id=list1[0])
    if pro1.aucted_product.product.temp == 3:
        pro1.aucted_product.winner = win1.user.user.username
        pro1.aucted_product.save()
        for i in pro2:
            if i.user.user.username == pro1.aucted_product.winner:
                res = Result.objects.get(result="Winner")
                stat1 = Status.objects.get(status="Done")
                pay2 = Payment.objects.get(pay="pending")
                i.payment = pay2
                i.result = res
                i.aucted_product.product.status = stat1
                i.aucted_product.product.save()
                i.save()
            else:
                res1 = Result.objects.get(result="Defeat")
                pay1 = Payment.objects.get(pay="reject")
                i.payment = pay1
                i.result = res1
                i.save()
    d = {'pro':pro1,'pro2':pro2,'end2':end2,'error':error,'terror':terror,'alt':alt}
    return render(request,'start_auction.html',d)

def Change_status(request,pid):
    if not request.user.is_staff:
        return redirect('login_user')
    new2 = new()
    count = 0
    if new2:
        count += 1
    user1 = User.objects.get(id=request.user.id)
    try:
        pro = Bidder.objects.get(user=user1)
        if pro:
            error="pat"
    except Bidder.DoesNotExist:
        try:
            pro = Auction_User.objects.get(user=user1)
            error = "Auction User profile found."
        except Auction_User.DoesNotExist:
            pro = None
            error = "User profile not found."
    terror = False
    pro1 = Product.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        terror=True
    d = {'pro':pro1,'error':error,'terror':terror,'count':count,'new2':new2}
    return render(request,'status.html',d)


def winner_announced(request):
    return redirect('result')

# from django.core.cache import cache
# cache.clear()