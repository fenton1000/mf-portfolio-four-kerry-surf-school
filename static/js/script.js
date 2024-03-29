$(function () {

    function changeHomeView() {
        if (window.matchMedia("(max-width: 650px)").matches) {
            $("#accordion").removeClass("make-div-disappear").addClass("make-div-appear");
            $("#cards, #lessoninfo, #hireinfo").removeClass("make-div-appear").addClass("make-div-disappear");
        } else {
            $("#cards, #lessoninfo, #hireinfo").removeClass("make-div-disappear").addClass("make-div-appear");
            $("#accordion").removeClass("make-div-appear").addClass("make-div-disappear");
        }
    }

    changeHomeView();

    // Add listener for window resizing:
    window.addEventListener("resize", changeHomeView);

    setTimeout(function () {
        let messages = document.getElementById('msg');
        let alert = new bootstrap.Alert(messages);
        alert.close();
    }, 3000);
});