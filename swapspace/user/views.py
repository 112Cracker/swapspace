from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse

from user.models import UserProfile, UserLocation, EmailRecord
from user.forms import UserProfileForm, UserRegisterForm, UserLoginForm, \
                       UserForgetPwdForm, UserResetPwdForm, UserAddressForm
from shoppingCart.models import ShoppingCart
from exchange.models import ExchangeItem, Category
from trade.models import SellItem
from utils.sendEmail import sendEmail
from exchange.views import calcRates

import json, re
# class CustomModelBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None):
#         print("Customize authenticate.")
#         try:
#             # user could login via either username or email
#             user = User.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None


# Create your views here.
# user login the website: url 'login'
def search_action(request, keywords):
    print("Enter user/search_action")
    words = re.findall(r"[\w']+", keywords)
    print(keywords)

    res_items = set()
    for w in words:
        items = ExchangeItem.objects.filter(description__icontains=w)
        for i in items:
            res_items.add(i)

    res_items = serializers.serialize('json', res_items)
    data = {"items": res_items}
    return HttpResponse(json.dumps(data), content_type='application/json')


def login_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'login.html', context)

    form = UserLoginForm(request.POST)
    context["loginForm"] = form

    # check login form validility
    if not form.is_valid():
        print("User Login Form is invalid ...")
        return render(request, 'login.html', context)

    username, password = form.cleaned_data["username"], form.cleaned_data["password"]
    print("{0}: {1}".format(username, password))
    user = authenticate(username=username, password=password)

    if user is None:
        print("User authentication failed ...")
        context["msg"] = "username or password does not exist."
        return render(request, 'login.html', context)

    print("User authentication success!")
    userProfile = user.myprofile
    # check activation
    if not userProfile.activated:
        print("User has not been activated")
        context["msg"] = "User has not been activated."
        return render(request, 'login.html', context)
    # check login information
    if not user:
        print("User logged in failed.")
        context["msg"] = "username and password do not match or exist."
        return render(request, 'login.html', context)
    

    login(request, user)
    print("User logged in successfully.")
    return redirect('/')


# user log out the website: url 'logout'
@login_required
def logout_action(request):
    logout(request)
    print("User log out.")
    return redirect('/')


# user register the website: url 'register'
def register_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'register.html')

    form = UserRegisterForm(request.POST)
    context["registerForm"] = form
    if not form.is_valid():
        print("User Registration Form is invalid ...")
        return render(request, 'register.html', context)

    print("User Registration Form is valid.")
    username, email = form.cleaned_data['username'], form.cleaned_data['email']
    password = form.cleaned_data['password1']
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    user.save()
    profile = UserProfile(user=user, good=0, fair=0, bad=0)
    profile.save()
    cart = ShoppingCart(user=user)
    cart.save()
    sendEmail(email) # send registration email

    print("New user is created but not activated.")
    return redirect('/login')


# user edit the profile: url 'edit-profile'
@login_required
def edit_profile_action(request):
    print("Enter user/edit_profile_action")
    user = request.user
    profile = UserProfile.objects.get(user=user)
    # GET: view user profile
    if request.method == "GET":
        form = UserProfileForm(instance=profile)
        context = {
            'profile': profile,
            'form': form,
            'user': user
        }
        return render(request, "edit-profile.html", context)

    # POST: update user profile
    edit_profile = UserProfile.objects.select_for_update().get(user=user)
    if request.FILES:
        print("User upload a new picture.")
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
    else:
        print("User upload nothing.")
        form = UserProfileForm(request.POST, instance=profile)
    if not form.is_valid():
        context = {'profile': profile, 'form': form}
        return render(request, 'edit-profile.html', context)

    edit_profile.update_time = timezone.now()
    form.save()
    profile = UserProfile.objects.get(user=user)
    context = {
        "user": user,
        "profile": profile
    }
    return render(request, "myprofile.html", context)


