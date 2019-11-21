//$(document).ready(function(){

    Dropzone.options.uploadDropzone = {
        paramName: "file",
        maxFilesize: 1024,
        url: '/send_csv',
        previewsContainer: "#upload-dropzone-previews",
        uploadMultiple: true,
        parallelUploads: 1,
        maxFiles: 1,
        init: function() {
            this.on("success", function(response) {
                $('.dz-progress').hide();
                $('.dz-size').hide();
                $('.dz-error-mark').hide();
                console.log(response);
            });
            this.on("complete", function(response) {
                console.log(response);
            });
        }
    };

document.getElementById('send_query').addEventListener('click', function() {
    var epsilon = parseFloat(document.getElementById("epsilon").value);
    console.log(epsilon);
    if (isNaN(epsilon)) {
      document.getElementById('result').value = 'Invalid epsilon!';
    } else {
      var xmlhttp = new XMLHttpRequest();
      //var url = 'http://localhost:5002/query';
      var url = 'http://172.25.0.2:5002/query'
      var data = JSON.stringify({
          'id':document.getElementById('id').value,
          'file':document.getElementById('file').value,
          'query':document.getElementById('query').value,
          'epsilon':document.getElementById('epsilon').value
      });
      xmlhttp.open('POST', url, false);
      xmlhttp.setRequestHeader('Content-Type', 'application/json');
      xmlhttp.send(data);
      document.getElementById('result').innerHTML = xmlhttp.responseText;
    }
    
});