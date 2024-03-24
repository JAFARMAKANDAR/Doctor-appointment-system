from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from.models import *
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.shortcuts import render, get_object_or_404
from .forms import HealthHistoryForm
from django.db import IntegrityError




# Create your views here.



def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Count the number of doctors, patients, and appointments
    d = Doctor.objects.count()
    p = Patient.objects.count()
    a = Appointment.objects.count()

    # Get all doctors from the database
    doctors = Doctor.objects.all()

    # Create a dictionary to map specialties to lists of doctors
    specialty_doctor_map = {}
    for doctor in doctors:
        specialty = doctor.special  # Access the 'special' attribute of the Doctor object
        if specialty in specialty_doctor_map:
            specialty_doctor_map[specialty].append(doctor)
        else:
            specialty_doctor_map[specialty] = [doctor]

    context = {'d': d, 'p': p, 'a': a, 'specialty_doctor_map': specialty_doctor_map}
    return render(request, 'index.html', context)


def specialty_doctors(request, specialty):
    # Count the number of  appointments
    a = Appointment.objects.count()

    doctors = Doctor.objects.filter(special=specialty)
    context = {'a': a, 'specialty': specialty, 'doctors': doctors}
    return render(request, 'specialty_doctors.html', context)


#for showing signup/login button for admin(by jafar)
def adminclick_view(request):
    return render(request, 'adminclick.html')

def patientclick_view(request):
    # Count the number of  patients
    p = Patient.objects.count()
    context = {'p': p}

    return render(request, 'patientclick.html', context)

def doctorclick_view(request):
    # Count the number of doctors
    d = Doctor.objects.count()
    context = {'d': d}
    return render(request, 'doctorclick.html', context)


def Service(request):
       return render(request, 'service.html')


def About(request):
       return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Register(request):
       return render(request, 'register.html')

def Legal(request):
    return render(request, 'legal.html')

def Information(request):
    return render(request, 'information.html')


def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        # Check for errors in input
        if len(username) > 10:
            messages.error(request, "Username must be 10 characters or less")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('signup')

        if pwd1 != pwd2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # Create the user
        myuser = User.objects.create_user(username, email, pwd1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your admin account has been successfully created. Please login.")
        return redirect('login')

    else:
        # Render the signup page template for GET request
        return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpwd = request.POST.get('loginpwd')

        user = authenticate(username=loginusername, password=loginpwd)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return render(request, 'login.html', {'error': True})  # Pass error message to the template
    else:
        return render(request, 'login.html')  # Render the login page for GET requests



@never_cache
def Logout_admin(request):
    logout(request)
    messages.success(request, "Successfully Logged out  ")
    return redirect('login')



def Add_Doctor(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        special = request.POST.get('special')

        try:
            Doctor.objects.create(name=name, mobile=contact, special=special)
            error = "no"
        except Exception as e:
            print(e)  # Log the specific error for debugging
            error = "yes"
    return render(request, 'add_doctor.html', {'error': error})


def View_Doctor(request):
    if not request.user.is_authenticated:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request,'view_doctor.html', d)


def Delete_Doctor(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')



def View_Patient(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat': pat}
    return render(request, 'view_patient.html', d)



def Patient_history(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    try:
        health_history = HealthHistory.objects.get(patient=patient)
    except HealthHistory.DoesNotExist:
        health_history = None

    if request.method == 'POST':
        form = HealthHistoryForm(request.POST, instance=health_history)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Health history updated successfully.')
                # Initialize form with a new instance to clear form fields
                form = HealthHistoryForm()
            except IntegrityError:
                # Handle case where a HealthHistory instance already exists for the patient
                messages.error(request, 'Error updating health history. A health history instance already exists for this patient.')
        else:
            messages.error(request, 'Error updating health history. Please correct the errors below.')
    else:
        form = HealthHistoryForm(instance=health_history)

    return render(request, 'patient_history.html', {'patient': patient, 'health_history': health_history, 'form': form})
def update_health_history(request, patient_id):
    if request.method == 'POST':
        form = HealthHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health history updated successfully.')
            # Redirect to the patient's history page after successful update
            return redirect('patient_history', patient_id=patient_id)
        else:
            # Form data is invalid, render the form with error messages
            messages.error(request, 'Error updating health history. Please correct the errors below.')
    else:
        # If it's not a POST request, create a new form instance
        form = HealthHistoryForm()

    return render(request, 'update_health_history.html', {'form': form})



def Add_Patient(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Patient.objects.create(name=name, gender=gender, mobile=mobile, address=address)
            error = "no"
        except Exception as e:
            print(e)  # Log the specific error for debugging
            error = "yes"
    return render(request, 'add_patient.html', {'error': error})

def Delete_Patient(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')




def View_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    appoint = Appointment.objects.all()
    d = {'appoint': appoint}
    return render(request, 'view_appointment.html', d)


def Add_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None  # Initialize the error variable

    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        patient = request.POST.get('patient')
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor = Doctor.objects.filter(name=doctor).first()
        patient = Patient.objects.filter(name=patient).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=date, time1=time)
            error = "no"
        except Exception as e:
            print(e)  # Log the specific error for debugging
            error = "yes"
    return render(request, 'add_appointment.html', {'error': error, 'doctor': doctor1, 'patient': patient1})

def Delete_Appointment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_patient')
