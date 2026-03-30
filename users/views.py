from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
import uuid


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # 🔥 ERP ACCESS CHECK
            if request.path.startswith("/erp"):
                if not user.is_erp_user:
                    messages.error(request, "No ERP access")
                    return redirect("/login/")

                if not user.is_approved:
                    messages.error(request, "Waiting for admin approval")
                    return redirect("/login/")

            login(request, user)

            # ROLE REDIRECT
            if user.role == "student":
                return redirect("/student/dashboard/")
            elif user.role == "teacher":
                return redirect("/erp/dashboard/")
            elif user.role == "admin":
                return redirect("/erp/dashboard/")
                

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "index.html")

@login_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")


@login_required
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")


@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
def erp_dashboard(request):
    if not request.user.is_erp_user:
        return redirect("/")

    return render(request, "erp_dashboard.html")

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            password=password,
            role="student",
            is_erp_user=False,
            is_approved=True
        )

        login(request, user)
        return redirect("//")

    return render(request, "register.html")

def erp_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_erp_user and user.is_approved:
            login(request, user)
            return redirect("/erp/dashboard/")
        else:
            messages.error(request, "Unauthorized ERP access")

    return render(request, "erp_login.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def edtech_register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 🔒 Password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("users:edtech_register")

        # 🔒 Email unique
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("users:edtech_register")

        # 🔥 Create username automatically from email
        username = email.split("@")[0] + str(uuid.uuid4())[:5]
        # Handle duplicate username
        if User.objects.filter(username=username).exists():
            username = username + "_user"

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="user"
        )

        login(request, user)
        messages.success(request, "Account created successfully!")

        return redirect("/")

    return render(request, "register.html")

def edtech_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")




@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":

        # BASIC INFO
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.phone = request.POST.get("phone")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.pincode = request.POST.get("pincode")
        user.about_me = request.POST.get("about_me")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        # 🔥 EXPERIENCE
        Experience.objects.filter(user=user).delete()

        companies = request.POST.getlist("company[]")
        roles = request.POST.getlist("role[]")
        start_dates = request.POST.getlist("start_date[]")
        end_dates = request.POST.getlist("end_date[]")

        for i in range(len(companies)):
            if companies[i]:
                Experience.objects.create(
                    user=user,
                    company=companies[i],
                    role=roles[i],
                    start_date=start_dates[i],
                    end_date=end_dates[i] or None
                )

        # 🔥 EDUCATION
        Education.objects.filter(user=user).delete()

        degrees = request.POST.getlist("degree[]")
        institutes = request.POST.getlist("edu_institute[]")
        years = request.POST.getlist("year[]")

        for i in range(len(degrees)):
            if degrees[i]:
                Education.objects.create(
                    user=user,
                    degree=degrees[i],
                    institute=institutes[i],
                    start_year=years[i]
                )

        # 🔥 QUALIFICATION
        Qualification.objects.filter(user=user).delete()

        titles = request.POST.getlist("qualification[]")

        for t in titles:
            if t:
                Qualification.objects.create(user=user, title=t)

        messages.success(request, "Profile Updated Successfully!")

        return redirect("users:edtech_profile")

    context = {
        "user": user,
        "experiences": user.experiences.all(),
        "educations": user.educations.all(),
        "qualifications": user.qualifications.all()
    }

    return render(request, "profile.html", context)

from .models import Experience, Education
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == "POST":

        # ===== BASIC INFO =====
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.pincode = request.POST.get("pincode")

        user.occupation = request.POST.get("occupation")
        user.institute = request.POST.get("institute")
        user.about_me = request.POST.get("about_me")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        # ===== EXPERIENCE =====
        Experience.objects.filter(user=user).delete()

        companies = request.POST.getlist("company[]")
        roles = request.POST.getlist("role[]")
        start_dates = request.POST.getlist("start_date[]")
        end_dates = request.POST.getlist("end_date[]")
        is_current_list = request.POST.getlist("is_current[]")  # only checked ones

        for i, company in enumerate(companies):
            if company:

                is_current = str(i) in is_current_list

                start_date = start_dates[i] if i < len(start_dates) and start_dates[i] else None
                end_date = end_dates[i] if i < len(end_dates) and end_dates[i] else None

                Experience.objects.create(
                    user=user,
                    company=company,
                    role=roles[i] if i < len(roles) else None,
                    start_date=start_date,
                    end_date=None if is_current else end_date,
                    is_current=is_current,
                )

        # ===== EDUCATION =====
        Education.objects.filter(user=user).delete()

        degrees = request.POST.getlist("degree[]")
        institutes = request.POST.getlist("edu_institute[]")
        years = request.POST.getlist("year[]")

        for i in range(len(degrees)):
            if degrees[i]:
                Education.objects.create(
                    user=user,
                    degree=degrees[i],
                    institute=institutes[i],
                    start_year=years[i] if years[i] else None,
                )

        messages.success(request, "Profile updated successfully!")

        return redirect("users:edtech_profile")

    return render(request, "edit_profile.html", {
        "user": user,
        "experiences": user.experiences.all(),
        "educations": user.educations.all(),
    })