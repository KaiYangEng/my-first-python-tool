import os
import PySimpleGUI as sg
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

current_dateTime = datetime.now()
units = ""
sampleDetail = ""
date = current_dateTime.date()

# Paths for Europe and USA
measurementPath_Europe = '//Athene/Messungen'
measurementPath_USA = "//Athene/Messungen"
#measurementPath_Europe = 'C:/Users/engkai/OneDrive - cyberTECHNOLOGIES GmbH/Desktop/Evaluation'
#measurementPath_USA = 'C:/Users/engkai/OneDrive - cyberTECHNOLOGIES GmbH/Desktop/Evaluation'
csv_file_path = "//Athene/Messungen/000_Sample-Management/Book3.csv"
#csv_file_path = 'C:/Users/engkai/OneDrive - cyberTECHNOLOGIES GmbH/Desktop/DataAnalysisTool/Features/10_SearchAndCreateFolder/table/Book3.csv'
system = sorted(['CT100', 'CT150', 'Vantage1', 'Vantage2', 'CT300', 'CT350', 'CT350T'])
contact_person =  sorted(['Kai Yang Eng', 'Toni Marko Pesa', 'Tobias Eppeneder','Wolfgang Buxeder','Disha Zanjad','Pooja Baisoya', 'Simon Cannonier','Frank Kemnitzer'])

# Define color themes
frame_bg_color = "#f2f2f2"
highlight_color = "#d1e7dd"

# GUI Layout
layout = [
    [sg.Frame(
        layout=[[sg.Radio('Europe & Asia', 'radio1', default=True, size=(17, 1), key='Europe'),
                 sg.Radio('USA', 'radio1', size=(15, 1), key='USA')]],
        title='Region:', title_color='darkblue', relief=sg.RELIEF_RIDGE, background_color=frame_bg_color)],

    [sg.Frame(
        layout=[
            [sg.T('Date:', size=(15, 1)), sg.In(default_text=date, key='dateInput', size=(29, 200))],
            [sg.T('Company Name:', size=(15, 1)), sg.In(key='company', size=(29, 200))],
            [sg.T('Sample Details:', size=(15, 1)), sg.In(key='sampleDetails', size=(29, 200))],
            [sg.T('Unit (pcs):', size=(15, 1)), sg.In(key='Unit', size=(29, 200))],
        ], title='Customer Information', title_color='darkgreen', relief=sg.RELIEF_GROOVE, background_color=frame_bg_color)],

    [sg.Frame(
        layout=[
            [sg.T('Application:', size=(15, 1)), sg.In(key='application', size=(29, 200))],
            [sg.T('Recipient:', size=(15, 1)), sg.Combo(contact_person, key='Recipient', size=(17, 200))],
            [sg.T('Measuring Person:', size=(15, 1)), sg.Combo(contact_person, key='measurePerson', size=(17, 200))],
            [sg.T('System:', size=(15, 1)), sg.Combo(system, size=(17, 1), key='systemCOMBO')],
            [sg.T('Sensor:', size=(15, 1)), sg.In(key='sensor', size=(17, 200))],
        ], title='Application Details', title_color='darkred', relief=sg.RELIEF_SOLID, background_color=highlight_color)],

    [sg.Button('OK', button_color=('white', 'green')), sg.Button('Plot'), sg.Exit(button_color=('white', 'red'))]
]

window = sg.Window("Sample Administration Vers1.6", layout, background_color='#e0e0e0')
def plot_entries(csv_path):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path)

        # Ensure the date column is in datetime format
        df['Eingangsdatum (yyyy-mm-dd)'] = pd.to_datetime(df['Eingangsdatum (yyyy-mm-dd)'], errors='coerce')

        # Drop rows where the date is invalid (NaT)
        df = df.dropna(subset=['Eingangsdatum (yyyy-mm-dd)'])

        # Create a new column for year and month
        df['Year'] = df['Eingangsdatum (yyyy-mm-dd)'].dt.year
        df['Month'] = df['Eingangsdatum (yyyy-mm-dd)'].dt.to_period('M')

        # Plot yearly entries
        yearly_counts = df['Year'].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        yearly_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of Entries Received Yearly')
        plt.xlabel('Year')
        plt.ylabel('Number of Entries')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Plot monthly entries
        monthly_counts = df['Month'].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        monthly_counts.plot(kind='line', marker='o', color='orange')
        plt.title('Number of Entries Received Monthly')
        plt.xlabel('Month')
        plt.ylabel('Number of Entries')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        sg.popup(f"Error generating plots: {e}", title="Error")


