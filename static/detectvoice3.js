$(document).ready(function () {
    $('form_pi').on('submit', function(e) {
        console.log('entered jquery')
        $.ajax({
            data: {
                getPersonalinfo=true
            },
            type: 'POST',
            url: '/personalinfo'
       })
       .done(function(data) {
            console.log('entered here');
            $('#printname').text(data.name).show();
            $('#printage').text(data.age).show();
            $('#printgender').text(data.gender).show();
       });
       e.preventDefault();
    });
});
   