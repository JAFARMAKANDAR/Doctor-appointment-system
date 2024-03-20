from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from.models import *


# Create your views here.
def index(request):
    # Check if the user is a staff member
    if not request.user.is_staff:
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
    doctors = Doctor.objects.filter(special=specialty)
    context = {'specialty': specialty, 'doctors': doctors}
    return render(request, 'specialty_doctors.html', context)


def Service(request):
       return render(request, 'service.html')


def About(request):
       return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Register(request):
       return render(request, 'register.html')

def Login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('home')
            else:
                error = "Invalid credentials"
        else:
            error = "Invalid credentials"

    return render(request, 'login.html', {'error': error})

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')



def Add_Doctor(request):
    if not request.user.is_staff:
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
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request,'view_doctor.html', d)


def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')



def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat': pat}
    return render(request, 'view_patient.html', d)


def Add_Patient(request):
    if not request.user.is_staff:
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
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')




def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appoint = Appointment.objects.all()
    d = {'appoint': appoint}
    return render(request, 'view_appointment.html', d)


def Add_Appointment(request):
    if not request.user.is_staff:
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
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_patient')
