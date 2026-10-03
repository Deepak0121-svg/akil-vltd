
document.addEventListener(
    "DOMContentLoaded",
    function () {

        const form =
            document.getElementById(
                "certificateForm"
            );

        const registration =
            document.getElementById(
                "vehicle_registration"
            );

        const serial =
            document.getElementById(
                "device_serial"
            );

        const imei =
            document.getElementById(
                "device_imei"
            );

        const iccid =
            document.getElementById(
                "device_iccid"
            );


        /*
        ========================================================
        VEHICLE REGISTRATION
        EXACTLY 10 ALPHANUMERIC CHARACTERS
        ========================================================
        */

        registration.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                    .replace(
                        /[^a-zA-Z0-9]/g,
                        ""
                    )
                    .toUpperCase()
                    .slice(
                        0,
                        10
                    );

            }
        );


        /*
        ========================================================
        SERIAL NUMBER
        EXACTLY 25 ALPHANUMERIC CHARACTERS
        ========================================================
        */

        serial.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                    .replace(
                        /[^a-zA-Z0-9]/g,
                        ""
                    )
                    .toUpperCase()
                    .slice(
                        0,
                        25
                    );

            }
        );


        /*
        ========================================================
        IMEI NUMBER
        EXACTLY 25 ALPHANUMERIC CHARACTERS
        ========================================================
        */

        imei.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                    .replace(
                        /[^a-zA-Z0-9]/g,
                        ""
                    )
                    .toUpperCase()
                    .slice(
                        0,
                        25
                    );

            }
        );


        /*
        ========================================================
        ICCID NUMBER
        EXACTLY 25 ALPHANUMERIC CHARACTERS
        ========================================================

        Allowed:
        0-9
        A-Z
        a-z

        Example:
        8991430008112624155FABC12

        Length:
        25 characters
        ========================================================
        */

        iccid.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                    .replace(
                        /[^a-zA-Z0-9]/g,
                        ""
                    )
                    .toUpperCase()
                    .slice(
                        0,
                        25
                    );

            }
        );


        /*
        ========================================================
        FORM VALIDATION
        ========================================================
        */

        form.addEventListener(
            "submit",
            function (event) {

                /*
                ------------------------------------------------
                VEHICLE REGISTRATION
                ------------------------------------------------
                */

                const reg =
                    registration.value.trim();


                if (
                    !/^[A-Z0-9]{10}$/.test(
                        reg
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "Vehicle Registration Number must contain exactly 10 letters/numbers."
                    );

                    registration.focus();

                    return;

                }


                /*
                ------------------------------------------------
                DEVICE VALUES
                ------------------------------------------------
                */

                const serialValue =
                    serial.value.trim();


                const imeiValue =
                    imei.value.trim();


                const iccidValue =
                    iccid.value.trim();


                /*
                ------------------------------------------------
                REQUIRED FIELD VALIDATION
                ------------------------------------------------
                */

                if (!serialValue) {

                    event.preventDefault();

                    alert(
                        "Please enter Serial Number."
                    );

                    serial.focus();

                    return;

                }


                if (!imeiValue) {

                    event.preventDefault();

                    alert(
                        "Please enter IMEI Number."
                    );

                    imei.focus();

                    return;

                }


                if (!iccidValue) {

                    event.preventDefault();

                    alert(
                        "Please enter ICCID Number."
                    );

                    iccid.focus();

                    return;

                }


                /*
                ====================================================
                SERIAL NUMBER VALIDATION
                EXACTLY 25 ALPHANUMERIC CHARACTERS
                ====================================================
                */

                if (
                    !/^[A-Z0-9]{25}$/.test(
                        serialValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "Serial Number must contain exactly 25 letters/numbers."
                    );

                    serial.focus();

                    return;

                }


                /*
                ====================================================
                IMEI VALIDATION
                EXACTLY 25 ALPHANUMERIC CHARACTERS
                ====================================================
                */

                if (
                    !/^[A-Z0-9]{25}$/.test(
                        imeiValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "IMEI Number must contain exactly 25 letters/numbers."
                    );

                    imei.focus();

                    return;

                }


                /*
                ====================================================
                ICCID VALIDATION
                EXACTLY 25 ALPHANUMERIC CHARACTERS
                ====================================================
                */

                if (
                    !/^[A-Z0-9]{25}$/.test(
                        iccidValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "ICCID Number must contain exactly 25 letters/numbers."
                    );

                    iccid.focus();

                    return;

                }


                /*
                ====================================================
                ALL VALID
                FORM WILL SUBMIT NORMALLY
                ====================================================
                */

            }
        );

    }
);

