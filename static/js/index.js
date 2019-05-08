$(document).ready(function() {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  // When connected, configure buttons
  socket.on('connect', function() {
    // Button should create a display name
    $('button#btn-display-name').click(function() {
      var displayName = $('#display-name').val();
      console.log(displayName);
      socket.emit('register display name', { display_name: displayName });
    });
  });

  // Set name to local storage
  socket.on('save display name', function(data) {
    localStorage.setItem('name', data.displayName);
    socket.emit('name set', { name: data.displayName });
  });

  // When a new vote is announced, add to the unordered list
  socket.on('show display name', function(data) {
    $('ul#display-names').prepend(`<li>${data.displayName}</li>`);
  });
});
