var ChatApp = angular.module('ChatApp', []);

ChatApp.controller('ChatController', function($scope) {
  var namespace = '/test';
  var socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port + namespace
  );

  $scope.messages = [];
  $scope.name = '';
  $scope.text = '';
  $scope.stamp = ''; // ADD DATE

  socket.on('connect', function() {
    console.log('connected');
  });

  socket.on('message', function(msg) {
    console.log(msg);
    $scope.messages.push(msg);
    $scope.$apply(); // update UI
    var el = document.getElementById('msgpane');
    el.scrollTop = el.scrollHeight;
  });

  $scope.setName = function setName() {
    socket.emit('identify', $scope.name);
  };

  $scope.send = function send() {
    console.log('Sending message: ' + $scope.text);
    socket.emit('message', $scope.text);
    $scope.text = ''; // Clear the input
  };
});
