
function hook_slug() {
         $('input#id_title').on('input', function(){
                  var title = $(this).val();
                  var url = $('#btn-new-submit').data('slug-url');
                  $.get(url, {'title': title}, function(data){
                        $('input#id_slug').val(data.slug);
                  });
            });
}

$('#btn-waliki_new').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.get(url, function(data){
            $('#new-modal .modal-body').empty().append(data.data);
            $('#new-modal').modal('show');

            hook_slug();

        });
});


$("#new-form").submit(function(e) {
    e.preventDefault();
    var url = $(this).attr('action');
    $.post(url, $(this).serialize(), function(data){
          if (data.redirect !== undefined){
              window.location = data.redirect;
          }else {
              $('#new-modal .modal-body').empty().append(data.data);
              hook_slug();
              $('#new-modal').modal('show');

          }
        });
});

