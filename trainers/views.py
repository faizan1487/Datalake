from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Create your views here.
from payment.models import Main_Payment
from payment.serializer import MainPaymentSerializer, AlNafiPaymentSerializer
from products.models import Alnafi_Product, Main_Product
from trainers.models import Trainer
from user.models import AlNafi_User, Main_User
from user.serializers import MainUserSerializer
from collections import defaultdict
import json
from django.db.models import F, Max, Q, Prefetch, Max, Min, Count, OuterRef, Subquery
from django.conf import settings
from datetime import date, datetime, time, timedelta
from user.serializers import MainUserSerializer
from user.services import upload_csv_to_s3
import pandas as pd
import os
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Trainer
import re


class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100




class TrainersData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        active = self.request.GET.get('active', None) or None
        product_name = self.request.GET.get('product', None)
        plan = self.request.GET.get('plan', None)
        export = self.request.GET.get('export', None) or None
        req_start_date = self.request.GET.get('start_date', None) or None
        req_end_date = self.request.GET.get('end_date', None) or None
        # url = request.build_absolute_uri()

        #8 queries outside loop
        trainers = Trainer.objects.all().prefetch_related('products__product_payments__user')
        if q:
            if request.user.is_admin:
                trainer = trainers.get(email__iexact=q.strip())
            else:
                trainers = trainers.get(email__iexact=request.user.email)
        else:
            if request.user.is_admin:
                trainer = trainers.get(email__iexact='sana@gmail.com')
            else:
                trainer = trainers.get(email__iexact=request.user.email)
        trainers_data = []
        exports_data = []
        current_datetime = datetime.now()
        export_data = {
            'export_trainer_name': trainer.trainer_name,
            'export_trainer_data': []
        }
    
        trainer_data = {
            'trainer_name': trainer.trainer_name,
            'trainer_email': trainer.email,
            'users': []
        }

        # if product_name:
        #     products = trainer.products.filter(product_name=product_name)
        # else:
        #     products = trainer.products.all()


        if product_name:
            keywords = product_name.split()
            query = Q()
            for keyword in keywords:
                query &= Q(product_name__icontains=keyword)
                products = trainer.products.filter(query)
        else:
            products = trainer.products.all()

        if plan:
            products_list = []
            lower_plan = plan.lower()
            pattern = r'\b(monthly|quarterly|half yearly|yearly)\b'

            for product in products:
                product_name = product.product_name.lower()
                matches = re.findall(pattern, product_name)

                if matches:
                    if lower_plan == matches[0]:
                        products_list.append(product)

             
            products = products_list
        

        #total 5 queries in one loop
        for product in products:
            #1 query from here
            #Replace userid and productid with user email and product name
            product_payments = product.product_payments.values('alnafi_payment_id','user_id',
                                                                'product_id','amount','currency',
                                                                'order_datetime','source',
                                                                'expiration_datetime','created_datetime')

            # print(product_payments)
            #no effect on query  

            #1 queries from here
            dates = product_payments.values('order_datetime')
            #1 queries from here
            result = dates.aggregate(greatest_order_datetime=Max('order_datetime'), lowest_order_datetime=Min('order_datetime'))
            greatest_order_datetime = result['greatest_order_datetime']
            lowest_order_datetime = result['lowest_order_datetime']
            
            
            if not req_start_date:
                start_date=lowest_order_datetime
            else:
                start_date = req_start_date
            if not req_end_date:
                end_date=greatest_order_datetime
            else:
                end_date = req_end_date

            # #no effect on query
            product_payments = product_payments.filter(order_datetime__range=(start_date, end_date))
            
            #2 queries from here
            users = list(product_payments.values('user__first_name','user__last_name','user__email','user__phone','product__product_name'))
            payment_list = list(product_payments.values('alnafi_payment_id','user_id','source',
                                                                'product_id','amount','currency',
                                                                'order_datetime',
                                                                'expiration_datetime','created_datetime'))
            #no effect on query
            for i in range(len(payment_list)):
                try:
                    payment_list[i]['user_id'] = users[i]['user__email']
                    payment_list[i]['first_name'] = users[i]['user__first_name']
                    payment_list[i]['last_name'] = users[i]['user__last_name']
                    payment_list[i]['product_id'] = users[i]['product__product_name']
                except Exception as e:
                    pass
            
            #no effect on query
            if payment_list:
                if active == 'true':
                    payment_list = [
                        {**payment, 'active': "true"}
                        for payment in payment_list if payment.get('expiration_datetime') and payment.get('expiration_datetime') > current_datetime
                    ]
                elif active == 'false':
                    payment_list = [
                        {**payment, 'active': "false"}
                        for payment in payment_list if payment.get('expiration_datetime') and payment.get('expiration_datetime') < current_datetime
                    ]
                else:
                    active_payments = [
                        {**payment, 'active': "true"}
                        for payment in payment_list if payment.get('expiration_datetime') and payment.get('expiration_datetime') > current_datetime
                    ]
                    inactive_payments = [
                        {**payment, 'active': "false"}
                        for payment in payment_list if payment.get('expiration_datetime') and payment.get('expiration_datetime') < current_datetime
                    ]
                    payment_list = active_payments + inactive_payments

            #no effect on query
            user_count = len(set(payment['user_id'] for payment in payment_list))
            
            # Removing duplicates payments of a single user
            #no effect on query
            payments_list = []
            for payment in payment_list:
                if 'Half Yearly' in payment['product_id']:
                    payment['plan'] = 'Half Yearly'
                elif 'Yearly' in payment['product_id']:
                    payment['plan'] = 'Yearly'
                elif 'Quarterly' in payment['product_id']:
                    payment['plan'] = 'Quarterly'
                elif 'Monthly' in payment['product_id']:
                    payment['plan'] = 'Monthly'

                is_unique = True
                for pay in payments_list:
                    if payment['user_id'] == pay['user_id']:
                        is_unique = False
                        break
                if is_unique:
                    trainer_data['users'].append(payment)
                    payments_list.append(payment)
            export_data['export_trainer_data'].append({'product_name':product.product_name, 'users_count': user_count,'users': payments_list})
            
            if not req_start_date:
                start_date = None
            if not req_end_date:
                end_date = None
    
        trainers_data.append(trainer_data)
        exports_data.append(export_data)

        if export=='true':
            for i in export_data['export_trainer_data']:
                # print(i)
                # for i in exports_dataexport_data['trainer_data']
                i['trainer_name'] = export_data['export_trainer_name']
            # print(export_data)
            #For CSV WORKING:
            Header = []
            for i in export_data['export_trainer_data']:
                for data_dict in i["users"]:
                    if data_dict:
                        Header.extend(['trainer_name', 'product_name'])
                        Header.extend(data_dict.keys())
                        break
            if Header:
                pass
            else:
                Header = ['trainer_name','product_name', 'alnafi_payment_id','user_id','source','product_id','amount','currency','order_datetime','expiration_datetime']

            # Create an empty DataFrame with the specified columns
            # df = pd.DataFrame(columns=Header)
            
            # Create a list to hold the DataFrames
            dfs = []

            for i in export_data['export_trainer_data']:
                # print(i)
                trainer_name = i['trainer_name']
                product_name = i['product_name']
                for data_dict in i["users"]:
                    if data_dict:
                        data_dict["trainer_name"] = trainer_name
                        data_dict["product_name"] = product_name
                        dfs.append(pd.DataFrame([data_dict]))
                        # df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
                        # df = df.append(data_dict, ignore_index=True)
            
            # Concatenate all DataFrames in the list
            df = pd.concat(dfs, ignore_index=True)
            
            file_name = f"Trainers_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = df.to_csv(index=False)
            s3 = upload_csv_to_s3(df,file_name)
            data = {'file_link': file_path,'export':'true'}
            return Response(data)
        else:
            return Response(trainers_data)




