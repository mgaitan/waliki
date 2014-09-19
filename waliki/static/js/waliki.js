debugger;
var editor = CodeMirror.fromTextArea(document.getElementById("id_raw"),
    {'mode': current_mode});

$( document.body ).on( 'click', '.dropdown-menu li', function( event ) {

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
