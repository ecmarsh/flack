$(document).ready(function() {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  // When connected, configure buttons
  socket.on('connect', function() {
    // Attach listeners to channel creation
    $('button#channel-name').click(function() {
      var channelName = $('input#channel-name').val();
      socket.emit('create channel', { channel_name: channelName });
    });
  });

  // When a new vote is announced, add to the unordered list
  socket.on('show display name', function(data) {
    $('ul#display-names').prepend(`<li>${data.displayName}</li>`);
  });
});
