from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Parent, Hospital, Child, Appointment, Vaccine, HospitalVaccine, HealthInfo
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, ChildCreationForm, UserForm, ChildForm, HospitalStatusForm, HealthInfoForm, AdminForm, AppointmentStatusForm, HospitalVaccineOrderForm, VaccineForm, OrderForm
from datetime import date, time, datetime

# Create your views here.

def home(request):
    appointments = None
    orders = None
    if request.user.is_authenticated:
        if request.user.type == "PARENT":
            parent = Parent.objects.get(id=request.user.id)
            childs = Child.objects.filter(parent=parent)
            appointments = Appointment.objects.filter(
                child__in=childs,
                status="SCHEDULED"
                )
        elif request.user.type == "HOSPITAL":
            hospitalvaccine = HospitalVaccine.objects.filter(hospital=request.user)
            appointments = Appointment.objects.filter(hospitalvaccine__in=hospitalvaccine, status="SCHEDULED")[0:5]
        elif request.user.type == "VACCINESUPPLIER":
            orders = HospitalVaccine.objects.filter(status='TOSHIP')

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    healthinfos = HealthInfo.objects.filter(
        Q(healthinfo__icontains=q) |
        Q(admin__username__icontains=q)
        )
    hospitals = Hospital.objects.exclude(status='APPROVED')

    context = {'appointments': appointments, 'healthinfos': healthinfos, 'hospitals': hospitals, 'orders': orders}
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exists")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.type == 'HOSPITAL' and user.status != 'APPROVED':
                messages.error(request, "Still waiting for admin to approve your registration.... Thank you for your patient.")
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Email or Password does not exists")


    context = {'page': page}

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.upper()
            user.save()
            return redirect('home')
        else:
            messages.error(request, "Email duplicated or password and confirmation password is not matched.")
    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            if(user.type == 'PARENT'):
                return redirect('profile-parent', pk=user.id)
            elif(user.type == 'HOSPITAL'):
                return redirect('profile-hospital', pk=user.id)

    return render(request, 'base/update_profile.html', context)

def updateAdmin(request):
    user = request.user
    form = AdminForm(instance=user)

    context = {'form': form}

    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('profile-admin', pk=user.id)

    return render(request, 'base/update_profile_admin.html', context)

@login_required(login_url='login')
def updateChild(request, pk):
    child = Child.objects.get(id=pk)
    form = ChildForm(instance=child)

    context = {'form': form}

    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, instance=child)
        if form.is_valid:
            child = form.save(commit=False)
            child.name = child.name.upper()
            child.save()
            return redirect('profile-child', pk=child.id)

    return render(request, 'base/update_profile.html', context)

def childProfilePage(request, pk):
    child = Child.objects.get(id=pk)
    appointments = Appointment.objects.filter(
        child=child,
        status="SCHEDULED"
        )
    appointments1 = Appointment.objects.filter(
        child=child,
        status="VACCINATED"
        )
    context = {'child': child, 'appointments': appointments, 'appointments1': appointments1}
    return render(request, 'base/profile_child.html', context)

def parentProfilePage(request, pk):
    user = User.objects.get(id=pk)
    appointments = None
    childs = Child.objects.filter(parent=user)
    appointments = Appointment.objects.filter(
        child__in=childs,
        status="SCHEDULED"
        )
    
    context = {'user': user, 'childs': childs, 'appointments': appointments}
    return render(request, 'base/profile_parent.html', context)

def hospitalProfilePage(request, pk):
    user = User.objects.get(id=pk)
    hospitalvaccines = HospitalVaccine.objects.filter(hospital=user)
    appointments = Appointment.objects.filter(
        hospitalvaccine__in = hospitalvaccines,
        status="SCHEDULED"
        )[0:5]
    
    context = {'user': user, 'hospitalvaccines': hospitalvaccines, 'appointments': appointments}
    return render(request, 'base/profile_hospital.html', context)

@login_required(login_url='login')
def adminProfilePage(request, pk):
    user = User.objects.get(id=pk)
    
    context = {'user': user}
    return render(request, 'base/profile_admin.html', context)

