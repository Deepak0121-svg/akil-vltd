
import json
import os
import sqlite3
import uuid

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, quote, parse_qs
from io import BytesIO

import qrcode


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)

DB = os.path.join(
    DATA_DIR,
    "certificates.db"
)

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
# FIXED VLTD DETAILS
# ============================================================

DEVICE_MANUFACTURER = "AKIL ENTERPRISES"

DEVICE_MODEL = "AKEEL 140"

SIM_PROVIDER = "Navspire"

SIM_VALIDITY = "1 Year"


# ============================================================
# CREATE DATA DIRECTORY
# ============================================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


# ============================================================
# DATABASE
# ============================================================

def get_db():

    con = sqlite3.connect(
        DB
    )

    con.row_factory = sqlite3.Row

    con.execute(
        """
        CREATE TABLE IF NOT EXISTS certificates
        (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    con.commit()

    return con


# ============================================================
# STATIC FILE READER
# ============================================================

def read_static_file(
    filename
):

    path = os.path.join(
        STATIC_DIR,
        filename
    )

    with open(
        path,
        "rb"
    ) as f:

        return f.read()


# ============================================================
# HTTP RESPONSE
# ============================================================

def send_response(
    handler,
    status_code,
    content_type,
    body
):

    handler.send_response(
        status_code
    )

    handler.send_header(
        "Content-Type",
        content_type
    )

    handler.send_header(
        "Cache-Control",
        "no-store"
    )

    handler.send_header(
        "Content-Length",
        str(len(body))
    )

    handler.end_headers()

    handler.wfile.write(
        body
    )


# ============================================================
# POST FORM PARSER
# ============================================================

def parse_post(
    handler
):

    content_length = int(
        handler.headers.get(
            "Content-Length",
            "0"
        )
    )

    raw = handler.rfile.read(
        content_length
    ).decode(
        "utf-8"
    )

    values = parse_qs(
        raw
    )

    return {
        key: value[0]
        for key, value in values.items()
    }


# ============================================================
# ALPHANUMERIC VALIDATOR
# ============================================================
#
# Allows:
#
#     A-Z
#     a-z
#     0-9
#
# Any length.
#
# No spaces.
# No special characters.
#
# IMPORTANT:
# There is NO 10-character restriction.
# ============================================================

def is_alphanumeric(
    value
):

    if not value:

        return False

    return (
        value.isascii()
        and value.isalnum()
    )


# ============================================================
# CLEAN FORM VALUE
# ============================================================

def clean_value(
    form,
    field
):

    return (
        form.get(
            field,
            ""
        )
        .strip()
    )


# ============================================================
# REQUEST HANDLER
# ============================================================

class Handler(
    BaseHTTPRequestHandler
):

    # ========================================================
    # GET
    # ========================================================

    def do_GET(
        self
    ):

        parsed = urlparse(
            self.path
        )

        path = parsed.path


        # ====================================================
        # MAIN FORM
        # ====================================================

        if path == "/":

            body = read_static_file(
                "form.html"
            )

            send_response(
                self,
                200,
                "text/html; charset=utf-8",
                body
            )

            return


        # ====================================================
        # CSS
        # ====================================================

        if path == "/static/style.css":

            body = read_static_file(
                "style.css"
            )

            send_response(
                self,
                200,
                "text/css; charset=utf-8",
                body
            )

            return


        # ====================================================
        # JAVASCRIPT
        # ====================================================

        if path == "/static/app.js":

            body = read_static_file(
                "app.js"
            )

            send_response(
                self,
                200,
                "application/javascript; charset=utf-8",
                body
            )

            return


        # ====================================================
        # CERTIFICATE
        # ====================================================

        if path.startswith(
            "/certificate/"
        ):

            certificate_id = path.rsplit(
                "/",
                1
            )[-1]


            con = get_db()


            row = con.execute(
                """
                SELECT data
                FROM certificates
                WHERE id = ?
                """,
                (
                    certificate_id,
                )
            ).fetchone()


            con.close()


            if not row:

                send_response(
                    self,
                    404,
                    "text/plain; charset=utf-8",
                    b"Certificate not found"
                )

                return


            certificate_data = json.loads(
                row["data"]
            )


            page = read_static_file(
                "certificate.html"
            ).decode(
                "utf-8"
            )


            json_data = json.dumps(
                certificate_data,
                ensure_ascii=False
            )


            # Prevent </script> problems

            json_data = json_data.replace(
                "</",
                "<\\/"
            )


            page = page.replace(
                "__CERT_DATA__",
                json_data
            )


            send_response(
                self,
                200,
                "text/html; charset=utf-8",
                page.encode(
                    "utf-8"
                )
            )

            return


        # ====================================================
        # QR CODE
        # ====================================================

        if path.startswith(
            "/qr/"
        ):

            certificate_id = path.rsplit(
                "/",
                1
            )[-1]


            con = get_db()


            row = con.execute(
                """
                SELECT id
                FROM certificates
                WHERE id = ?
                """,
                (
                    certificate_id,
                )
            ).fetchone()


            con.close()


            if not row:

                send_response(
                    self,
                    404,
                    "text/plain; charset=utf-8",
                    b"Certificate not found"
                )

                return


            target_url = (
                PUBLIC_BASE_URL.rstrip("/")
                + "/certificate/"
                + quote(
                    certificate_id
                )
            )


            qr_image = qrcode.make(
                target_url
            )


            buffer = BytesIO()


            qr_image.save(
                buffer,
                format="PNG"
            )


            send_response(
                self,
                200,
                "image/png",
                buffer.getvalue()
            )

            return


        # ====================================================
        # 404
        # ====================================================

        send_response(
            self,
            404,
            "text/plain",
            b"Not Found"
        )


    # ========================================================
    # POST
    # ========================================================

    def do_POST(
        self
    ):

        if self.path != "/create":

            send_response(
                self,
                404,
                "text/plain",
                b"Not Found"
            )

            return


        form = parse_post(
            self
        )


        # ====================================================
        # VEHICLE REGISTRATION
        # ====================================================

        registration_number = (
            clean_value(
                form,
                "vehicle_registration"
            )
            .upper()
        )


        # ====================================================
        # VEHICLE REGISTRATION VALIDATION
        #
        # NO 10 CHARACTER LIMIT
        #
        # Any length is accepted.
        #
        # Only:
        #     A-Z
        #     0-9
        #
        # are allowed.
        # ====================================================

        if not is_alphanumeric(
            registration_number
        ):

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                (
                    b"Vehicle Registration Number must contain "
                    b"only letters and numbers."
                )
            )

            return


        # ====================================================
        # VEHICLE FIELDS
        # ====================================================

        vehicle_category = clean_value(
            form,
            "vehicle_category"
        )

        vehicle_type = clean_value(
            form,
            "vehicle_type"
        )

        owner_name = clean_value(
            form,
            "owner_name"
        )

        district_state = clean_value(
            form,
            "district_state"
        )

        installation_date = clean_value(
            form,
            "installation_date"
        )

        activation_date = clean_value(
            form,
            "activation_date"
        )


        # ====================================================
        # REQUIRED VEHICLE VALIDATION
        # ====================================================

        required_vehicle_fields = {

            "Vehicle Category":
                vehicle_category,

            "Vehicle Type":
                vehicle_type,

            "Owner Name":
                owner_name,

            "District / State":
                district_state,

            "Date of Installation":
                installation_date,

            "Date of Activation":
                activation_date
        }


        for field_name, field_value in required_vehicle_fields.items():

            if not field_value:

                send_response(
                    self,
                    400,
                    "text/plain; charset=utf-8",
                    (
                        f"{field_name} is required."
                    ).encode(
                        "utf-8"
                    )
                )

                return


        # ====================================================
        # DEVICE INFORMATION
        # ====================================================

        device_serial = (
            clean_value(
                form,
                "device_serial"
            )
            .upper()
        )

        device_imei = (
            clean_value(
                form,
                "device_imei"
            )
            .upper()
        )

        device_iccid = (
            clean_value(
                form,
                "device_iccid"
            )
            .upper()
        )


        # ====================================================
        # REQUIRED DEVICE VALIDATION
        # ====================================================

        if not device_serial:

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                b"Device Serial Number is required."
            )

            return


        if not device_imei:

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                b"IMEI Number is required."
            )

            return


        if not device_iccid:

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                b"ICCID Number is required."
            )

            return


        # ====================================================
        # SERIAL NUMBER
        # ANY LENGTH - ALPHANUMERIC ONLY
        # ====================================================

        if not is_alphanumeric(
            device_serial
        ):

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                (
                    b"Serial Number must contain "
                    b"only letters and numbers."
                )
            )

            return


        # ====================================================
        # IMEI NUMBER
        # ANY LENGTH - ALPHANUMERIC ONLY
        # ====================================================

        if not is_alphanumeric(
            device_imei
        ):

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                (
                    b"IMEI Number must contain "
                    b"only letters and numbers."
                )
            )

            return


        # ====================================================
        # ICCID NUMBER
        # ANY LENGTH - ALPHANUMERIC ONLY
        # ====================================================

        if not is_alphanumeric(
            device_iccid
        ):

            send_response(
                self,
                400,
                "text/plain; charset=utf-8",
                (
                    b"ICCID Number must contain "
                    b"only letters and numbers."
                )
            )

            return


        # ====================================================
        # CERTIFICATE ID
        # ====================================================

        certificate_id = (
            uuid.uuid4()
            .hex[:12]
            .upper()
        )


        # ====================================================
        # CERTIFICATE DATA
        # ====================================================

        certificate_data = {

            # ==================================================
            # VEHICLE DETAILS
            # ==================================================

            "vehicle_registration":
                registration_number,

            "vehicle_category":
                vehicle_category,

            "vehicle_type":
                vehicle_type,

            "owner_name":
                owner_name,

            "district_state":
                district_state,


            # ==================================================
            # EXPLICIT CERTIFICATE DISPLAY FIELDS
            # ==================================================

            "certificate_vehicle_registration":
                registration_number,

            "certificate_vehicle_category":
                vehicle_category,

            "certificate_vehicle_type":
                vehicle_type,

            "certificate_owner_name":
                owner_name,

            "certificate_district_state":
                district_state,


            # ==================================================
            # VLTD DEVICE
            # ==================================================

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


            # ==================================================
            # FLAT DEVICE FIELDS
            # ==================================================

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


            # ==================================================
            # SIM
            # ==================================================

            "sim_provider":
                SIM_PROVIDER,

            "sim_validity":
                SIM_VALIDITY,


            # ==================================================
            # DATES
            # ==================================================

            "installation_date":
                installation_date,

            "activation_date":
                activation_date,


            # ==================================================
            # EXPLICIT CERTIFICATE DATE FIELDS
            # ==================================================

            "certificate_installation_date":
                installation_date,

            "certificate_activation_date":
                activation_date,


            # ==================================================
            # CERTIFICATE ID
            # ==================================================

            "certificate_id":
                certificate_id
        }


        # ====================================================
        # SAVE CERTIFICATE
        # ====================================================

        con = get_db()


        con.execute(
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

                datetime.now().isoformat(
                    timespec="seconds"
                )
            )
        )


        con.commit()

        con.close()


        # ====================================================
        # REDIRECT TO CERTIFICATE
        # ====================================================

        self.send_response(
            303
        )

        self.send_header(
            "Location",
            "/certificate/"
            + certificate_id
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.end_headers()


    # ========================================================
    # SERVER LOG
    # ========================================================

    def log_message(
        self,
        format,
        *args
    ):

        print(
            "[%s] %s"
            % (
                self.log_date_time_string(),
                format % args
            )
        )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    get_db().close()


    print()

    print(
        "=" * 65
    )

    print(
        "VLTD CERTIFICATE GENERATOR"
    )

    print(
        "=" * 65
    )

    print()


    print(
        "Manufacturer        :",
        DEVICE_MANUFACTURER
    )

    print(
        "Device Model        :",
        DEVICE_MODEL
    )

    print(
        "SIM Provider        :",
        SIM_PROVIDER
    )

    print()


    print(
        "Server Port         :",
        PORT
    )

    print()


    print(
        "Open on this computer:"
    )

    print(
        f"http://127.0.0.1:{PORT}"
    )

    print()


    print(
        "QR Base URL:"
    )

    print(
        PUBLIC_BASE_URL
    )

    print()


    print(
        "Vehicle Registration Format:"
    )

    print(
        "Any length - Alphanumeric only"
    )

    print()


    print(
        "Device Number Format:"
    )

    print(
        "Any length - Alphanumeric only"
    )

    print()


    print(
        "Press CTRL+C to stop."
    )

    print()


    print(
        "=" * 65
    )

    print()


    server = ThreadingHTTPServer(
        (
            HOST,
            PORT
        ),
        Handler
    )


 
