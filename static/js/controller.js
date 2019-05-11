var ChatApp = angular.module('ChatApp', []);

ChatApp.controller('ChatController', function($scope, $http) {
  var namespace = '/test';
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port + namespace
  );

  $scope.messages = [];
  $scope.roster = [];
  $scope.name = cookieFns.get('displayName') || '';
  $scope.text = '';
  $scope.stamp = '';
  $scope.current_room = cookieFns.get('activeChannel') || '';

  socket.on('connect', function() {
    console.log('connected');
    $scope.setName();
  });

  socket.on('roster', function(names) {
    $scope.roster = names;
    $scope.$apply();
  });

  socket.on('rooms', function(rooms) {
    console.log('Got some new rooms');
    $scope.rooms = rooms;
    if (!$scope.current_room) $scope.current_room = rooms[0];

    $scope.$apply();
  });

  $scope.createRoom = function() {
    if ($scope.new_room_name.length > 0) {
      $http
        .post('/new_room', { name: $scope.new_room_name })
        .then(function(res) {
          // console.log(JSON.stringify(res.data));
          $scope.new_room_name = '';
        }),
        function(err) {
          console.error(err);
        };
    }
    socket.emit('join', $scope.new_room_name);
    console.log('Created room: ' + $scope.new_room_name);
  };

  // Show the message
  socket.on('message', function(msg) {
    console.log(msg);
    $scope.messages.push(msg);
    $scope.$apply(); // update UI
  });

  // Set display name
  $scope.setName = function setName() {
    cookieFns.set('displayName', $scope.name);
    socket.emit('identify', $scope.name);
  };

  // Leave current room, join selected room
  $scope.changeRoom = function(new_room) {
    socket.emit('leave', $scope.current_room);
    $scope.current_room = new_room;
    socket.emit('join', new_room);
    cookieFns.set('activeChannel', new_room);
  };

  // Create a new message
  $scope.send = function send() {
    console.log('Sending message: ' + $scope.text);
    socket.emit('message', { text: $scope.text, room: $scope.current_room });
    $scope.text = ''; // Clear the input
  };
});
