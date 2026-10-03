
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
        IMEI - NUMBERS ONLY
        ========================================================
        */

        imei.addEventListener(
            "input",
            function () {

                this.value =
                    this.value.replace(
                        /[^0-9]/g,
                        ""
                    );

            }
        );


        /*
        ========================================================
        ICCID
        19 DIGITS + OPTIONAL FINAL F
        Example:
        8991430008112624155
        8991430008112624155F
        ========================================================
        */

        iccid.addEventListener(
            "input",
            function () {

                let value =
                    this.value
                    .toUpperCase()
                    .replace(
                        /[^0-9F]/g,
                        ""
                    );


                /*
                ------------------------------------------------
                Keep only the first 19 digits.
                ------------------------------------------------
                */

                let digits =
                    value
                    .replace(
                        /F/g,
                        ""
                    )
                    .slice(
                        0,
                        19
                    );


                /*
                ------------------------------------------------
                F is allowed ONLY at the end.
                ------------------------------------------------
                */

                let hasF =
                    value.endsWith("F");


                this.value =
                    digits +
                    (
                        hasF
                            ? "F"
                            : ""
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
                VEHICLE REGISTRATION VALIDATION
                ------------------------------------------------
                */

                const reg =
                    registration.value.trim();


                if (
                    reg.length !== 10 ||
                    !/^[A-Z0-9]{10}$/.test(reg)
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
                SERIAL NUMBER
                ------------------------------------------------
                */

                const serial =
                    document
                    .getElementById(
                        "device_serial"
                    )
                    .value
                    .trim();


                /*
                ------------------------------------------------
                IMEI
                ------------------------------------------------
                */

                const imeiValue =
                    imei.value.trim();


                /*
                ------------------------------------------------
                ICCID
                ------------------------------------------------
                */

                const iccidValue =
                    iccid.value.trim();


                /*
                ------------------------------------------------
                REQUIRED FIELD VALIDATION
                ------------------------------------------------
                */

                if (!serial) {

                    event.preventDefault();

                    alert(
                        "Please enter Serial Number."
                    );

                    return;

                }


                if (!imeiValue) {

                    event.preventDefault();

                    alert(
                        "Please enter IMEI Number."
                    );

                    return;

                }


                if (!iccidValue) {

                    event.preventDefault();

                    alert(
                        "Please enter ICCID Number."
                    );

                    return;

                }


                /*
                ====================================================
                IMEI VALIDATION
                NUMBERS ONLY
                ====================================================
                */

                if (
                    !/^[0-9]+$/.test(
                        imeiValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "IMEI Number must contain numbers only."
                    );

                    imei.focus();

                    return;

                }


                /*
                ====================================================
                ICCID VALIDATION
                19 DIGITS + OPTIONAL FINAL F
                ====================================================
                */

                if (
                    !/^[0-9]{19}F?$/.test(
                        iccidValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "ICCID Number must contain 19 digits, with an optional final F."
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

