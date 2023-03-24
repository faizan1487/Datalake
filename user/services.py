from django.shortcuts import render
from .models import AlnafiUser, IslamicAcademyUser
from django.db.models import Q
from datetime import date, datetime, timedelta
from payment.models import UBL_IPG_Payment, Payment, Easypaisa_Payment

def paying_users(isPaying):
    queryset = AlnafiUser.objects.all()
    paying_users = []
    for user in queryset:
        pay_users = []
        ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
        easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
        stripe_user = Payment.objects.filter(email=user.email)
        pay_users.append(ubl_user)
        pay_users.append(easypaisa_user)
        # pay_users.append(stripe_user)
        for pay_user in pay_users:
            for p_user in pay_user:
                if isPaying =="True":
                    if p_user.customer_email == user.email:
                        paying_users.append(user)   
                        # if p_user.email == user.email:
                        #     paying_users.append(user)
                            
    return paying_users
    
    
    
def alnafi_user(q, start_date, end_date, isPaying):
    if start_date:
        pass
    else:
        first_user = AlnafiUser.objects.last()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = AlnafiUser.objects.first()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
        
    if q:
        if isPaying =='True':
            # paying_user = paying_users(isPaying)
            queryset = AlnafiUser.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
            query_time = queryset.filter(Q(created_at__gte = end_date) & Q(created_at__lte = start_date))
        elif isPaying =='False':
            queryset = AlnafiUser.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
            query_time = queryset.filter(Q(created_at__gte = end_date) & Q(created_at__lte = start_date))
            # paying_user = paying_users(query_time)
        else:
            queryset = AlnafiUser.objects.filter(
                Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
            query_time = queryset.filter(Q(created_at__gte = end_date) & Q(created_at__lte = start_date))
            # paying_user = paying_users(query_time)
    else:
        queryset = AlnafiUser.objects.all()
        query_time = queryset.filter(created_at__lte = start_date, created_at__gte = end_date)    
    return query_time

def islamic_user(q, start_date, end_date, isPaying): 
    if start_date:
        pass
    else:
        first_user = IslamicAcademyUser.objects.last()
        date_time_obj = first_user.date_created.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = IslamicAcademyUser.objects.first()
        date_time_obj = last_user.date_created.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj   
    if q:
        if isPaying == 'True':
            paying_users = IslamicAcademyUser.objects.filter(is_paying_customer=True)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademyUser.objects.filter(is_paying_customer=False)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
        else:
            queryset = IslamicAcademyUser.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
    else:
        if isPaying == 'True':
            paying_users = IslamicAcademyUser.objects.filter(is_paying_customer=True)
            query_time = paying_users.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademyUser.objects.filter(is_paying_customer=False)
            query_time = paying_users.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
        else:
            queryset = IslamicAcademyUser.objects.all()
            query_time = queryset.filter(Q(date_created__lte = start_date) & Q(date_created__gte = end_date))
            
    return query_time