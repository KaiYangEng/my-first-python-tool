# my-first-python-tool
📂 Sample Administration Tool
A Python GUI tool to automate folder creation for sample management in a company server.

Python PySimpleGUI Pandas

📌 Overview
This tool simplifies the process of organizing incoming customer samples by:
✅ Automatically creating folders in the company server (//Athene/Messungen/).
✅ Storing metadata (company name, sample details, units, etc.) in a CSV file.
✅ Generating plots to visualize sample entries over time.

============================================================================================
⚙️ Features
1. User-Friendly GUI (PySimpleGUI)
  Input fields for:
    - Company name, sample details, units.
    - Application, measuring person, system type.
  Region selection (Europe/Asia or USA).

2. Automated Folder Structure
  Creates a parent folder for the company (if it doesn’t exist).

  Generates subfolders:
  📂 [Date]_[Units]x_[SampleName]  
    ├── 0_Received  
    ├── 1_Measurement  
    └── 2_Returned  
    
3. CSV Logging
  Appends sample details to Book3.csv (with duplicate checks).

4. Data Visualization
  Click "Plot" to generate:
    📊 Yearly/Monthly trends of sample entries (using Matplotlib).

============================================================================================
🚀 Installation
1. Prerequisites:
  - Python 3.8+
  - Required libraries:
      bash
      pip install PySimpleGUI pandas matplotlib
    
2. Run the Script:
  bash
  python sample_administration.py

============================================================================================
🖥️ Usage
1. Fill in the form:
  - Region: Select Europe/Asia or USA.
  - Customer Info: Company name, sample details, units.
  - Application Details: System, sensor, recipient, etc.

2. Click "OK" to:
  - Create folders on the server.
  - Log data to CSV.

3. Click "Plot" to visualize historical entries.

============================================================================================
📂 Folder Structure Example
//Athene/Messungen/  
└── Company_Name/  
    └── 2024-05-20_5x_Sample123/  
        ├── 0_Received/  
        ├── 1_Measurement/  
        └── 2_Returned/  
📝 CSV Fields
Column (German)	            Description	                Example
Eingangsdatum	              Entry date (YYYY-MM-DD)	    2024-05-20
Kunde	                      Company name	              ABC Corp
Probename	                  Sample details + units	    Sample123 (5x)
Ergebnisse Serverordner	    Folder path	                //Athene/...

============================================================================================
⚠️ Notes
- Server Paths: Modify measurementPath_Europe/USA and csv_file_path in the script if needed.
- Backdating: Commit dates can be faked (see Git tricks but push dates remain accurate.
- Ethical Use: Avoid misrepresenting data in the CSV/folders.

============================================================================================
📜 License
MIT License - Free for commercial and personal use.

============================================================================================
🔗 How to Contribute
Fork this repository.

Submit a pull request for improvements (e.g., error handling, UI upgrades).
