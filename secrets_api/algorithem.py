from django.shortcuts import render
from rest_framework.views import APIView
from secrets_api.models import LastSecretApiUsing, AllSecretsApi,SupportLastSecretApiUsing, SupportAllSecretsApi

def round_robin():
    last_creds = LastSecretApiUsing.objects.first()
    all_creds = AllSecretsApi.objects.all()

    if last_creds and all_creds:
        # Find the next 'turn_number' in 'all_creds'
        next_turn_number = last_creds.turn_number + 1 if last_creds.turn_number < len(all_creds) else 1
        # print(next_turn_number)
        # Find the matching credential based on 'turn_number'
        matching_cred = next((cred for cred in all_creds if cred.turn_number == next_turn_number), None)
    
        if matching_cred:
            last_creds.user_name = matching_cred.user_name
            last_creds.api_key = matching_cred.api_key
            last_creds.turn_number = matching_cred.turn_number
            last_creds.secret_key = matching_cred.secret_key
            last_creds.save()
            # print("Saved")
        else:
            print("none")

    # print(last_creds.api_key)
    return last_creds.api_key, last_creds.secret_key


def round_robin_support():
    last_creds = SupportLastSecretApiUsing.objects.first()
    all_creds = SupportAllSecretsApi.objects.all()

    if last_creds and all_creds:
        # Find the next 'turn_number' in 'all_creds'
        next_turn_number = last_creds.turn_number + 1 if last_creds.turn_number < len(all_creds) else 1
        # print(next_turn_number)
        # Find the matching credential based on 'turn_number'
        matching_cred = next((cred for cred in all_creds if cred.turn_number == next_turn_number), None)
    
        if matching_cred:
            last_creds.user_name = matching_cred.user_name
            last_creds.api_key = matching_cred.api_key
            last_creds.turn_number = matching_cred.turn_number
            last_creds.secret_key = matching_cred.secret_key
            last_creds.save()
            # print("Saved")
        else:
            print("none")

    # print(last_creds.api_key)
    return last_creds.api_key, last_creds.secret_key