@login_required(login_url='login')
def manageChildPage(request, pk):
    user = User.objects.get(id=pk)
    childs = user.child_set.all()
    appointments = Appointment.objects.filter(
        child__in=childs,
        status="SCHEDULED"
        )

    context = {'childs': childs, 'appointments': appointments}
    return render(request, 'base/manage_child.html', context)

def addChild(request):
    if request.user.contact is None:
        return redirect('update-profile')
    
    form = ChildCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = ChildCreationForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.name = child.name.upper()
            child.parent = request.user
            child.save()
            return redirect('manage-child', pk=request.user.id)
        else:
            messages.error(request, "This IC has been registered before.")

    return render(request, 'base/add_child.html', context)

def deleteChild(request, pk):
    child = Child.objects.get(id=pk)

    try:
        appointment = Appointment.objects.get(
            child = child,
            status = 'SCHEDULED'
        )
    except:
        appointment = None

    if request.method == 'POST':
        if appointment is not None:
            hospitalvaccine = appointment.hospitalvaccine
            hospitalvaccine.stored += 1
            hospitalvaccine.booked -= 1
            hospitalvaccine.save()
        child.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': child})

def bookAppointment(request, pk):
    child = Child.objects.get(id=pk)
    try:
        vaccine = Vaccine.objects.get(startage__lte=child.age,endage__gte=child.age)
    except:
        vaccine = None
    hospitalvaccines = HospitalVaccine.objects.filter(vaccine=vaccine,status='COMPLETED',stored__gt = 0)
    hospitalvaccines2 = HospitalVaccine.objects.filter(vaccine=vaccine)
    try:
        bookedappointment = Appointment.objects.get(child=child,hospitalvaccine__in=hospitalvaccines2)
    except:
        bookedappointment = None
    context = {'hospitalvaccines': hospitalvaccines, 'child': child, 'bookedappointment': bookedappointment, 'vaccine': vaccine}

    if request.method == 'POST':
        
        input_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        input_time = datetime.strptime(request.POST.get('time'), '%H:%M').time()

        if date.today() < input_date:
            if time(10, 0) <= input_time <= time(17, 0):
                hospital = Hospital.objects.get(username=request.POST.get('hospital'))
                hospitalvaccines = HospitalVaccine.objects.filter(vaccine=vaccine, hospital=hospital).get(stored__gt = 0)
                hospitalvaccines.stored -= 1
                hospitalvaccines.booked += 1
                hospitalvaccines.save()
                Appointment.objects.create(hospitalvaccine = hospitalvaccines,child = child,date = request.POST.get('date'),time = request.POST.get('time')
                )
                return redirect('manage-child', pk=request.user.id)
            else:
                messages.error(request, "Every hospital is opening for vaccination service from 10:00am to 5:00pm.")
        else:
            messages.error(request, "You are only allowed to book appointments starting from tomorrow.")
        
    return render(request, 'base/book_appointment.html', context)

def childRecordPage(request):
    childs = Child.objects.all()
    hospitals = Hospital.objects.exclude(status='APPROVED')
    context = {'childs': childs, 'hospitals': hospitals}
    return render(request, 'base/view_child_record.html', context)

def parentRecordPage(request):
    parents = Parent.objects.all()
    hospitals = Hospital.objects.exclude(status='APPROVED')
    context = {'parents': parents, 'hospitals': hospitals}
    return render(request, 'base/view_parent_record.html', context)

def hospitalRecordPage(request):
    hospitals1 = Hospital.objects.all()
    hospitals = Hospital.objects.exclude(status='APPROVED')
    context = {'hospitals1': hospitals1 ,'hospitals': hospitals}
    return render(request, 'base/view_hospital_record.html', context)

