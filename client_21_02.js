$(document).ready(function () {
  var socket = io('http://' + document.domain + ':' + location.port);
  console.log('http://' + document.domain + ':' + location.port)
  socket.on('connect', function () {
    console.log('con');
    socket.emit('event', { data: 'I\'m connected!' });
  });

  socket.on('my_response', function (msg, cd) {
    console.log(msg.data, 10);
    generateData(msg.data)
    // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    if (cd) {
      cd();
    }
  });

  $("#btn").click(function () {
    socket.emit('my_event', { data: 'I\'m connected!' });
  });

  $("#one_1").click(function () {
    let inputData = $('#one_!').val();
    socket.emit('my_event', { data: inputData });
  });
  $("#two_2").click(function () {
    let inputData = $('#two_!').val();
    socket.emit('my_event', { data: inputData });
  });
  $("#three_3").click(function () {
    let inputData = $('#three_!').val();
    socket.emit('my_event', { data: inputData });
  });
  $("#four_4").click(function () {
    let inputData = $('#four_!').val();
    socket.emit('my_event', { data: inputData });
  });
  $("#five_5").click(function () {
    let inputData = $('#five_!').val();
    socket.emit('my_event', { data: inputData });
  });
});

//
// $(document).ready(function() {
//     // Connect to the Socket.IO server.
//     // The connection URL has the following format, relative to the current page:
//     //     http[s]://<domain>:<port>[/<namespace>]
//     var socket = io('http://' + document.domain + ':' + location.port);
//
//     // Event handler for new connections.
//     // The callback function is invoked when a connection with the
//     // server is established.
//     socket.on('connect', function() {
//
//         socket.emit('my_event', {data: 'I\'m connected!'});
//     });
//
//     // Event handler for server sent data.
//     // The callback function is invoked whenever the server emits data
//     // to the client. The data is then displayed in the "Received"
//     // section of the page.
//     socket.on('my_response', function(msg, cb) {
//       console.log(1)
//         $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
//         if (cb)
//             cb();
//     });
//
// });
