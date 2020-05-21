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

          fetchNotes();

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
      'signInOptions': [ firebase.auth.GoogleAuthProvider.PROVIDER_ID, firebase.auth.EmailAuthProvider.PROVIDER_ID]
    };

    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }

  function fetchNotes() {
    $.ajax(backendHostUrl + '/notes', {
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      }
    }).then(function (data) {
      $('#notes-container').empty();
      data.forEach(function (note) {
        $('#notes-container').append($('<p>').text(note.message));
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

  var saveNoteBtn = $('#add-note');
  saveNoteBtn.click(function (event) {
    event.preventDefault();

    var noteField = $('#note-content');
    var note = noteField.val();
    noteField.val("");

    $.ajax(backendHostUrl + '/notes', {
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      },
      method: 'POST',
      data: JSON.stringify({
        'message': note
      }),
      contentType: 'application/json'
    }).then(function () {
      fetchNotes();
    });
  });

  configureFirebaseLogin();
  configureFirebaseLoginWidget();

});