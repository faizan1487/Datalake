from django.shortcuts import render
from .models import AlNafi_User, IslamicAcademy_User
from django.db.models import Q
from datetime import date, datetime, timedelta
from payment.models import UBL_IPG_Payment, Stripe_Payment, Easypaisa_Payment

def paying_users(query_time, isPaying):
    paying_users = []
    for user in query_time:
        pay_users = []
        ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
        easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
        stripe_user = Stripe_Payment.objects.filter(customer_email=user.email)
        pay_users.append(ubl_user)
        pay_users.append(easypaisa_user)
        pay_users.append(stripe_user)
        for pay_user in pay_users:
            for p_user in pay_user:
                if isPaying:
                    if isPaying =="True":
                        if p_user.customer_email == user.email:
                            paying_users.append(user)
                        else:
                            print("email does not exist")
                    else:
                        if p_user.customer_email != user.email:
                            paying_users.append(user)
                else:
                    return query_time
                                   
    return paying_users
    
def alnafi_user(q, start_date, end_date, isPaying):
    if start_date:
        pass
    else:
        first_user = AlNafi_User.objects.last()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = AlNafi_User.objects.first()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
        
    if q:
        queryset = AlNafi_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
        query_time = queryset.filter(Q(created_at__date__gte = end_date) & Q(created_at__date__lte = start_date))
        paying_user_queryset = paying_users(query_time, isPaying)
    else:
        query_time = AlNafi_User.objects.filter(created_at__date__lte = start_date, created_at__date__gte = end_date)
        paying_user_queryset = paying_users(query_time, isPaying)
    return paying_user_queryset

def islamic_user(q, start_date, end_date, isPaying): 
    if start_date:
        pass
    else:
        first_user = IslamicAcademy_User.objects.last()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = IslamicAcademy_User.objects.first()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj   
    if q:
        if isPaying == 'True':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__lte = start_date) & Q(created_at__date__gte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__lte = start_date) & Q(created_at__date__gte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__lte = start_date) & Q(created_at__gte = end_date))
    else:
        if isPaying == 'True':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            query_time = paying_users.filter(Q(created_at__lte = start_date) & Q(created_at__gte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            query_time = paying_users.filter(Q(created_at__lte = start_date) & Q(created_at__gte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.all()
            query_time = queryset.filter(Q(created_at__lte = start_date) & Q(created_at__gte = end_date))
            
    return query_time