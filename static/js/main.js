//$(document).ready(function(){
	
    // Function to download data to a file
    function download(data, filename, type) {
        console.log(data.length);
        // console.log(data);
    	var file = new Blob([data], {type: type});
    	console.log(file.size);
    	if (window.navigator.msSaveOrOpenBlob) // IE10+
        	window.navigator.msSaveOrOpenBlob(file, filename);
    	else { // Others
        	var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        	a.href = url;
        	a.download = filename;
        	document.body.appendChild(a);
        	a.click();
        	setTimeout(function() {
            		document.body.removeChild(a);
            		window.URL.revokeObjectURL(url);  
        	}, 0); 
   	    }
    }

    Dropzone.options.encryptDropzone = {
        paramName: "file",
        maxFilesize: 1024,
        url: '/crypto/encrypt',
        previewsContainer: "#encrypt-dropzone-previews",
        uploadMultiple: true,
        parallelUploads: 1,
        maxFiles: 1,
        init: function() {
            var file_name = 'file';
            var file_ext = '.txt';
            var file_type = 'text/plain';
            this.on("success", function(file, response) {
                $('.dz-progress').hide();
                $('.dz-size').hide();
                $('.dz-error-mark').hide();
                console.log(response);
                console.log(file);
                console.log(file_ext);
                console.log(file_name);
                console.log(file_type);
                download(response, 'enc_'+file_name+file_ext, file_type);
            });
            this.on("sending", function(file) {
                console.log(file);
            });
            this.on("drop", function (file) {
                console.log(file);
                // formdata = new FormData();
                // console.log("drop event");
                // // if($(this).prop('files').length > 0) {
                // //     file = $(this).prop('files')[0];
                //     console.log('File: '+file.dataTransfer.files[0]);
                //     formdata.append("file", file);
                // // }
                // $.ajax({
                //     type: 'POST',
                //     url: '/crypto/encrypt',
                //     data: formdata,
                //     processData: false,
                //     contentType: false
                // });

            });
            this.on("complete", function(file, resp) {
                console.log(file);
                console.log(resp);
                $.get("/log/getLog", function(data, status){
                    console.log(data);
                    console.log(status);
                    data = data.replace(/ /g, '\u00a0').replace(/\n/g, "<br/>");
                    data = data.replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
                    document.getElementById('log').innerHTML = data;
                });
            });
            this.on("addedfile", function(file) {
                var file_splits = file.name.split('.');
                file_name = file_splits[0];
                if(file_splits.length === 1)
                    file_ext = "";
                else
                    file_ext = "."+file_splits[1];
                console.log(file_ext);
                file_type = file.type;
            //    var removeButton = Dropzone.createElement("<a href=\"#\">Remove file</a>");
            //    var _this = this;
            //    removeButton.addEventListener("click", function(e) {
            //        e.preventDefault();
            //        e.stopPropagation();
            //        _this.removeFile(file);
            //        var name = "largeFileName=" + cd.pi.largePicPath + "&smallFileName=" + cd.pi.smallPicPath;
            //        $.ajax({
            //            type: 'POST',
            //            url: 'DeleteImage',
            //            data: name,
            //            dataType: 'json'
            //        });
            //    });
            //    file.previewElement.appendChild(removeButton);
            });
        }
    };

    Dropzone.options.decryptDropzone = {
        paramName: "file",
        maxFilesize: 1024,
        url: '/crypto/decrypt',
        previewsContainer: "#decrypt-dropzone-previews",
        uploadMultiple: true,
        parallelUploads: 1,
        maxFiles: 1,
        init: function() {
            var file_name = 'file';
            var file_ext = '.txt';
            var file_type = 'text/plain';
            this.on("success", function(file, response) {
                $('.dz-progress').hide();
                $('.dz-size').hide();
                $('.dz-error-mark').hide();
                console.log(response);
                console.log(file);
                console.log(atob(response));
                download(atob(response), 'dec_'+file_name+file_ext, file_type);
            });
            this.on("sending", function(file, xhr, o) {
                console.log(file);
            });
            this.on("drop", function (file) {
                // formdata = new FormData();
                // if($(this).prop('files').length > 0) {
                //     file = $(this).prop('files')[0];
                //     formdata.append("file", file);
                // };
                // $.ajax({
                //     type: 'POST',
                //     url: '/crypto/decrypt',
                //     data: formdata,
                //     processData: false,
                //     contentType: false
                // });
            });
            this.on("complete", function(file, resp) {
                console.log(file);
                console.log(resp);
                $.get("/log/getLog", function(data, status){
                    console.log(data);
                    console.log(status);
                    data = data.replace(/ /g, '\u00a0').replace(/\n/g, "<br/>");
                    data = data.replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
                    document.getElementById('log').innerHTML = data;
                });
            });
            this.on("addedfile", function(file) {
                var file_splits = file.name.split('.');
                file_name = file_splits[0];
                if(file_splits.length === 1)
                    file_ext = "";
                else
                    file_ext = "."+file_splits[1];
                file_type = file.type;
            //     var removeButton = Dropzone.createElement("<a href=\"#\">Remove file</a>");
            //     var _this = this;
            //     removeButton.addEventListener("click", function(e) {
            //         e.preventDefault();
            //         e.stopPropagation();
            //         _this.removeFile(file);
            //         var name = "largeFileName=" + cd.pi.largePicPath + "&smallFileName=" + cd.pi.smallPicPath;
            //         $.ajax({
            //             type: 'POST',
            //             url: 'DeleteImage',
            //             data: name,
            //             dataType: 'json'
            //         });
            //     });
            //     file.previewElement.appendChild(removeButton);
            });
        }
    };

//});

document.getElementById('show-log').addEventListener('click', function() {
    var currDisplay = document.getElementById('log').style.display;
    if (currDisplay == 'block') {
      document.getElementById('log-label').style.display = 'none';
      document.getElementById('log').style.display = 'none';
      document.getElementById('show-log').innerText = 'Show log';
    } else {
      document.getElementById('log-label').style.display = 'block';
      document.getElementById('log').style.display = 'block';
      document.getElementById('show-log').innerText = 'Hide log';
    }
    
});