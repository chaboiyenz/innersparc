from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum, F


def home(request):
    return render(request, 'index.html')

def navbar(request):
    return render(request, 'navbar.html', {'user': request.user})

def signin(request):
    if request.user.is_authenticated:
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to the same page after login
        else:
            return render(request, "signin.html", {"error": "Invalid username or password"})

    return render(request, "signin.html")

@login_required
def signout(request):
    logout(request)
    return redirect("signin")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please wait for admin approval.")
            return redirect("signin")  # Redirect to login page
    else:
        form = SignUpForm()
    
    return render(request, "signup.html", {"form": form})

@login_required(login_url='signin')
def profile(request, id):
    user_profile = get_object_or_404(Profile, id=id)  # Fetch profile by ID
    return render(request, 'profile.html', {'user_profile': user_profile})


def monthly_sales_data(request):
    sales = (
        Sale.objects.filter(status='active')
        .annotate(month=F('created_at__month'))
        .values('month')
        .annotate(total_price=Sum('price'))
        .order_by('month')
    )

    data = {str(item["month"]): float(item["total_price"]) for item in sales}
    return JsonResponse(data)

@login_required(login_url='signin')
def dashboard(request):
    user_profile = Profile.objects.get(user=request.user)

    # Compute sales stats
    sales = Sale.objects.filter(agent__is_approved=True).order_by('-price')
    agents = Profile.objects.filter(is_approved=True).annotate(
        sales_volume=Sum('sales__price')
    ).order_by('-sales_volume')

    total_sales = sales.aggregate(total=Sum('price'))['total'] or 0
    active_sales = sales.filter(status='active').aggregate(total=Sum('price'))['total'] or 0
    cancelled_sales = sales.filter(status='cancelled').aggregate(total=Sum('price'))['total'] or 0
    total_agents = agents.count()

    return render(request, 'dashboard.html', {
        'sales': sales,
        'agents': agents,
        'total_sales': total_sales,
        'active_sales': active_sales,
        'cancelled_sales': cancelled_sales,
        'total_agents': total_agents,
        'user_profile': user_profile
    })


@login_required(login_url='signin')
def approve(request):
    accounts = Profile.objects.filter(is_approved=False)  # Get only unapproved users
    context = {
        'accounts': accounts,
    }
    return render(request, 'approve.html', context)

def approve_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.user.username} has been approved!")
    return redirect('approve')

def reject_user(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.user.delete()  # Deletes the user and profile
    messages.error(request, f"User {profile.user.username} has been declined.")
    return redirect('approve')
 