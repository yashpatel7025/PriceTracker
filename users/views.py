
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from track.models import Product
# Create your views here.

def register(request):

        if request.method == 'POST':#when client click on SIGN UP there we have type=submit 
                                    #therefor it will give POST reqest and this if will be executed
                                    #request will have everything...
                                    #we can access evey field of frontend side...which user have entered 
                                    #by uing 'request.POST' we can access everfield data enterd by user
                                    #example is shown in track app.....ok and ok2 view
            form = UserRegisterForm(request.POST)
            if form.is_valid():
	            form.save()   #if you dont write this then user name will not register to database
	            username = form.cleaned_data.get('username')
	            messages.success(request, f'Your account has been created..!')
	            return redirect('login')
        else: #<-------method wil be GET...
            #whenever we come here  from url then it will be GET method.
            
       		 form = UserRegisterForm()
        myform={
         'form':form

        }
        return render(request,'users/register.html',myform)


#@login_required it will only run if user is already logged in other wise it will automatically redirect to login page
                 #(differnt url will be there for login page something like ?next/prifile)
                 #first and after sucessfull log in it will redirect to profile page
@login_required
def profile(request):
    if request.method == 'POST':         
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        
    }
    
    return render(request,'users/profile.html',context)
