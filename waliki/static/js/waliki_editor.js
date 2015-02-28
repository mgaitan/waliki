var editor = CodeMirror.fromTextArea(document.getElementById("id_raw"), cm_settings);

$(document.body).on('click', '#markup_menu li', function(event) {

  var $target = $( event.currentTarget );

  $target.closest( '.btn-group' )
     .find( '[data-bind="label"]' ).text( $target.text() )
        .end()
     .children( '.dropdown-toggle' ).dropdown( 'toggle' );

  $('#id_markup').val($target.text());
  console.log($target);
  var new_mode = $target.find('a').data('mode');
  editor.setOption('mode', new_mode);

  console.log(new_mode);

  return false;

});

function winHeight() {
  return window.innerHeight || (document.documentElement || document.body).clientHeight;
}


$(document.body).on('click', '#fullscreen', function(event) {
    var $editor = $('#waliki_editor');
    var is_full = $editor.hasClass('waliki_full_screen');
    if (is_full){
        $editor.removeClass('waliki_full_screen');
        $('#editor').addClass('pad');
        $(this).find('span').attr('class', 'glyphicon glyphicon-resize-full');
        $('.form-group:not(#div_id_raw), .row:last', 'form.form').show();
        $('.CodeMirror').height($('.CodeMirror').data('height'));
    }else{
        $editor.addClass('waliki_full_screen');
        $('#editor').removeClass('pad');
        $(this).find('span').attr('class', 'glyphicon glyphicon-resize-small');
        $('.form-group:not(#div_id_raw), .row:last', 'form.form').hide();
        $('.CodeMirror').data('height', $('.CodeMirror').height());
        $('.CodeMirror').height(winHeight() - 52);
    }
    editor.focus();
});


$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
  var target = $(e.target).attr("href");
  if ((target == '#editor')) {
    editor.focus();
  }
});


$('#btn-waliki_move').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        console.log(url);
        $.get(url, function(data){
            $('#move-modal .modal-body').empty().append(data.data);
            $('#move-modal').modal('show');
        });
});

$("#move-form").submit(function(e) {
    e.preventDefault();
    var url = $(this).attr('action');
    $.post(url, $(this).serialize(), function(data){
          if (data.redirect !== undefined){
            window.location = data.redirect;
          }else {
              $('#move-modal .modal-body').empty().append(data.data);
              $('#move-modal').modal('show');
          }
        });
});