# Event Loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # Determine the measurement path based on region selection
    if values['Europe']:
        current_path = measurementPath_Europe
    elif values['USA']:
        current_path = measurementPath_USA

    if event == 'OK':
        # Gather user input
        companyName = values.get('company', '').strip()
        units = values.get('Unit', '').strip()
        sampleDetail = values.get('sampleDetails', '').strip()
        application = values.get('application', '').strip()
        system_selected = values.get('systemCOMBO', '').strip()
        sensor = values.get('sensor', '').strip()
        entry_date = values.get('dateInput', '').strip()

        # Validate input
        if not companyName or not units or not sampleDetail:
            sg.popup("Please fill all fields.", title="Error")
            continue

        # Check if company folder exists
        companyFolderPath = os.path.join(current_path, companyName)
        if not os.path.exists(companyFolderPath):
            # Create the company folder if it does not exist
            os.makedirs(companyFolderPath, exist_ok=True)

        # Generate folder name
        folderName = f"{entry_date} {units}x {sampleDetail}"

        # Create folderName inside company folder
        mainFolderPath = os.path.join(companyFolderPath, folderName)
        try:
            os.makedirs(mainFolderPath, exist_ok=True)

            # Create subfolders with specific names
            subFolderNames = ['0_Received', '1_Measurement', '2_Returned']
            for subFolderName in subFolderNames:
                subFolderPath = os.path.join(mainFolderPath, subFolderName)
                os.makedirs(subFolderPath, exist_ok=True)

            # Append a new row to the CSV file
            new_row = {
                "Eingangsdatum (yyyy-mm-dd)": date,
                "Kunde": companyName,
                "Probename": f"{sampleDetail} ({units}x)",
                "Ansprechpartner": values.get('Recipient', 'TBA'),
                "Benutzer": values.get('measurePerson', 'TBA'),
                "Status": "N",
                "Liefertermin (yyyy-mm-dd)": "TBA",
                "System": values.get('systemCOMBO', 'TBA'),
                "Sensor": values.get('sensor', 'TBA'),
                "Lagerort": "TBA",
                "Messung/Analyse": "TBA",
                "Ergebnisse Serverordner": mainFolderPath,
                "Bemerkungen": "TBA"
            }

            # Read the existing CSV and append the new row
            if os.path.exists(csv_file_path):
                # Read the existing CSV
                df = pd.read_csv(csv_file_path)

                # Check for duplicates
                is_duplicate = (
                        (df["Kunde"] == new_row["Kunde"]) &
                        (df["Probename"] == new_row["Probename"]) &
                        (df["Ergebnisse Serverordner"] == new_row["Ergebnisse Serverordner"])
                )
                if is_duplicate.any():
                    sg.popup("Duplicate entry found. The details have already been added.", title="Duplicate Entry")
                else:
                    # Append the new row if no duplicate is found
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv(csv_file_path, index=False)
                    sg.popup(f"Folder and subfolders created successfully:\n{mainFolderPath}\n\nDetails added to CSV.", title="Success")
            else:
                # If the file does not exist, create a new DataFrame and save it
                df = pd.DataFrame([new_row])
                df.to_csv(csv_file_path, index=False)
                sg.popup(f"Folder and subfolders created successfully:\n{mainFolderPath}\n\nNew CSV file created with details.", title="Success")
        except Exception as e:
            sg.popup(f"Error creating folders or updating CSV:\n{e}", title="Error")
    if event == 'Plot':
        plot_entries(csv_file_path)
# Close the window
window.close()