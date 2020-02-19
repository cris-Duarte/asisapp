
function onSignIn(googleUser) {
  var id_token = googleUser.getAuthResponse().id_token;
  toServer(id_token);
}
function toServer(it) {
  var idt0ken = it;
  const request = new XMLHttpRequest();
  request.open('POST','/gCallback',false);
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  request.send('idtoken=' + idt0ken);
  if (request.status === 200) {
    location.reload();
}
};