# user view profile: url 'myprofile'
@login_required
def view_profile_action(request):
    if request.method != "GET":
        raise Http404

    user = request.user
    profile = UserProfile.objects.get(user=user)
    form = UserProfileForm(instance=profile)
    rate_cnt, score, rating = calcRates(profile)
    context = {"user": user,
               "profile": profile,
               "form": form,
               "rate_cnt": rate_cnt,
               "rating": rating}
    addresses = UserLocation.objects.filter(user=user)
    if addresses.count() != 0:
        address = addresses[0]
        address1 = address.address1
        city = address.city
        state = address.state
        zip_code = address.zip_code
        context["address1"] = address1
        context["city"] = city
        context["state"] = state
        context["zip_code"] = zip_code
        context["address"] = True
    else:
        context["address"] = False
    return render(request, "myprofile.html", context)


# user edit address: url 'edit-address'
@login_required
def edit_address_action(request):
    # no user address situation
    if UserLocation.objects.filter(user=request.user).count() == 0:
        print("hihi")
        return redirect(reverse('myaddress'))

    user = request.user
    address = UserLocation.objects.get(user=user)
    try:
        if request.method == "GET":
            print("Get edit address page")
            form = UserAddressForm(instance=address)
            context = {
                'form': form,
                'address': address,
            }
            return render(request, 'edit-address.html', context)

        edit_address = UserLocation.objects.select_for_update().get(user=user)
        form = UserAddressForm(request.POST, instance=address)
        if not form.is_valid():
            context = {'form': form, 'address': address}
            return render(request, 'edit-address.html', context)

        form.save()
        address = Address.objects.get(user=user)
        context = {'form': form}
        return redirect(reverse("myaddress"))
    except:
        context = {'form': form, 'address': address}
        return redirect(reverse('myprofile'))


# user view address: url 'my-address'
@login_required
def view_address_action(request):
    if request.method != "GET":
        raise Http404

    context = {}
    try:
        userLocation = UserLocation.objects.get(user=request.user)
        context['address'] = userLocation
        print("The user has created an address!")
        return render(request, 'myaddress.html', context)
    except:
        print("The user has not created an address ...")
        return render(request, 'myaddress.html', context)


@login_required
def create_address_action(request):
    if request.method == "GET":
        return render(request, 'create-address.html')

    # one user limit to one address information
    if UserLocation.objects.filter(user=request.user).count() > 0:
        redirect('/myaddress')

    address1 = request.POST.get("address1")
    address2 = request.POST.get("address2")
    city, state = request.POST.get('city'), request.POST.get('state'),
    zip_code = request.POST.get('zip_code')

    userLocation = UserLocation(user=request.user, address1=address1, address2=address2,
                                city=city, state=state, zip_code=zip_code)
    create_address_form = UserAddressForm(request.POST, instance=userLocation)
    if not create_address_form.is_valid():
        print("User create address form is invalid ...")
        context = {'form': create_address_form}
        return render(request, 'create-address.html', context)
    print('User create address form is valid.')

    create_address_form.save()
    return redirect(reverse('myprofile'))


# handle user click registration email to activate account
def activate_action(request, code):
    emailRecords = EmailRecord.objects.filter(code=code)
    if len(emailRecords) == 1:
        emailRecord = emailRecords[0]
        email = emailRecord.email
        user = User.objects.get(email=email)
        userProfile = UserProfile.objects.get(user=user)
        userProfile.activated = True
        userProfile.save()
        print("A user clicked the activation link!")
        return render(request, 'login.html', {"msg": "User activate successfully!"})
    else:
        print("A user clicked the wrong reset-password link ...")
        return render(request, 'index.html')


# user could update password: url 'update-pwd'
def update_pwd_action(request):
    userResetPwdForm = UserResetPwdForm()
    if request.method == "GET":
        return render(request, 'reset-pwd.html', {'resetPwdForm': userResetPwdForm})

    context = {}
    form = UserResetPwdForm(request.POST)
    context["resetPwdForm"] = form

    if not form.is_valid():
        print("User update pwd form in invalid ...")
        return render(request, 'reset-pwd.html', context)

    newPwd = form.cleaned_data["password1"]
    username = form.cleaned_data["username"]
    user = User.objects.get(username=username)

    print("User: {0} update password.:{1}".format(user, newPwd))
    # update to new password
    user.set_password(newPwd)
    user.save()

    return render(request, 'login.html')