class TrainerProducts(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self,request):
    #     trainer_email = request.GET.get('q').strip()
    #     trainer = get_object_or_404(Trainer, email__iexact=trainer_email)
    #     products = trainer.products.all().values("product_name")
    #     # print(products)
    #     return Response(products)
    

    def get(self,request):
        # queryset = Alnafi_Product.objects.exclude(name__in=['test','test10']).values_list('name', flat=True)
        trainer_email = request.GET.get('q').strip()
        trainer = get_object_or_404(Trainer, email__iexact=trainer_email)
        products = trainer.products.all().values("product_name")
        words_to_remove = ['Wnglish','01_2_7','01_2_4','01_2_6','Brazil','(Italy)',' in english','Bengali','Mandarin',' in','yearly','Annual in english','Half Yearly in english','Quarterly in english','Quarterly','half','Half', 'Monthly', 'Yearly', 'HalfYearly','Annual',' halfyearly','QUARTERLY','annual','Quaterly','TEST','English','english','Urdu','Italian','French','Chinese','Spanish','Arabic','Malay','Indonesian','Hindi','Bangla','Portuguese','Swahili','Russian','Japanese','Persian','Filipino','Turkish','Marathi','Javanese','German','Vietnamese']
        to_not_remove = ['Arabic for Urdu Speakers']
        # return Response(queryset)
    
        query_objects_without_words = []
        for product in products:
            name = product["product_name"]
            for word in words_to_remove:
                if name not in to_not_remove:
                    name = name.replace(word, '')  # Remove the word from the name
            query_objects_without_words.append(name)

        
        names_list_without_spaces = [name.rstrip() for name in query_objects_without_words]
        names_list_without_duplicates = list(set(names_list_without_spaces))
        filtered_list = [item for item in names_list_without_duplicates if item != ""]
        
        return Response(filtered_list)




