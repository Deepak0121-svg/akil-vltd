
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
        ANY LENGTH - ALPHANUMERIC ONLY
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
                    .toUpperCase();

            }
        );


        /*
        ========================================================
        DEVICE FIELD CLEANER
        SERIAL / IMEI / ICCID
        ANY LENGTH - ALPHANUMERIC ONLY
        ========================================================
        */

        function cleanDeviceField(
            field
        ) {

            field.addEventListener(
                "input",
                function () {

                    this.value =
                        this.value
                        .replace(
                            /[^a-zA-Z0-9]/g,
                            ""
                        )
                        .toUpperCase();

                }
            );

        }


        /*
        ========================================================
        APPLY DEVICE CLEANER
        ========================================================
        */

        cleanDeviceField(
            serial
        );

        cleanDeviceField(
            imei
        );

        cleanDeviceField(
            iccid
        );


        /*
        ========================================================
        FORM SUBMIT VALIDATION
        ========================================================
        */

        form.addEventListener(
            "submit",
            function (event) {


                /*
                ------------------------------------------------
                VEHICLE REGISTRATION
                ANY LENGTH
                ALPHANUMERIC ONLY
                ------------------------------------------------
                */

                const reg =
                    registration.value.trim();


                if (
                    !/^[A-Z0-9]+$/.test(
                        reg
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "Vehicle Registration Number must contain only letters and numbers."
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
                SERIAL REQUIRED
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


                /*
                ------------------------------------------------
                IMEI REQUIRED
                ------------------------------------------------
                */

                if (!imeiValue) {

                    event.preventDefault();

                    alert(
                        "Please enter IMEI Number."
                    );

                    imei.focus();

                    return;

                }


                /*
                ------------------------------------------------
                ICCID REQUIRED
                ------------------------------------------------
                */

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
                SERIAL NUMBER
                ANY LENGTH
                ALPHANUMERIC ONLY
                ====================================================
                */

                if (
                    !/^[A-Z0-9]+$/.test(
                        serialValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "Serial Number must contain only letters and numbers."
                    );

                    serial.focus();

                    return;

                }


                /*
                ====================================================
                IMEI NUMBER
                ANY LENGTH
                ALPHANUMERIC ONLY
                ====================================================
                */

                if (
                    !/^[A-Z0-9]+$/.test(
                        imeiValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "IMEI Number must contain only letters and numbers."
                    );

                    imei.focus();

                    return;

                }


                /*
                ====================================================
                ICCID NUMBER
                ANY LENGTH
                ALPHANUMERIC ONLY
                ====================================================
                */

                if (
                    !/^[A-Z0-9]+$/.test(
                        iccidValue
                    )
                ) {

                    event.preventDefault();

                    alert(
                        "ICCID Number must contain only letters and numbers."
                    );

                    iccid.focus();

                    return;

                }


                /*
                ====================================================
                ALL VALID
                CERTIFICATE WILL BE CREATED
                ====================================================
                */

            }
        );

    }
);

