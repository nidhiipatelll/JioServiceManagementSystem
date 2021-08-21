import random
import string
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.shortcuts import render
from .forms import FileUpload
from .models import *
import pandas as pd

global tempSessionId
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'LoginPage.html')


def login(request):
    global tempSessionId
    email = request.POST.get('txtUserEmail')
    password = request.POST.get('txtUserPass')
    user = TblRegistration.objects.filter(userEmail=email, userPassword=password)
    if user is not None:
        for item in user:
            tempSessionId = item.id
            if item.userType == "Admin":
                return render(request, 'Admin/AdminDashboard.html')
            elif item.userType == "Agent":
                return render(request, 'Agent/AgentDashboard.html')
            elif item.userType == "Customer":
                return render(request, 'Customer/CustomerDashboard.html')
            else:
                msg = "Invalid user Email or Password!"
                return HttpResponse(msg)
    else:
        msg = "Invalid user Email or Password!"
        return HttpResponse(msg)


def admineditprofile(request):
    admin_data = TblRegistration.objects.filter(userType="Admin")
    return render(request, 'Admin/AdminEditProfile.html', {'admin_data': admin_data})


def editprofile(request):
    admin_data = TblRegistration.objects.get(userType="Admin")
    uName = request.POST.get('txtUserName')
    if len(request.POST.get('txtUserName')) == 0:
        uName = admin_data.userName
    uEmail = request.POST.get('txtUserEmail')
    if len(request.POST.get('txtUserEmail')) == 0:
        uEmail = admin_data.userEmail
    uGender = request.POST.get('rbtUserGender')
    if len(request.POST.get('rbtUserGender')) == 0:
        uGender = admin_data.userGender
    uContactNo = request.POST.get('txtContactNo')
    if len(request.POST.get('txtContactNo')) == 0:
        uContactNo = admin_data.userContactNo
    uCity = request.POST.get('txtUserCity')
    if len(request.POST.get('txtUserCity')) == 0:
        uCity = admin_data.userCity
    uAddress = request.POST.get('txtUserAddress')
    if len(request.POST.get('txtUserAddress')) == 0:
        uAddress = admin_data.userAddress
    admin_data.userName = uName
    admin_data.userEmail = uEmail
    admin_data.userGender = uGender
    admin_data.userContactNo = uContactNo
    admin_data.userAddress = uAddress
    admin_data.userCity = uCity
    admin_data.save()
    admin_data = TblRegistration.objects.filter(id=admin_data.id)
    return render(request, 'Admin/AdminEditProfile.html', {'admin_data': admin_data})


def logout(request):
    return render(request, 'LoginPage.html')


def admindashboard(request):
    global tempSessionId
    if tempSessionId is not None:
        return render(request, 'Admin/AdminDashboard.html')
    else:
        return render(request, 'LoginPage.html')


def uploadsheet(request):
    return render(request, 'Admin/AdminUploadSheet.html')


def insertSheet(request):
    data = {}
    sheetData = TblSheetDetails.objects.all()
    data['customerData'] = TblRegistration.objects.filter(userType="Customer")
    data['agentData'] = TblRegistration.objects.filter(userType="Agent")
    return render(request, 'Admin/AdminManageTransaction.html', {'sheetData': sheetData})


def addtransaction(request):
    df = pd.read_csv(r'ServiceProvider1/media/uploads/JIO.xlsx')
    dforderId = df['Order ID']
    dfCustomerName = df['Customer Name']
    dfOrderAmount = df['Order Amount']
    dfCreationDate = df['Creation Date']
    dfAgentId = request.POST.get('agentlist')
    dfPaidAmount = request.POST.get('amt')
    dfSrNo = request.POST.get('srno')
    dfModificationDate = datetime.now().date()
    dfStatus = request.POST.get('status')
    return render(request, 'Admin/AdminManageTransaction.html')


def viewhistory(request):
    return render(request, 'Admin/AdminTransactionHistory.html')


def registerUser(request):
    return render(request, 'Admin/AdminRegisterUser.html')


