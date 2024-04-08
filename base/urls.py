from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    #parent url
    path('update-profile/', views.updateUser, name="update-profile"),
    path('update-profile-child/<str:pk>', views.updateChild, name="update-profile-child"),
    path('profile-child/<str:pk>', views.childProfilePage, name="profile-child"),
    path('profile-parent/<str:pk>', views.parentProfilePage, name="profile-parent"),
    path('manage-child/<str:pk>', views.manageChildPage, name="manage-child"),
    path('add-child/', views.addChild, name="add-child"),
    path('delete-child/<str:pk>', views.deleteChild, name="delete-child"),
    path('book-appointment/<str:pk>', views.bookAppointment, name="book-appointment"),

    #admin url
    path('profile-admin/<str:pk>', views.adminProfilePage, name="profile-admin"),
    path('update-profile-admin/', views.updateAdmin, name="update-profile-admin"),
    path('child-record', views.childRecordPage, name="child-record"),
    path('parent-record', views.parentRecordPage, name="parent-record"),
    path('hospital-record', views.hospitalRecordPage, name="hospital-record"),
    path('reschedule-appointment/<str:pk>', views.rescheduleAppointment, name="reschedule-appointment"),
    path('update-hospital-status/<str:pk>', views.updateHospitalStatus, name="update-hospital-status"),
    path('create-healthinfo/', views.createHealthInfo, name="create-healthinfo"),
    path('healthinfo/<str:pk>', views.viewHealthInfo, name="healthinfo"),
    path('delete-healthinfo/<str:pk>', views.deleteHealthInfo, name="delete-healthinfo"),
    path('delete-parent/<str:pk>', views.deleteParent, name="delete-parent"),
    path('delete-hospital/<str:pk>', views.deleteHospital, name="delete-hospital"),

    #hospital url
    path('profile-hospital/<str:pk>', views.hospitalProfilePage, name="profile-hospital"),
    path('view-appointment-hospital/<str:pk>', views.viewAppointmentHospital, name="view-appointment-hospital"),
    path('update-appointment-status/<str:pk>', views.updateAppointmentStatus, name="update-appointment-status"),
    path('view-vaccine-stock/<str:pk>', views.viewVaccineStock, name="view-vaccine-stock"),
    path('create-vaccine-order/', views.createVaccineOrder, name="create-vaccine-order"),

    #vaccinesupplier url
    path('manage-vaccine/', views.manageVaccine, name="manage-vaccine"),
    path('create-vaccine/', views.createVaccine, name="create-vaccine"),
    path('update-vaccine/<str:pk>', views.updateVaccine, name="update-vaccine"),
    path('delete-vaccine/<str:pk>', views.deleteVaccine, name="delete-vaccine"),
    path('vaccine/<str:pk>', views.viewVaccineInfo, name="vaccine"),
    path('view-vaccine-order/', views.viewVaccineOrder, name="view-vaccine-order"),
    path('update-order-status/<str:pk>', views.updateOrderStatus, name="update-order-status"),
    path('to-receive-order/', views.toReceiveOrder, name="to-receive-order"),
    path('track-expired-stock/', views.trackExpiryStock, name="track-expired-stock"),
]