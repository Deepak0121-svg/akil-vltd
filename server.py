import os
import json
import uuid
import sqlite3
import qrcode

from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"

DB = DATA_DIR / "certificates.db"


# Create required folders
DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

STATIC_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SERVER CONFIGURATION
# ============================================================

HOST = "0.0.0.0"

PORT = int(
    os.environ.get(
        "PORT",
        "8090"
    )
)


# ============================================================
# PUBLIC URL
# ============================================================

PUBLIC_BASE_URL = "https://akil-vltd.onrender.com"


# ============================================================
# FIXED DEVICE INFORMATION
# ============================================================

DEVICE_MANUFACTURER = "AKIL ENTERPRISES"

DEVICE_MODEL = "AKEEL 140"

SIM_PROVIDER = "Navspire"

SIM_VALIDITY = "1 Year"


# ============================================================
# DATABASE
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DB
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS certificates
        (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# VALIDATION HELPERS
# ============================================================

def is_alphanumeric(value):
    """
    Accepts ANY length.

    Allowed:
        A-Z
        a-z
        0-9

    No minimum/maximum length.

    Examples accepted:
        123
        ABC123
        8991430008112624155
        8991430008112624155F
        ABC123XYZ987654321

    Examples rejected:
        empty
        ABC 123
        ABC-123
        ABC@123
    """

    if not value:
        return False

    return (
        value.isascii()
        and value.isalnum()
    )


def is_vehicle_registration(value):
    """
    Vehicle registration must contain
    exactly 10 alphanumeric characters.
    """

    if not value:
        return False

    if not value.isascii():
        return False

    if not value.isalnum():
        return False

    return len(value) == 10


# ============================================================
# FORM VALUE HELPER
# ============================================================

def clean_value(value):
    """
    Convert None to empty string and remove
    leading/trailing spaces.
    """

    if value is None:
        return ""

    return str(value).strip()


# ============================================================
# HTML FILE LOADER
# ============================================================

def load_file(filename):

    file_path = STATIC_DIR / filename

    if not file_path.exists():

        return None

    return file_path.read_text(
        encoding="utf-8"
    )


# ============================================================
# CERTIFICATE ID
# ============================================================

def generate_certificate_id():

    return uuid.uuid4().hex[:12].upper()


# ============================================================
# CURRENT TIME
# ============================================================

def current_timestamp():

    return datetime.now(
        timezone.utc
    ).isoformat()


# ============================================================
# SAVE CERTIFICATE
# ============================================================

def save_certificate(
    certificate_id,
    certificate_data
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO certificates
        (
            id,
            data,
            created_at
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,
        (
            certificate_id,
            json.dumps(
                certificate_data,
                ensure_ascii=False
            ),
            current_timestamp()
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# LOAD CERTIFICATE
# ============================================================

def load_certificate(
    certificate_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            data
        FROM certificates
        WHERE id = ?
        """,
        (
            certificate_id,
        )
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    try:

        return json.loads(
            row["data"]
        )

    except Exception:

        return None


# ============================================================
# SEND RESPONSE
# ============================================================

class Handler(
    BaseHTTPRequestHandler
):


    # --------------------------------------------------------
    # COMMON RESPONSE
    # --------------------------------------------------------

    def send_text(
        self,
        content,
        status=200,
        content_type="text/html; charset=utf-8"
    ):

        if isinstance(
            content,
            str
        ):

            content = content.encode(
                "utf-8"
            )

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            content_type
        )

        self.send_header(
            "Content-Length",
            str(len(content))
        )

        self.end_headers()

        self.wfile.write(
            content
        )


    # --------------------------------------------------------
    # REDIRECT
    # --------------------------------------------------------

    def redirect(
        self,
        location
    ):

        self.send_response(
            303
        )

        self.send_header(
            "Location",
            location
        )

        self.end_headers()


    # --------------------------------------------------------
    # 404
    # --------------------------------------------------------

    def not_found(self):

        self.send_text(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>404</title>
            </head>
            <body>
                <h1>404 - Not Found</h1>
            </body>
            </html>
            """,
            status=404
        )


    # --------------------------------------------------------
    # SERVER ERROR
    # --------------------------------------------------------

    def server_error(
        self,
        message
    ):

        self.send_text(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Server Error</title>
            </head>
            <body>
                <h1>Server Error</h1>
                <p>{message}</p>
            </body>
            </html>
            """,
            status=500
        )


    # ========================================================
    # GET
    # ========================================================

    def do_GET(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path


        # ----------------------------------------------------
        # HOME PAGE
        # ----------------------------------------------------

        if path == "/":

            html = load_file(
                "form.html"
            )

            if html is None:

                self.not_found()

                return

            self.send_text(
                html
            )

            return


        # ----------------------------------------------------
        # STYLE CSS
        # ----------------------------------------------------

        if path == "/static/style.css":

            css = load_file(
                "style.css"
            )

            if css is None:

                self.not_found()

                return

            self.send_text(
                css,
                content_type="text/css; charset=utf-8"
            )

            return


        # ----------------------------------------------------
        # APP JS
        # ----------------------------------------------------

        if path == "/static/app.js":

            js = load_file(
                "app.js"
            )

            if js is None:

                self.not_found()

                return

            self.send_text(
                js,
                content_type="application/javascript; charset=utf-8"
            )

            return


        # ----------------------------------------------------
        # CERTIFICATE PAGE
        #
        # /certificate/XXXXXXXXXXXX
        # ----------------------------------------------------

        if path.startswith(
            "/certificate/"
        ):

            certificate_id = unquote(
                path[
                    len("/certificate/"):
                ]
            ).strip()

            if not certificate_id:

                self.not_found()

                return

            certificate_data = load_certificate(
                certificate_id
            )

            if certificate_data is None:

                self.not_found()

                return

            certificate_html = load_file(
                "certificate.html"
            )

            if certificate_html is None:

                self.not_found()

                return

            certificate_json = json.dumps(
                certificate_data,
                ensure_ascii=False
            )

            certificate_html = certificate_html.replace(
                "__CERT_DATA__",
                certificate_json
            )

            self.send_text(
                certificate_html
            )

            return


        # ----------------------------------------------------
        # QR CODE
        #
        # /qr/XXXXXXXXXXXX
        # ----------------------------------------------------

        if path.startswith(
            "/qr/"
        ):

            certificate_id = unquote(
                path[
                    len("/qr/"):
                ]
            ).strip()

            if not certificate_id:

                self.not_found()

                return

            certificate_data = load_certificate(
                certificate_id
            )

            if certificate_data is None:

                self.not_found()

                return

            verification_url = (
                PUBLIC_BASE_URL
                + "/certificate/"
                + certificate_id
            )

            try:

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=4
                )

                qr.add_data(
                    verification_url
                )

                qr.make(
                    fit=True
                )

                image = qr.make_image()

                from io import BytesIO

                output = BytesIO()

                image.save(
                    output,
                    format="PNG"
                )

                png_data = output.getvalue()

                self.send_text(
                    png_data,
                    content_type="image/png"
                )

                return

            except Exception as error:

                self.server_error(
                    str(error)
                )

                return


        # ----------------------------------------------------
        # UNKNOWN PATH
        # ----------------------------------------------------

        self.not_found()


    # ========================================================
    # POST
    # ========================================================

    def do_POST(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path


        # ----------------------------------------------------
        # CREATE CERTIFICATE
        # ----------------------------------------------------

        if path != "/create":

            self.not_found()

            return


        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

        except ValueError:

            content_length = 0


        if content_length <= 0:

            self.send_text(
                "Invalid form submission.",
                status=400
            )

            return


        try:

            body = self.rfile.read(
                content_length
            )

            body_text = body.decode(
                "utf-8"
            )

            from urllib.parse import parse_qs

            form = parse_qs(
                body_text,
                keep_blank_values=True
            )

        except Exception as error:

            self.send_text(
                f"Unable to read form: {error}",
                status=400
            )

            return


        # ====================================================
        # GET FORM VALUE
        # ====================================================

        def get_form_value(
            name
        ):

            values = form.get(
                name,
                [""]
            )

            if not values:

                return ""

            return clean_value(
                values[0]
            )


        # ====================================================
        # VEHICLE DETAILS
        # ====================================================

        vehicle_registration = (
            get_form_value(
                "vehicle_registration"
            )
            .upper()
        )

        vehicle_category = get_form_value(
            "vehicle_category"
        )

        vehicle_type = get_form_value(
            "vehicle_type"
        )

        owner_name = get_form_value(
            "owner_name"
        )

        district_state = get_form_value(
            "district_state"
        )

        installation_date = get_form_value(
            "installation_date"
        )

        activation_date = get_form_value(
            "activation_date"
        )


        # ====================================================
        # DEVICE DETAILS
        # ====================================================

        device_serial = (
            get_form_value(
                "device_serial"
            )
            .upper()
        )

        device_imei = (
            get_form_value(
                "device_imei"
            )
            .upper()
        )

        device_iccid = (
            get_form_value(
                "device_iccid"
            )
            .upper()
        )


        # ====================================================
        # VEHICLE REGISTRATION VALIDATION
        # EXACTLY 10 CHARACTERS
        # ====================================================

        if not is_vehicle_registration(
            vehicle_registration
        ):

            self.send_text(
                """
                Vehicle Registration Number
                must contain exactly 10
                letters/numbers.
                """,
                status=400
            )

            return


        # ====================================================
        # REQUIRED VEHICLE FIELDS
        # ====================================================

        required_fields = {

            "Vehicle Category":
                vehicle_category,

            "Vehicle Type":
                vehicle_type,

            "Owner Name":
                owner_name,

            "District / State":
                district_state,

            "Installation Date":
                installation_date,

            "Activation Date":
                activation_date
        }


        for field_name, value in required_fields.items():

            if not value:

                self.send_text(
                    f"""
                    {field_name} is required.
                    """,
                    status=400
                )

                return


        # ====================================================
        # DEVICE FIELD REQUIRED VALIDATION
        # ====================================================

        if not device_serial:

            self.send_text(
                "Please enter Serial Number.",
                status=400
            )

            return


        if not device_imei:

            self.send_text(
                "Please enter IMEI Number.",
                status=400
            )

            return


        if not device_iccid:

            self.send_text(
                "Please enter ICCID Number.",
                status=400
            )

            return


        # ====================================================
        # DEVICE SERIAL VALIDATION
        #
        # IMPORTANT:
        # NO 25 CHARACTER LIMIT
        # ====================================================

        if not is_alphanumeric(
            device_serial
        ):

            self.send_text(
                "Serial Number must contain only letters and numbers.",
                status=400
            )

            return


        # ====================================================
        # IMEI VALIDATION
        #
        # IMPORTANT:
        # NO 25 CHARACTER LIMIT
        # ====================================================

        if not is_alphanumeric(
            device_imei
        ):

            self.send_text(
                "IMEI Number must contain only letters and numbers.",
                status=400
            )

            return


        # ====================================================
        # ICCID VALIDATION
        #
        # IMPORTANT:
        # NO 25 CHARACTER LIMIT
        # ====================================================

        if not is_alphanumeric(
            device_iccid
        ):

            self.send_text(
                "ICCID Number must contain only letters and numbers.",
                status=400
            )

            return


        # ====================================================
        # GENERATE CERTIFICATE ID
        # ====================================================

        certificate_id = generate_certificate_id()


        # ====================================================
        # CERTIFICATE DATA
        # ====================================================

        certificate_data = {

            # -----------------------------------------------
            # CERTIFICATE
            # -----------------------------------------------

            "certificate_id":
                certificate_id,

            "created_at":
                current_timestamp(),


            # -----------------------------------------------
            # VEHICLE
            # -----------------------------------------------

            "vehicle": {

                "registration":
                    vehicle_registration,

                "category":
                    vehicle_category,

                "type":
                    vehicle_type,

                "owner_name":
                    owner_name,

                "district_state":
                    district_state,

                "installation_date":
                    installation_date,

                "activation_date":
                    activation_date
            },


            # -----------------------------------------------
            # DEVICE
            # -----------------------------------------------

            "device": {

                "manufacturer":
                    DEVICE_MANUFACTURER,

                "model":
                    DEVICE_MODEL,

                "serial":
                    device_serial,

                "imei":
                    device_imei,

                "iccid":
                    device_iccid
            },


            # -----------------------------------------------
            # FLAT DEVICE FIELDS
            #
            # Kept for compatibility with existing
            # certificate.html / JavaScript.
            # -----------------------------------------------

            "device_manufacturer":
                DEVICE_MANUFACTURER,

            "device_model":
                DEVICE_MODEL,

            "device_serial":
                device_serial,

            "device_imei":
                device_imei,

            "device_iccid":
                device_iccid,


            # -----------------------------------------------
            # SIM
            # -----------------------------------------------

            "sim_provider":
                SIM_PROVIDER,

            "sim_validity":
                SIM_VALIDITY,


            # -----------------------------------------------
            # VERIFICATION URL
            # -----------------------------------------------

            "verification_url":
                (
                    PUBLIC_BASE_URL
                    + "/certificate/"
                    + certificate_id
                )
        }


        # ====================================================
        # SAVE TO DATABASE
        # ====================================================

        try:

            save_certificate(
                certificate_id,
                certificate_data
            )

        except Exception as error:

            self.server_error(
                str(error)
            )

            return


        # ====================================================
        # REDIRECT TO CERTIFICATE
        # ====================================================

        self.redirect(
            "/certificate/"
            + certificate_id
        )


    # ========================================================
    # LOG
    # ========================================================

    def log_message(
        self,
        format,
        *args
    ):

        print(
            "[SERVER]",
            format % args
        )


# ============================================================
# START SERVER
# ============================================================

def main():

    init_database()

    server = ThreadingHTTPServer(
        (
            HOST,
            PORT
        ),
        Handler
    )

    print(
        ""
    )

    print(
        "=============================================="
    )

    print(
        " VLTD CERTIFICATE SERVER"
    )

    print(
        "=============================================="
    )

    print(
        f" Host : {HOST}"
    )

    print(
        f" Port : {PORT}"
    )

    print(
        f" URL  : http://localhost:{PORT}"
    )

    print(
        "=============================================="
    )

    print(
        "Device Serial / IMEI / ICCID:"
    )

    print(
        "NO 25 CHARACTER LIMIT"
    )

    print(
        "ANY LENGTH ALPHANUMERIC VALUE ACCEPTED"
    )

    print(
        "=============================================="
    )

    print(
        ""
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nServer stopped."
        )

    finally:

        server.server_close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()