def insertUser(request):
    if request.method == 'POST':
        userName = request.POST.get('txtUserName')
        userType = request.POST.get('rbtUserType')
        userGender = request.POST.get('rbtUserGender')
        userContactNo = request.POST.get('txtContactNo')
        userEmail = request.POST.get('txtUserEmail')
        userAddress = request.POST.get('txtUserAddress')
        userCity = request.POST.get('txtUserCity')
        userPassword = "".join((random.choice(string.ascii_lowercase) for x in range(9)))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        userCreationTime = current_time
        userCreationDate = datetime.now().date()
        userStatus = "Active"
        customerBalance = ""
        if request.POST.get('txtCustomerBalance') is not None:
            customerBalance = int(request.POST.get('txtCustomerBalance'))
        if TblRegistration.objects.filter(userEmail=userEmail).exists():
            return render(request, 'Admin/AdminRegisterUser.html')
        else:
            if userType == "Agent":
                TblReg = TblRegistration.objects.create(userName=userName, userType=userType, userGender=userGender,
                                                        userContactNo=userContactNo, userEmail=userEmail,
                                                        userAddress=userAddress,
                                                        userCity=userCity, userPassword=userPassword,
                                                        userCreationTime=userCreationTime,
                                                        userCreationDate=userCreationDate, userStatus=userStatus)
                TblReg.save()
                return render(request, 'Admin/AdminRegisterUser.html')
            elif userType == "Customer":
                TblReg = TblRegistration.objects.create(userName=userName, userType=userType, userGender=userGender,
                                                        userContactNo=userContactNo, userEmail=userEmail,
                                                        userAddress=userAddress,
                                                        userCity=userCity, userPassword=userPassword,
                                                        userCreationTime=userCreationTime,
                                                        userCreationDate=userCreationDate, userStatus=userStatus)
                TblReg.save()
                retrieveAll = TblRegistration.objects.all()
                getId = ""
                for i in retrieveAll:
                    getId = i.id
                TblCust = TblCustomerDetails.objects.create(Customerid=TblRegistration.objects.get(id=getId),
                                                            customerBalance=customerBalance)
                TblCust.save()
                return render(request, 'Admin/AdminRegisterUser.html')
            else:
                return render(request, 'Admin/AdminDashboard.html')


def viewusers(request):
    query_results = TblRegistration.objects.all()
    return render(request, 'Admin/AdminViewUsers.html', {'query_results': query_results})


def edituser(request):
    global editUserId
    editUserId = request.POST.get('edituserid')
    deleteUserId = request.POST.get('deleteid')
    if request.POST.get('deleteid'):
        query_results = TblRegistration.objects.get(id=deleteUserId)
        query_results.userStatus = "inactive"
        query_results.save()
        query_results = TblRegistration.objects.all()
        return render(request, 'Admin/AdminViewUsers.html', {'query_results': query_results})
    else:
        load_data = TblRegistration.objects.filter(id=editUserId).values()
        return render(request, 'Admin/AdminEditUser.html', {'load_data': load_data})


def updateuser(request):
    global editUserId
    load_data = TblRegistration.objects.get(id=editUserId)
    uName = request.POST.get('txtUserName')
    if len(request.POST.get('txtUserName')) == 0:
        uName = load_data.userName
    uEmail = request.POST.get('txtUserEmail')
    if len(request.POST.get('txtUserEmail')) == 0:
        uEmail = load_data.userEmail
    uGender = request.POST.get('rbtUserGender')
    if len(request.POST.get('rbtUserGender')) == 0:
        uGender = load_data.userGender
    uContactNo = request.POST.get('txtContactNo')
    if len(request.POST.get('txtContactNo')) == 0:
        uContactNo = load_data.userContactNo
    uCity = request.POST.get('txtUserCity')
    if len(request.POST.get('txtUserCity')) == 0:
        uCity = load_data.userCity
    uAddress = request.POST.get('txtUserAddress')
    if len(request.POST.get('txtUserAddress')) == 0:
        uAddress = load_data.userAddress
    uType = request.POST.get('rbtUserType')
    if len(request.POST.get('rbtUserType')) == 0:
        uType = load_data.userType
    load_data.userName = uName
    load_data.userEmail = uEmail
    load_data.userGender = uGender
    load_data.userContactNo = uContactNo
    load_data.userAddress = uAddress
    load_data.userCity = uCity
    load_data.userType = uType
    load_data.save()
    load_data = TblRegistration.objects.filter(id=editUserId)
    return render(request, 'Admin/AdminEditUser.html', {'load_data': load_data})


