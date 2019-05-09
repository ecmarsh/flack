var ChatApp = angular.module('ChatApp', []);

ChatApp.controller('ChatController', function($scope) {
  var namespace = '/test';
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port + namespace
  );

  $scope.messages = [];
  $scope.roster = [];
  $scope.name = localStorage.getItem('name') || '';
  $scope.text = '';
  $scope.stamp = '';

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
      superagent
        .post('/new_room')
        .send({ name: $scope.new_room_name })
        .end(function(err, result) {});
    }

    $scope.new_room_name = '';
    console.log('Create room: ' + $scope.new_room_name);
  };

  // Show the message
  socket.on('message', function(msg) {
    console.log(msg);
    $scope.messages.push(msg);
    $scope.$apply(); // update UI
    var el = document.getElementById('msgpane');
    el.scrollTop = el.scrollHeight;
  });

  // Set display name
  $scope.setName = function setName() {
    socket.emit('identify', $scope.name);
  };

  $scope.changeRoom = function(new_room) {
    $scope.current_room = new_room;
  };

  // Send a message
  $scope.send = function send() {
    console.log('Sending message: ' + $scope.text);
    socket.emit('message', $scope.text);
    $scope.text = ''; // Clear the input
  };
});
