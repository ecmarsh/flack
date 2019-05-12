var ChatApp = angular.module('ChatApp', []);

ChatApp.controller('ChatController', function($scope, $http) {
  var namespace = '/chat',
    socket = io.connect(
      location.protocol +
        '//' +
        document.domain +
        ':' +
        location.port +
        namespace
    );

  $scope.name = cookieFns.get('displayName') || ''; // display name
  $scope.current_room = cookieFns.get('activeChannel') || 'general';
  $scope.messages = []; // active room messages
  $scope.roster = []; // online users
  $scope.text = ''; // message text form

  socket.on('connect', function() {
    console.log('Connected');
    // Send any cookie values to server
    $scope.setName();
    if ($scope.current_room) {
      socket.emit('join', $scope.current_room);
    }
  });

  // Sync local roster w/ server sessions
  socket.on('roster', function(names) {
    $scope.roster = names;
    $scope.$apply();
  });

  // Sync local channels w/ server rooms
  socket.on('rooms', function(rooms) {
    console.log('Got some new rooms');
    $scope.rooms = rooms;
    if (!$scope.current_room) {
      $scope.current_room = rooms[0];
      socket.emit('join', rooms[0]);
    }
    $scope.$apply();
  });

  // Create new channel
  $scope.createRoom = function() {
    if ($scope.new_room_name.length > 0) {
      // POST req to create channel
      $http
        .post('/new_room', { name: $scope.new_room_name })
        .then(function(res) {
          // console.log(JSON.stringify(res.data));
          $scope.new_room_name = '';
        }),
        function(e) {
          console.error(e);
        };
    }
    // Move them into the new room
    $scope.changeRoom($scope.new_room_name);
    $scope.apply();
  };

  // Batch update messages
  socket.on('localUpdate', function(msgs) {
    $scope.messages = msgs;
    $scope.$apply();
  });

  // Show the message
  socket.on('message', function(msg) {
    $scope.messages.push(msg);
    $scope.$apply(); // Update UI
  });

  // Create a new message
  $scope.send = function send() {
    socket.emit('message', { text: $scope.text, room: $scope.current_room });
    $scope.text = ''; // Clear the input
  };

  // Set and save display name
  $scope.setName = function setName() {
    socket.emit('identify', $scope.name);
    cookieFns.set('displayName', $scope.name);
  };

  $scope.changeRoom = function(new_room) {
    // Leave current channel, join selected
    socket.emit('leave', $scope.current_room);
    $scope.current_room = new_room;
    $scope.messages = []; // reset messages
    // Store user's channel
    cookieFns.set('activeChannel', new_room.toLowerCase());
    // Join the new room
    socket.emit('join', new_room);
  };
});
