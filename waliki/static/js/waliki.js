var editor = CodeMirror.fromTextArea(document.getElementById("id_raw"), cm_settings);

$(document.body).on('click', '.dropdown-menu li', function(event) {

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
        $(this).find('span').attr('class', 'glyphicon glyphicon-resize-full');
        $('.form-group:not(#div_id_raw), .row:last', 'form.form').show();
        $('.CodeMirror').height($('.CodeMirror').data('height'));
    }else{
        $editor.addClass('waliki_full_screen');
        $(this).find('span').attr('class', 'glyphicon glyphicon-resize-small');
        $('.form-group:not(#div_id_raw), .row:last', 'form.form').hide();
        $('.CodeMirror').data('height', $('.CodeMirror').height());
        $('.CodeMirror').height(winHeight() - 75);
    }
});
