/*
$(document).ready(function() {
     $('form').on('submit', function(event) {
       $.ajax({
          data : {
            date_debut : $("date-debut").val(),
            date_fin : $("date-fin").val(),
                 },
             type : 'POST',
             url : '/dateSearch'
            })
        .done(function(data) {
          $('#output').text(data.output).show();
      });
      event.preventDefault();
      });
});
*/
/*

$('#addResto').click( addRestoSurveiller(event) {
  var list = document.getElementById("etablissements-choisies");
  var nom_etablissement = document.getElementById("etablissement-dropdown").value;
  list.innerHTML = nom_etablissement + "~"
}*/

function myFunction() {
  document.getElementById("addResto").innerHTML = "YOU CLICKED ME!";
}


/*$('#submit-button').click(function(event){
    var form = $('#date-form');
    var form_id = 'date-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getDatesFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData);
});

function getDatesFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}



function modular_ajax(url, type, formData) {
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        contentType: false,
        beforeSend: function() {
            // loading bar
            $('#form-response').html("<div class='progress'><div class='indeterminate'></div></div>");
        },
        complete: function () {
            // hide loading bar
            $('#form-response').html("");
        },
        success: function ( data ){
            if ( !$.trim( data.feedback )) { // response from Flask is empty
                toast_error_msg = "An empty response was returned.";
                toast_category = "danger";
            }
            else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = data.category;
            }
        },
        error: function(xhr) {console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = "An error occured";
            toast_category = "danger";
        },
    }).done(function() {
        M.toast({html: toast_error_msg, classes: 'bg-' +toast_category+ ' text-white'});
    });
};

var csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});


//////////





function onDateSubmit() {
  var date_debut = document.getElementById("date-debut").value;
  var date_fin = document.getElementById("date-fin").value;
  var msg_error = document.getElementById("msg_erreur2");
  var test = document.getElementById("test");


  
  if (date_debut === "" || date_fin === "" ) {
    msg_error.style.display = "block";
  } else {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          test.innerHTML = "testingggggg";
        } else {
          console.log('Erreur avec le serveur');
        }
      }
    };
    xhr.open("GET", "/contravenants?/du="+date_debut+"&au="+date_fin, true); 
    xhr.send();
  }

}

/*$(function(){
  $('button').click(function(){
    //var user = $('#inputUsername').val();
    //var pass = $('#inputPassword').val();

    var date_debut = document.getElementById("date-debut").value;
  var date_fin = document.getElementById("date-fin").value;
  var msg_error = document.getElementById("msg_erreur2");
  var test = document.getElementById("test");

    $.ajax({
      url: '/homeSearch',
      data: $('form').serialize(),
      type: 'GET',
      success: function(response){
        console.log(response);
      },
      error: function(error){
        console.log(error);
      }
    });
  });
});*/