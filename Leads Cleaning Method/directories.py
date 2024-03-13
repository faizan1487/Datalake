import os
from datetime import datetime

def create_folders():
    # Get today's date
    today = datetime.today().strftime('%d-%m-%Y')

    # Create main folder with today's date
    main_folder = os.path.join(os.getcwd(), today)
    try:
        os.makedirs(main_folder)
        print(f"Main folder '{today}' created successfully.")
    except FileExistsError:
        print(f"Main folder '{today}' already exists.")

    # Create Downloaded_leads folder
    downloaded_leads_folder = os.path.join(main_folder, 'Downloaded_Leads')
    try:
        os.makedirs(downloaded_leads_folder)
        print("Downloaded_leads folder created successfully.")
    except FileExistsError:
        print("Downloaded_leads folder already exists.")

    # Create clean_leads folder
    clean_leads_folder = os.path.join(main_folder, 'Clean_Leads')
    try:
        os.makedirs(clean_leads_folder)
        print("clean_leads folder created successfully.")
    except FileExistsError:
        print("clean_leads folder already exists.")

if __name__ == "__main__":
    create_folders()
