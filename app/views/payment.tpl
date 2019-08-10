<script>
    $(function(){

        // Search payer by name or enter account number
        $("#searchPayerBy").change(function() {
            var changeVal = $(this).val();
            if (changeVal === "account") {
                $("#payByAccount").removeClass("hidden");
                $("#payments-account").addClass("payments");

                $("#payByPerson").addClass("hidden");
                $("#payments-person").removeClass("payments");
            }
            if (changeVal === "person") {
                $("#payByPerson").removeClass("hidden");
                $("#payments-person").addClass("payments");

                $("#payByAccount").addClass("hidden");
                $("#payments-account").removeClass("payments");
            }
        });

        // Select if payment or credit
        

    });
</script>