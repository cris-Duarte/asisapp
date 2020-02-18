
function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  toServer(id_token);
}
var toServer = function(it) {
  var idt0ken = it;
  const request = new XMLHttpRequest();
  request.open('POST','/gCallback');
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  request.onload = function() {

};
  request.send('idtoken=' + idt0ken);

};