def rescheduleAppointment(request, pk):
    child = Child.objects.get(id=pk)

    try:
        appointment = Appointment.objects.get(
            child=child,
            status="SCHEDULED"
        )
    except:
        appointment = None

    if appointment is not None:
        vaccine = appointment.hospitalvaccine.vaccine
        hospitalvaccines = HospitalVaccine.objects.filter(
            vaccine=vaccine,
            status='COMPLETED',
            stored__gt = 0
            )
    else:
        vaccine = None
        hospitalvaccines = None

    context = {'hospitalvaccines': hospitalvaccines, 'child': child, 'vaccine': vaccine, 'appointment': appointment}

    if request.method == 'POST':

        input_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        input_time = datetime.strptime(request.POST.get('time'), '%H:%M').time()

        if date.today() < input_date:
            if time(10, 0) <= input_time <= time(17, 0):
                if appointment.hospitalvaccine.hospital.username != request.POST.get('hospital'):
                    hospital = Hospital.objects.get(username=request.POST.get('hospital'))
                    hospitalvaccines = HospitalVaccine.objects.filter(vaccine=vaccine).get(hospital=hospital, status='COMPLETED', stored__gt = 0)
                    print(hospitalvaccines.stored, hospitalvaccines.booked)
                    hospitalvaccines.stored -= 1
                    hospitalvaccines.booked += 1
                    print(hospitalvaccines.stored, hospitalvaccines.booked)
                    hospitalvaccines.save()

                    hospitalvaccinesold = appointment.hospitalvaccine
                    print(hospitalvaccinesold)

                    hospitalvaccinesold.stored += 1
                    hospitalvaccinesold.booked -= 1
                    hospitalvaccinesold.save()
                    
                    appointment.hospitalvaccine = hospitalvaccines
                appointment.date = request.POST.get('date')
                appointment.time = request.POST.get('time')
                appointment.save()
                return redirect('child-record')
            else:
                messages.error(request, "Every hospital is opening for vaccination service from 10:00am to 5:00pm.")
        else:
            messages.error(request, "You are only allowed to reschedule appointments starting from tomorrow.")

    return render(request, 'base/reschedule_appointment.html', context)

def updateHospitalStatus(request, pk):
    hospital = Hospital.objects.get(id=pk)
    form = HospitalStatusForm(instance=hospital)
    context = {'form': form, 'hospital': hospital}

    if request.method == 'POST':
        form = HospitalStatusForm(request.POST, instance=hospital)
        if form.is_valid:
            form.save()
            return redirect('hospital-record')

    return render(request, 'base/update_hospital_status.html', context)

def createHealthInfo(request):
    form = HealthInfoForm()

    context = {'form': form}

    if request.method == 'POST':
        form = HealthInfoForm(request.POST)
        if form.is_valid:
            healthinfo = form.save(commit=False)
            healthinfo.admin = request.user
            healthinfo.save()
            return redirect('home')

    return render(request, 'base/create_healthinfo.html', context)

def viewHealthInfo(request, pk):
    healthinfo = HealthInfo.objects.get(id=pk)

    context = {'healthinfo': healthinfo}

    return render(request, 'base/view_healthinfo.html', context)

def deleteHealthInfo(request, pk):
    healthinfo = HealthInfo.objects.get(id=pk)

    if request.method == 'POST':
        healthinfo.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': healthinfo})

def deleteParent(request, pk):
    parent = Parent.objects.get(id=pk)

    if request.method == 'POST':
        parent.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': parent})

def deleteHospital(request, pk):
    hospital = Hospital.objects.get(id=pk)

    if request.method == 'POST':
        hospital.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': hospital})

def viewAppointmentHospital(request,pk):
    hospital = Hospital.objects.get(id = pk)
    hospitalvaccine = HospitalVaccine.objects.filter(hospital=hospital)
    appointments1 = Appointment.objects.filter(hospitalvaccine__in=hospitalvaccine)

    hospitalvaccine = HospitalVaccine.objects.filter(hospital=request.user)
    appointments = Appointment.objects.filter(hospitalvaccine__in=hospitalvaccine, status="SCHEDULED")[0:5]

    context = {'user':hospital, 'appointments1':appointments1, 'appointments':appointments}
    return render(request, 'base/view_appointment_hospital_main.html', context)

