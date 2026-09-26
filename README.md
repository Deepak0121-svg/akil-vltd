# VLTD Certificate Generator

A local web application for generating VLTD Fitment Certificates.

---

## Folder Structure

VLTD_Certificate_Generator/

    server.py

    devices.json

    README.md

    data/

    static/
        form.html
        certificate.html
        style.css
        app.js


---

# 1. REQUIREMENTS

Install:

Python 3.11 or newer.

The following Python packages are required:

qrcode

Pillow


---

# 2. INSTALL PYTHON PACKAGES

Open PowerShell.

Go to the project folder.

Example:

cd "D:\VLTD_Certificate_Generator"


Then run:

py -m pip install qrcode pillow


---

# 3. START SERVER

Run:

py server.py


You should see:

VLTD CERTIFICATE GENERATOR

Server running on port 8090

Open on this computer:

http://127.0.0.1:8090


---

# 4. OPEN GENERATOR

Open Chrome.

Go to:

http://127.0.0.1:8090


The certificate generation form will appear.


---

# 5. VEHICLE REGISTRATION NUMBER

The registration number must contain exactly 10 characters.

Example:

TN72DX8035


Allowed:

A-Z

0-9


Examples:

TN72DX8035

TN72AB1234

KL01AA1234


Invalid:

TN72DX803

TN72DX80355

TN-72-DX8035

TN72 DX8035


Lowercase letters are automatically converted to uppercase.


---

# 6. DEVICE DETAILS

Device information is controlled using:

devices.json


Example:

[
    {
        "id": "DEVICE-001",
        "manufacturer": "SRI KRISHNA TECHNOLOGY",
        "model": "JAISON 140",
        "serial": "SRIKJ1012600000734",
        "imei": "868329080038478",
        "iccid": "89917241214029310732"
    }
]


The certificate user cannot manually modify these fields.

To add another device, add another object to devices.json.


---

# 7. CONNECTIVITY

The following values are automatically fixed:

SIM Service Provider:

navspire


SIM Validity:

1 year


The certificate generation user cannot change these values.


---

# 8. QR CODE

Every certificate receives a unique certificate ID.

Example:

A1B2C3D4E5F6


The QR code points to:

/certificate/A1B2C3D4E5F6


When the QR code is scanned, the saved certificate is displayed.


---

# 9. IMPORTANT - PHONE QR SCANNING

If the certificate is generated on a PC and the QR code is scanned using a mobile phone, the QR URL must be reachable from the mobile phone.


For local Wi-Fi testing:

Find the PC IP address:

ipconfig


Example:

IPv4 Address:

192.168.1.20


Then change server.py:

PUBLIC_BASE_URL = "http://192.168.1.20:8090"


Restart the server.


The phone and PC must be connected to the same Wi-Fi network.


Then the QR code can open:

http://192.168.1.20:8090/certificate/XXXXXXXXXXXX


---

# 10. WINDOWS FIREWALL

If the phone cannot open the certificate, allow TCP port 8090 through Windows Firewall.


Run PowerShell as Administrator:

New-NetFirewallRule `
    -DisplayName "VLTD Certificate Generator 8090" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 8090 `
    -Action Allow


---

# 11. PRODUCTION

For actual public certificate verification, use:

HTTPS

A real domain

A proper web server/reverse proxy

Database backups

Authentication for certificate creation


Example:

https://cert.example.com


Then:

PUBLIC_BASE_URL = "https://cert.example.com"


---

# 12. DATABASE

Generated certificates are stored in:

data/certificates.db


The database is automatically created by server.py.


Each certificate contains:

Certificate ID

Vehicle registration number

Vehicle category

Vehicle type

Owner name

District / State

Device details

SIM provider

SIM validity

Installation date

Activation date


---

# 13. CERTIFICATE VERIFICATION

Scanning the QR code opens the certificate stored in the database.

The QR code does not store the complete certificate.

It stores a URL containing the certificate ID.


Example:

https://cert.example.com/certificate/A1B2C3D4E5F6


---

# 14. PRINTING

Open the certificate.

Use:

Ctrl + P


Select:

Paper size: A4

Orientation: Portrait

Margins: None / Default depending on browser

Scale: 100%


The certificate is designed for A4 printing.


---

# IMPORTANT

The fixed compliance wording should only be used where the issuer is authorized to issue that certificate.

The QR code verifies the certificate record stored by this application. It does not independently establish government or authority approval.