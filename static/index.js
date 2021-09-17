console.log('Fighting!');


$(document).ready(function () {
  // codigo de Jquery

  var editorEntrada = CodeMirror.fromTextArea(
    document.getElementById('entrada'), {
    mode: "julia",
    theme: "darcula",
    lineNumbers: true,
    lineWrapping: true,
    readOnly: false
  });
  editorEntrada.setSize(null, 300);

  var editorSalida = CodeMirror.fromTextArea(
    document.getElementById('salida'), {
    mode: "julia",
    theme: "darcula",
    lineNumbers: true,
    lineWrapping: true,
    readOnly: true
  });
  editorSalida.setSize(null, 300);

  //labels que no se pueden ver
  document.getElementById("txtsalida").style.display = 'none';
  document.getElementById("txtentrada").style.display = 'none';
  document.getElementById("txterrores").style.display = 'none';

  if (window.location.href.indexOf("submit") > -1) {
    //editorSalida.getDoc().setValue('var msg = "Hi";');

    var loquesale = document.getElementById("txtsalida")
    var textosalida = loquesale.textContent;
    var loqueentra = document.getElementById("txtentrada")
    var textoentrada = loqueentra.textContent;

    editorSalida.getDoc().setValue(textosalida);
    editorEntrada.getDoc().setValue(textoentrada);

  }
});