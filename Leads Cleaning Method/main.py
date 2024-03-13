import excell_sheet
import crm_api


if __name__ == "__main__":
    
    file_path = '/home/owais/Documents/DATA LAKE/Leads_Cleaning/New_Method/27-02-2024/Downloaded_Leads/Pak-Cyber Security leads-14-2-24_Leads_2024-02-13_2024-02-26.xlsx'
    
    city = "-"
    
    form = "Cyber Security"
    
    country = "Pakistan"
    
    source = "Facebook"
    
    advert = "https://fb.me/21rMG0lv9fHcEpk"
    
    assigned_date = "27 Feb 2024"

    output_file_name = "Pak-Cyber Security leads-14-2-24_Leads_2024-02-13_2024-02-26.xlsx"

    # Excell Sheet Data Normalized:
    processed_data = excell_sheet.process_excel_data(file_path, city, form, country, source, advert, assigned_date)
    
    # Now CRM TASK
    crm_api.clean_leads(processed_data, output_file_name)