# user click reset password email link and get reset password page: url 'reset'
def get_reset_action(request, code):
    emailRecords = EmailRecord.objects.filter(code=code)
    if len(emailRecords) == 1:
        emailRecord = emailRecords[0]
        email = emailRecord.email
        print("A user clicked the reset-password link!")
        return render(request, 'reset-pwd.html')
    else:
        print("A user clicked the wrong reset-password link ...")
        return render(request, 'index.html')


# user click forget password link and get send reset password email page
# user click send email button and send reset password email: url 'forget'
def forget_pwd_action(request):
    userForgetPwdForm = UserForgetPwdForm()
    if request.method == "GET":
        return render(request, 'forgetpwd.html', {'forgetPwdForm': userForgetPwdForm})

    context = {}
    form = UserForgetPwdForm(request.POST)
    context["forgetPwdForm"] = form

    if not form.is_valid():
        print("User forget pwd form is invalid ...")
        return render(request, 'forgetpwd.html', context)

    email = form.cleaned_data['email']
    print("Send to %s"%(email))

    sendEmail(email, 'forget')
    return render(request, 'send-success.html')

# get user profile picture
@login_required
def get_picture_action(request, username="xuliangsun"):
    curr_user = request.user
    curr_username = curr_user.username
    if curr_username != username:
        other_user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=other_user)
        print("Get other user's profile picture.")
    else:
        profile = UserProfile.objects.get(user=curr_user)
        print("Get log-in user's profile picture.")
    if not profile.portrait:
        raise Http404

    return HttpResponse(profile.portrait)


# add item to sell favorite
@login_required
def favorite_sell_action(request):
    print("Enter user/favorite_sell_action")
    if request.method != "POST":
        raise Http404

    if 'itemId' not in request.POST:
        data = {'errors': 'Invalid requests'}
        return HttpResponse(json.dumps(data), content_type='application/json')

    user = request.user
    profile = UserProfile.objects.get(user=user)

    itemId = request.POST.get('itemId')
    item = SellItem.objects.get(pk=itemId)
    
    # user can favorite item only once
    if item in profile.sellFavorites.all():
        print("Already add to sell items favorites")
        return redirect(reverse('trade'))

    item.favorites += 1
    item.save()


    profile.sellFavorites.add(item)
    profile.save()

    data = {'Add to sell favorite': 'success'}
    print('Add item{0} to {1}'.format(id, request.user))

    return HttpResponse(json.dumps(data), content_type='application/json')


# add item to favorite
@login_required
def favorite_action(request):
    print("Enter user/favorite_action")
    if request.method != "POST":
        raise Http404

    if 'itemId' not in request.POST:
        data = {'errors': 'Invalid requests'}
        return HttpResponse(json.dumps(data), content_type='application/json')

    user = request.user
    profile = UserProfile.objects.get(user=user)

    itemId = request.POST.get('itemId')
    item = ExchangeItem.objects.get(pk=itemId)
    
    # user can favorite item only once
    if item in profile.exchangeFavorites.all():
        print("Already add to exchange items favorites")
        return redirect(reverse('exchange'))

    item.favorites += 1
    item.save()


    profile.exchangeFavorites.add(item)
    profile.save()

    data = {'Add to favorite': 'success'}
    print('Add item{0} to {1}'.format(id, request.user))

    return HttpResponse(json.dumps(data), content_type='application/json')


# return items of the user based on action
@login_required
def get_myitems(request, itemId):
    print("Enter user/get_myitems: get available items to select before send request")
    user = request.user
    item = ExchangeItem.objects.get(id=itemId)

    # get items (before and include 'in exchange' status)
    items = ExchangeItem.objects.filter(user=user).filter(status__lte=2) 
    request_items_ids = []
    for i in items:
        # exclude request or requested or accept or accepted items
        if i in item.request.all() or i in item.myRequesteds.all() or i in item.accept.all() or i in item.myAccepteds.all():
            continue
        request_items_ids.append(i.id)
    request_items = ExchangeItem.objects.filter(id__in=request_items_ids)

    res_items = serializers.serialize('json', request_items)

    data = {
        'items': res_items
    }
    return HttpResponse(json.dumps(data), content_type="application/json")