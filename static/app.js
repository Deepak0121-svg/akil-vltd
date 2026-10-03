
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
        ICCID - EXACTLY 19 DIGITS
        ========================================================
        */

        iccid.addEventListener(
            "input",
            function () {

                let value =
                    this.value.replace(
                        /[^0-9]/g,
                        ""
                    );

                this.value =
                    value.slice(
                        0,
                        19
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


                const serial =
                    document
                    .getElementById(
                        "device_serial"
                    )
                    .value
                    .trim();


                const imeiValue =
                    imei.value.trim();


                const iccidValue =
                    iccid.value.trim();


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
                EXACTLY 19 DIGITS
                ====================================================
                */

                if (
                    !/^[0-9]{19}$/.test(
                        iccidValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "ICCID Number must contain exactly 19 digits."
                    );

                    iccid.focus();

                    return;

                }

            }
        );

    }
);
