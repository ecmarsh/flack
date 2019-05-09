$(document).ready(function() {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  // Attach listeners
  socket.on('connect', function() {
    // Attach listeners to channel creation
    $('button#channel-name').click(function() {
      var channelName = $('input#channel-name').val();
      socket.emit('create channel', { channel_name: channelName });
    });
  });
});
