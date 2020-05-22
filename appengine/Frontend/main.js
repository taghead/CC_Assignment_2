$(function () {
  var backendHostUrl = 'https://backend-dot-wellbeing-app-cloud-computing.ts.r.appspot.com';

  var config = {
    apiKey: "AIzaSyD1HTBWxISiw41mcO13ZliL5JxslNYhOco",
    authDomain: "wellbeing-app-cloud-computing.firebaseapp.com",
    databaseURL: "https://wellbeing-app-cloud-computing.firebaseio.com",
    projectId: "wellbeing-app-cloud-computing",
    storageBucket: "wellbeing-app-cloud-computing.appspot.com",
    messagingSenderId: "355287276328",
    appId: "1:355287276328:web:a8c73e4d164c608c91ce1d",
    measurementId: "G-7WX27YE7MP"
  };

  var userIdToken = null;

  function configureFirebaseLogin() {

    firebase.initializeApp(config);

    firebase.auth().onAuthStateChanged(function (user) {
      if (user) {
        $('#logged-out').hide();
        var name = user.displayName;
        var welcomeName = name ? name : user.email;

        user.getIdToken().then(function (idToken) {
          userIdToken = idToken;

          fetchFood();

          $('#user').text(welcomeName);
          $('#logged-in').show();
          $('#sign-out').show();
          $('#sign-in').hide();

        });

      } else {
        $('#sign-out').hide();
        $('#sign-in').show();
        $('#logged-in').hide();
        $('#logged-out').show();

      }
    });
  }

  function configureFirebaseLoginWidget() {
    var uiConfig = {
      'signInSuccessUrl': '/',
      'signInOptions': [ /*firebase.auth.GoogleAuthProvider.PROVIDER_ID,*/ firebase.auth.EmailAuthProvider.PROVIDER_ID ]
    };

    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }

  function fetchFood() {
    $.ajax(backendHostUrl + '/food', {
      headers: {'Authorization': 'Bearer ' + userIdToken}
    }).then(function (data) {
      $('#food-container').empty();
      data.forEach(function (f) {
        $('#food-container').append($('<p>').text(f.message+"("+f.food+" "+f.calories+")"));
      });
    });
  }

  var signOutBtn = $('#sign-out');
  signOutBtn.click(function (event) {
    event.preventDefault();
    firebase.auth().signOut().then(function () {
      console.log("Sign out successful");
    }, function (error) {
      console.log(error);
    });
  });

  var saveFoodBtn = $('#add-food');
  saveFoodBtn.click(function (event) {
    event.preventDefault();

    var foodName = $('#add-food-name');
    var foodCal = $('#add-food-cal');
    $.ajax(backendHostUrl + '/add_food', {
      headers: {'Authorization': 'Bearer ' + userIdToken},
      method: 'POST',
      data: JSON.stringify({
        'message': "You added: "+foodName.val()+" which had "+foodCal.val()+" Calories",
        'food': foodName.val(),
        'calories': foodCal.val()
      }),
      contentType: 'application/json'
    }).then(function () {
      fetchFood();
    });
    foodName.val("");
    foodCal.val("");
  });

  configureFirebaseLogin();
  configureFirebaseLoginWidget();

});