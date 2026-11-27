"""
Download the ENIGH 2024 microdata (INEGI) into data/raw/.

Raw data are not committed (see .gitignore).

INSTRUCTIONS FOR MANUAL DOWNLOAD:
1. Go to: https://www.inegi.org.mx/programas/enigh/nc/2024/#microdatos
2. Scroll down to "Principales variables por hogar (concentradohogar.*)".
3. Click on "Descargar" for the "CSV" format.
4. Extract the downloaded ZIP file.
5. Move the extracted file () into your `data/raw/` folder.

The analysis scripts (01_load.py) expect the file `concentradohogar.csv` to be inside `data/raw/`.
"""
# No download code here because the URL is requires user interaction.