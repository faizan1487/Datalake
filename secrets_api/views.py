from django.shortcuts import render
from rest_framework.views import APIView
from secrets_api.models import LastSecretApiUsing, AllSecretsApi
from rest_framework.response import Response
# Create your views here.


class GetData(APIView):
    def get(self, request):
        try:
            last_creds = LastSecretApiUsing.objects.first()
            all_creds = AllSecretsApi.objects.all()

            if last_creds and all_creds:
                # Find the next 'turn_number' in 'all_creds'
                next_turn_number = last_creds.turn_number + 1 if last_creds.turn_number < len(all_creds) else 1

                # Find the matching credential based on 'turn_number'
                matching_cred = next((cred for cred in all_creds if cred.turn_number == next_turn_number), None)

                if matching_cred:
                    last_creds.user_name = matching_cred.user_name
                    last_creds.api_key = matching_cred.api_key
                    last_creds.turn_number = matching_cred.turn_number
                    last_creds.secret_key = matching_cred.secret_key
                    last_creds.save()

            return Response({'msg': 'ok'})
        except Exception as e:
            # Handle any exceptions that might occur during this process
            return Response({'error': str(e)})