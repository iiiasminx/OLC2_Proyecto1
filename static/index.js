console.log('Fighting!');

$(document).ready(function () {
    // codigo de Jquery

    var editorEntrada = CodeMirror.fromTextArea(
      document.getElementById('entrada'), {
      mode: "julia",
      theme: "darcula",
      lineNumbers: true,
      lineWrapping: false, 
      readOnly: false
    });
    editorEntrada.setSize(null, 300);

    var editorSalida = CodeMirror.fromTextArea(
      document.getElementById('salida'), {
      mode: "julia",
      theme: "darcula",
      lineNumbers: true,
      lineWrapping: false, 
      readOnly: true
    });
    editorSalida.setSize(null, 300);
});