let data = document.currentScript.dataset;
let dateOfBirth = data.dob;
let lessonDate = data.lessonDate;
let abilityLevel = data.abilityLevel;
let lessonTime = data.lessonTime;

$(document).ready(function () {

    function fillInDateOfBirth() {
        let newDateOfBirth = new Date(dateOfBirth);
        let formattedDateOfBirth = new Date(
            newDateOfBirth.getTime() - (newDateOfBirth.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
        $("#id_date_of_birth").val(formattedDateOfBirth);
    }

    function fillInLessonDate() {
        let newLessonDate = new Date(lessonDate);
        let formattedLessonDate = new Date(
            newLessonDate.getTime() - (newLessonDate.getTimezoneOffset() * 60000))
            .toISOString()
            .split("T")[0];
        $("#id_lesson_date").val(formattedLessonDate);
    }

    function fillInAbilityLevel() {
        $("option[value|='"+abilityLevel+"']").attr('selected', 'selected');
    }

    function fillInLessonTime() {
        let [time, modifier] = lessonTime.split(' ');
        let hours;
        let minutes;
        if (time.includes(':')) {
            [hours, minutes] = time.split(':');
        } else {
            hours = time
            minutes = '00'
        }
        if (hours === '12') {
            hours = '00';
        }
        if (modifier === 'p.m.') {
            hours = parseInt(hours, 10) + 12;
        }
        lesson = `${hours}:${minutes}`;
        $("option[value|='"+lesson+"']").attr('selected', 'selected');
    }

    fillInDateOfBirth();
    fillInLessonDate();
    fillInAbilityLevel();
    fillInLessonTime();
});