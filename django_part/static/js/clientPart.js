var socket = null;
var isopen = false;
var counter = 0;
window.onload = function() {
   socket = new WebSocket("ws://127.0.0.1:9000");
   socket.binaryType = "arraybuffer";
   socket.onopen = function () {
     console.log("Connected!");
   };
   socket.onmessage = function (e) {
     if (typeof e.data == "string") {
       console.log("Received: " + e.data);
       var data = e.data.split(',');
       if (data[0] == 'query'){
         counter = counter + 1;
       if (counter >= 1) {
        for (var i = 1; i <= counter; i++) {
          var ProgressBar = document.getElementById("lamp" + i);
          ProgressBar.innerHTML = '<span class="done"></span>';
        }
       }
         if (counter > 2) {
           setTimeout(function () {
             window.location.href = 'http://127.0.0.1:8000/#/query/' + data[1] + '/';
           }, 300);
         }
       }
       if (data[0] == 'zip') {
         console.log(data[1]);
         window.location.href = 'http://127.0.0.1:8000/download/' + data[1];
       }
     }
   };
   socket.onclose = function (e) {
     console.log("Connection closed.");
     socket = null;
     isopen = false;
   }
};