def updateAppointmentStatus(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentStatusForm(instance=appointment)
    context = {'form': form, 'appointment': appointment}

    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid:
            form.save()
            return redirect('view-appointment-hospital', request.user.id)

    return render(request, 'base/update_appointment_status.html', context)

def viewVaccineStock(request,pk):
    hospital = Hospital.objects.get(id=pk)
    hospitalvaccines = HospitalVaccine.objects.filter(hospital = hospital)

    appointments = Appointment.objects.filter(hospitalvaccine__in=hospitalvaccines, status="SCHEDULED")[0:5]

    context = {'hospital':hospital, 'hospitalvaccines' : hospitalvaccines, 'appointments':appointments}
    return render(request, 'base/view_vaccine_stock.html', context)

def createVaccineOrder(request):
    if request.user.contact is None:
        return redirect('update-profile')
    
    form = HospitalVaccineOrderForm()
    context = {'form': form}

    if request.method == 'POST':
        hospitalvaccine = HospitalVaccine.objects.filter(hospital = request.user, stored__gt = 0, vaccine = request.POST.get('vaccine'))
        if hospitalvaccine.exists():
            messages.error(request, "Unable to order. Vaccine stock of this vaccine still available.")

        else:
            form = HospitalVaccineOrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.hospital = request.user
                order.save()
                return redirect('view-vaccine-stock', pk=request.user.id)

    return render(request, 'base/create_vaccine_order.html', context)

def manageVaccine(request):
    vaccines = Vaccine.objects.all()
    orders = HospitalVaccine.objects.filter(status='TOSHIP')

    context = {'vaccines': vaccines, 'orders': orders}

    return render(request, 'base/manage_vaccine.html', context)

def createVaccine(request):
    form = VaccineForm()
    context = {'form': form}

    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-vaccine')

    return render(request, 'base/create_vaccine.html', context)

def updateVaccine(request, pk):
    vaccine = Vaccine.objects.get(id=pk)
    form = VaccineForm(instance=vaccine)
    context = {'form': form, 'vaccine': vaccine}

    if request.method == 'POST':
        form = VaccineForm(request.POST, instance=vaccine)
        if form.is_valid:
            form.save()
            return redirect('manage-vaccine')

    return render(request, 'base/update_vaccine.html', context)

def deleteVaccine(request, pk):
    vaccine = Vaccine.objects.get(id=pk)

    if request.method == 'POST':
        vaccine.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': vaccine})

def viewVaccineInfo(request, pk):
    vaccine = Vaccine.objects.get(id=pk)

    context = {'vaccine': vaccine}

    return render(request, 'base/view_vaccine_info.html', context)

def viewVaccineOrder(request):
    orders1 = HospitalVaccine.objects.filter(status='TOSHIP')
    orders = HospitalVaccine.objects.filter(status='TOSHIP')

    context = {'orders1': orders1, 'orders': orders}

    return render(request, 'base/view_vaccine_order_main.html', context)

def updateOrderStatus(request, pk):
    order = HospitalVaccine.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form, 'order': order}

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            order = form.save(commit=False)
            if request.POST.get('status') == 'TORECEIVE' or request.POST.get('status') == 'TOSHIP':
                order.expiry = request.POST.get('date')
            order.save()
            if order.status == 'TORECEIVE':
                return redirect('view-vaccine-order')
            elif order.status == 'COMPLETED':
                return redirect('to-receive-order')
            elif order.status == 'EXPIRED' or order.status == 'TOSHIP':
                return redirect('track-expired-stock')

    return render(request, 'base/update_order_status.html', context)

def toReceiveOrder(request):
    orders1 = HospitalVaccine.objects.filter(status='TORECEIVE')
    orders = HospitalVaccine.objects.filter(status='TOSHIP')

    context = {'orders1': orders1, 'orders': orders}

    return render(request, 'base/view_vaccine_order_main.html', context)

def trackExpiryStock(request):
    orders1 = HospitalVaccine.objects.filter(Q(status='COMPLETED') | Q(status='EXPIRED'))
    orders = HospitalVaccine.objects.filter(status='TOSHIP')

    context = {'orders1': orders1, 'orders': orders}

    return render(request, 'base/view_vaccine_order_main.html', context)