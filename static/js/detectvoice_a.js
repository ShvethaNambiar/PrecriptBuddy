$(document).ready(function () {
    $('#form_pi').on('submit', function(e) {
        e.preventDefault();
        console.log('entered jquery')
        $.ajax({
            type: 'POST',
            url: '/personalinfo'
       })
       .done(function(data) {
            console.log('entered here');
            $('#printname').text(data.name).show();
            $('#printage').text(data.age).show();
            $('#printgender').text(data.gender).show();
       });
    });
    $('#form_symptoms').on('submit', function(e) {
        e.preventDefault();
        console.log('entered jquery')
        $.ajax({
            type: 'POST',
            url: '/symptoms'
       })
       .done(function(data) {
           $('#printsymptoms').text(data.symptoms_split).show()
       });
    });
});
   