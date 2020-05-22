//'query': 'SELECT * FROM [wellbeing-app-cloud-computing.food.food] LIMIT 10;'
var project_id = 'wellbeing-app-cloud-computing';
var client_id = '355287276328-5vlstr8o47dvd5sssh0kvd0bmt9u5lp2.apps.googleusercontent.com';

var config = {
    'client_id': client_id,
    'scope': 'https://www.googleapis.com/auth/bigquery'
  };

  function showProjects() {
    var request = gapi.client.bigquery.projects.list();
    request.execute(function(response) {     
        $('#result_box').html(JSON.stringify(response, null));
    });
  }

  function showDatasets() {
    var request = gapi.client.bigquery.datasets.list({
      'projectId':'publicdata'
    });
    request.execute(function(response) {     
        $('#result_box').html(JSON.stringify(response.result.datasets, null));
    });
  }

  function runQuery() {
   var request = gapi.client.bigquery.jobs.query({
      'projectId': project_id,
      'timeoutMs': '30000',
      'query': 'query': 'SELECT * FROM [wellbeing-app-cloud-computing.food.food] LIMIT 10;'
    });
    request.execute(function(response) {     
        console.log(response);
        $('#result_box').html(JSON.stringify(response.result.rows, null));
    });
  }

  function auth() {
    gapi.auth.authorize(config, function() {
        gapi.client.load('bigquery', 'v2');
        $('#client_initiated').html('BigQuery client initiated');
        $('#auth_button').fadeOut();
        $('#projects_button').fadeIn();
        $('#dataset_button').fadeIn();
        $('#query_button').fadeIn();
    });
  }