class AnalyticsTrainers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        trainers = Trainer.objects.all()
        if q:
            trainers = trainers.filter(trainer_name__icontains=q)

        trainers_data = []

        for trainer in trainers:
            trainer_data = {
                'trainer_name': trainer.trainer_name,
                'user_counts': []
            }

            user_count = 0

            products = trainer.products.all().prefetch_related('product_payments')
            payments = Main_Payment.objects.filter(product__in=products).order_by('order_datetime')

            for payment in payments:
                user_count += 1
                trainer_data['user_counts'].append({
                    'order_datetime': payment.order_datetime,
                    'user_count': user_count
                })
            trainers_data.append(trainer_data)


        # print(trainers_data)
        return Response(trainers_data)


class TrainersName(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # queryset = Trainer.objects.values_list('trainer_name','email')
        queryset = Trainer.objects.values('trainer_name', 'email')
        trainer_list = [{"trainer_name": item['trainer_name'], "email": item['email']} for item in queryset]


        return Response(trainer_list)







# class TrainersData(APIView):
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [GroupPermission]
#     # required_groups = ['Sales', 'Admin']
#     def get(self, request):
#         q = self.request.GET.get('q', None) or None
#         product = self.request.GET.get('product', None)
#         export = self.request.GET.get('export', None) or None
#         # create a datetime object for 24 hours ago
#         url = request.build_absolute_uri()


#         # payments = Main_Payment.objects.filter(product__product_name__icontains='Python Automation - Tools and handson')
#         # print(payments)
#         # payments = payments.exclude(amount__in=[0,0.1,1,2,0.01,1.0,2.0,3.0,4.0,5.0,5.0,6.0,7.0,8.0,9.0,10.0,10])
#         # distinct_users = payments.order_by('user').values('user').distinct()
#         trainers = Trainer.objects.all()
#         if q:
#             trainers = trainers.filter(trainer_name__icontains=q)

#         if product:
#             keywords = product.split()
#             query = Q()
#             for keyword in keywords:
#                 query &= Q(products__product_name__icontains=keyword)
#                 trainers = trainers.filter(query)

#         trainers = trainers.annotate(total_users=Count('products__product_payments__user', distinct=True)).values('trainer_name', 'products__product_name', 'products__product_payments__user__email','products__product_payments__user__username')
#         # Create a dictionary to store the grouped data
#         grouped_data = defaultdict(lambda: defaultdict(list))

#         # Iterate over the queryset and group the data
#         for trainer in trainers:
#             trainer_name = trainer['trainer_name']
#             product_name = trainer['products__product_name']
#             user_email = trainer['products__product_payments__user__username' if 'products__product_payments__user__email' == None else 'products__product_payments__user__email']
#             grouped_data[trainer_name][product_name].append(user_email)

#         # print(grouped_data)

#         # Convert the grouped data to a list of dictionaries
#         result = []
#         for trainer_name, products in grouped_data.items():
#             # print("trainer_namee",trainer_name)
#             # print("products",products)
#             for product_name, users in products.items():
#                 result.append({
#                     'trainer_name': trainer_name,
#                     'product_name': product_name,
#                     # 'users': users,
#                     'user_count': len(users)-1 if users[0] == None else len(users)
#                 })
#                 # print("users",len(users))

#         # print(result[-1])
#         # payments = payments.filter(user__id__in=Subquery(distinct_users)).values('product__id', 'product__product_name').annotate(total_payments=Count('id'))
#         paginator = MyPagination()
#         paginated_queryset = paginator.paginate_queryset(result, request)
#         return paginator.get_paginated_response(paginated_queryset)



# class TrainersData(APIView):
#     def get(self, request):
#         q = self.request.GET.get('q', None) or None
#         product = self.request.GET.get('product', None)
#         export = self.request.GET.get('export', None) or None
#         url = request.build_absolute_uri()

#         trainers = Trainer.objects.all().prefetch_related('products__product_payments__user')
#         if q:
#             trainers = trainers.filter(trainer_name__icontains=q)

#         if product:
#             keywords = product.split()
#             query = Q()
#             for keyword in keywords:
#                 query &= Q(products__product_name__icontains=keyword)
#             trainers = trainers.filter(query)

#         trainers_data = []

#         for trainer in trainers:
#             trainer_data = {
#                 'trainer_name': trainer.trainer_name,
#                 'products': {}
#             }

#             for product in trainer.products.all():
#                 user_count = len(set(payment.user_id for payment in product.product_payments.all()))
#                 trainer_data['products'][product.product_name] = user_count

#             trainers_data.append(trainer_data)

#         return Response(trainers_data)





# payments = Main_Payment.objects.exclude(product__product_name="test").exclude(amount=1).filter(source__in=['Easypaisa','UBL_IPG','Stripe'])

#     if source:
#         payments = payments.filter(source=source)

#     if not start_date:
#         if payments:
#             first_payment = payments.exclude(order_datetime=None).last()
#             date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#             new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
#             start_date = new_date_obj + timedelta(days=20)
#     if not end_date:
#         if payments:
#             last_payment = payments.exclude(order_datetime=None).first()
#             date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#             new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
#             end_date = new_date_obj - timedelta(days=20)

#     delta = end_date - start_date
#     dates = []
#     for i in range(delta.days + 1):
#         date = start_date + timedelta(days=i)
#         dates.append(date)

#     payments = payments.filter(order_datetime__date__in=dates)
#     payment_dict = {}
#     for payment in payments:
#         if payment.order_datetime.date() in payment_dict:
#             payment_dict[payment.order_datetime.date()].append(payment)
#         else:
#             payment_dict[payment.order_datetime.date()] = [payment]

#     response_data = []
#     for date in dates:
#         if date.date() in payment_dict:
#             payments_for_date = payment_dict[date.date()]
#             serialized_payments = MainPaymentSerializer(payments_for_date, many=True).data
#         else:
#             serialized_payments = []

#         response_data.append({
#             'date': date.date(),
#             'payments': len(serialized_payments)
#         })

#     print(payments.count())
#     return response_data
