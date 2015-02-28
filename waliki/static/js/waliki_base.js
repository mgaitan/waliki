
$('#btn-waliki_new').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.get(url, function(data){
            $('#new-modal .modal-body').empty().append(data.data);
            $('#new-modal').modal('show');

            $('input#id_title').on('input', function(){
                  var title = $(this).val();
                  console.log(title)
                  var url = $('#btn-new-submit').data('slug-url');
                  $.get(url, {'title': title}, function(data){
                        $('input#id_slug').val(data.slug);
                  });
            });

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
              $('#new-modal').modal('show');
          }
        });
});

