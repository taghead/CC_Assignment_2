<!doctype html>
<html>

<head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
  <script src="https://www.gstatic.com/firebasejs/5.6.0/firebase-app.js"></script>
  <script src="https://www.gstatic.com/firebasejs/5.6.0/firebase-auth.js"></script>
  <script src="https://cdn.firebase.com/libs/firebaseui/3.4.1/firebaseui.js"></script>
  <link type="text/css" rel="stylesheet" href="https://cdn.firebase.com/libs/firebaseui/3.4.1/firebaseui.css">
  <link rel="stylesheet" type="text/css" href="/css/style.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <script>
    $(
      function () {
        var userIdToken = null;
        var firebase_config = {
          apiKey: "AIzaSyD1HTBWxISiw41mcO13ZliL5JxslNYhOco",
          authDomain: "wellbeing-app-cloud-computing.firebaseapp.com",
          databaseURL: "https://wellbeing-app-cloud-computing.firebaseio.com",
          projectId: "wellbeing-app-cloud-computing",
          storageBucket: "wellbeing-app-cloud-computing.appspot.com",
          messagingSenderId: "355287276328",
          appId: "1:355287276328:web:a8c73e4d164c608c91ce1d",
          measurementId: "G-7WX27YE7MP"
        };

        function configureFirebaseLogin() {
          firebase.initializeApp(firebase_config);
          firebase.auth().onAuthStateChanged(function (user) {
            if (user) {
              $('#logged-out').hide();
              var name = user.displayName;
              var welcomeName = name ? name : user.email;
              user.getIdToken().then(function (idToken) {
                userIdToken = idToken;
                fetchNotes();
                $('#user').text(welcomeName);
                $('#logged-in').show();
              });
            } else {
              $('#logged-in').hide();
              $('#logged-out').show();

            }
          });
        }

        function configureFirebaseLoginWidget() {
          var uiConfig = {
            'signInSuccessUrl': '/',
            'signInOptions': [firebase.auth.GoogleAuthProvider.PROVIDER_ID, firebase.auth.EmailAuthProvider
              .PROVIDER_ID
            ]
          };
          var ui = new firebaseui.auth.AuthUI(firebase.auth());
          ui.start('#firebaseui-auth-container', uiConfig);
        }

        var signOutBtn = $('#sign-out');
        signOutBtn.click(function (event) {
          event.preventDefault();
          firebase.auth().signOut().then(function () {
              console.log("Sign out successful");
            },
            function (error) {
              console.log(error);
            });
        });

        configureFirebaseLogin();
        configureFirebaseLoginWidget();
      });
  </script>
  <title>Health Wellbeing</title>
</head>