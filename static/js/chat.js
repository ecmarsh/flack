$(document).ready(function() {
  var namespace = window.location.pathname.substring(5);

  // Connect to websocket
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  // When connected, configure buttons
  socket.on('connect', function() {
    // Attach listeners to channel creation
    $('button#send').click(function() {
      var user = localStorage.getItem('name');
      var text = $('#message-data').val();
      var name = namespace.substring(1);
      var now = new Date();
      var data = {
        user: user,
        text: text,
        name: name,
        stamp: now.toLocaleTimeString('en-US'),
      };
      console.log(data);
      socket.emit('incoming', data);
    });
  });

  $('button#send-room').click(function(event) {
    event.preventDefault();
    console.log('...sending');
    socket.emit('newmessage', {
      channel: window.location.pathname.substring(6),
      message: $('#room-data').val(),
    });
    return false;
  });

  // Show new message
  socket.on('received', function(data) {
    console.log(data);
    let markup = ``;
    for (let message of data) {
      console.log(message);
      markup += `<li>
			    <p>${message.user}<span> ${message.stamp}</p>
				<p>${message.text}</p>
			</li>`;
    }
    console.log(markup);
    $('ul#messages').append(markup);
  });
});