def agentdashboard(request):
    return render(request, 'Agent/AgentDashboard.html')


def agentupdatetransaction(request):
    return render(request, 'Agent/AgentEditTransaction.html')


def agentviewtransactions(request):
    return render(request, 'Agent/AgentViewTransactions.html')


def agentviewcustomers(request):
    query_results = TblRegistration.objects.all()
    return render(request, 'Agent/AgentViewCustomer.html', {'query_results': query_results})


def agentaddcustomer(request):
    return render(request, 'Agent/AgentAddCustomer.html')


def agenteditprofile(request):
    global tempSessionId
    """uName = request.POST.get('txtUserName')
    if len(request.POST.get('txtUserName')) == 0:
        uName = admin_data.userName
    uEmail = request.POST.get('txtUserEmail')
    if len(request.POST.get('txtUserEmail')) == 0:
        uEmail = admin_data.userEmail
    uGender = request.POST.get('rbtUserGender')
    if len(request.POST.get('rbtUserGender')) == 0:
        uGender = admin_data.userGender
    uContactNo = request.POST.get('txtContactNo')
    if len(request.POST.get('txtContactNo')) == 0:
        uContactNo = admin_data.userContactNo
    uCity = request.POST.get('txtUserCity')
    if len(request.POST.get('txtUserCity')) == 0:
        uCity = admin_data.userCity
    uAddress = request.POST.get('txtUserAddress')
    if len(request.POST.get('txtUserAddress')) == 0:
        uAddress = admin_data.userAddress
    admin_data.userName = uName
    admin_data.userEmail = uEmail
    admin_data.userGender = uGender
    admin_data.userContactNo = uContactNo
    admin_data.userAddress = uAddress
    admin_data.userCity = uCity
    admin_data.save()"""
    agent_data = TblRegistration.objects.filter(id=tempSessionId)
    return render(request, 'Agent/AgentEditProfile.html', {'agent_data': agent_data})


def agentprofile(request):
    global tempSessionId
    agent_data = TblRegistration.objects.get(id=tempSessionId)
    uName = request.POST.get('txtUserName')
    if len(request.POST.get('txtUserName')) == 0:
        uName = agent_data.userName
    uEmail = request.POST.get('txtUserEmail')
    if len(request.POST.get('txtUserEmail')) == 0:
        uEmail = agent_data.userEmail
    uGender = request.POST.get('rbtUserGender')
    if len(request.POST.get('rbtUserGender')) == 0:
        uGender = agent_data.userGender
    uContactNo = request.POST.get('txtContactNo')
    if len(request.POST.get('txtContactNo')) == 0:
        uContactNo = agent_data.userContactNo
    uCity = request.POST.get('txtUserCity')
    if len(request.POST.get('txtUserCity')) == 0:
        uCity = agent_data.userCity
    uAddress = request.POST.get('txtUserAddress')
    if len(request.POST.get('txtUserAddress')) == 0:
        uAddress = agent_data.userAddress
    agent_data.userName = uName
    agent_data.userEmail = uEmail
    agent_data.userGender = uGender
    agent_data.userContactNo = uContactNo
    agent_data.userAddress = uAddress
    agent_data.userCity = uCity
    agent_data.save()
    agent_data = TblRegistration.objects.filter(id=agent_data.id)
    return render(request, 'Agent/AgentEditProfile.html', {'agent_data': agent_data})
