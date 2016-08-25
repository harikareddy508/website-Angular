var app = angular.module('sampleApp', []);

app.controller('MainController', ['$scope', 'MainService', '$timeout', function($scope, MainService, $timeout) {
    $scope.appointments = [];
    $scope.showSuccessMessage = false;
    $scope.getAppointments = function(searchText) {
        MainService.getAppointments(searchText).then(function(appointments){
           $scope.appointments = appointments;
        });
    };
    $scope.getAppointments('');

    $scope.createAppointment = function(appointment) {
        $scope.showSuccessMessage = false;
        MainService.createAppointment(appointment).then(function(data) {
            $scope.showSuccessMessage = data.status;
            $scope.appointments.push(data.appointment);
            $timeout(function() {
                $scope.showSuccessMessage = false;
            }, 2000);
            $scope.appointment = {}; //clearing out appointment form
        });
    };
}]);

app.factory('MainService', ['$http', function($http) {
    var service = {};
    service.getAppointments = function(searchText) {
        return $http.get('/?search=' + searchText).then(function (response) {
            return response.data.appointments;
        });
    };

    service.createAppointment = function(appointment) {
        return $http.post('/', appointment).then(function(response) {
            return response.data;
        });
    }
    return service;
}]);
$(document).ready(function() {
    //Initializing timepicker with icon
    $('#time').timepicker({
        defaultTime: 'current',
        showSeconds: true,
        showMeridian: false
    });
});