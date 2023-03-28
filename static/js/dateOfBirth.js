$(function () {

    function setMaxDate() {
        let maxDate = new Date();
        let formattedMaxDate = new Date(
            maxDate.getTime() - (maxDate.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
            $('#id_date_of_birth').attr('max', formattedMaxDate);
    }

    setMaxDate();
});