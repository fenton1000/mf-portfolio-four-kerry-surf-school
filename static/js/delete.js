$(function(){
    $('#all-bookings button').on("click", function(){
        let dataDeleteHref = $(this).attr('data-delete-href');
        $('#confirm').attr('href', dataDeleteHref);
    });
});