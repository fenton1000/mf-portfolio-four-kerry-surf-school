let data = document.currentScript.dataset;
let dateOfBirth = data.dob;

$(function () {

    function fillInDateOfBirth() {
        let newDateOfBirth = new Date(dateOfBirth);
        let formattedDateOfBirth = new Date(
            newDateOfBirth.getTime() - (newDateOfBirth.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
        $("#id_date_of_birth").val(formattedDateOfBirth);
    }

    fillInDateOfBirth(); 
});