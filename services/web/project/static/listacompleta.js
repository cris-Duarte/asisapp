document.addEventListener('DOMContentLoaded', function() {
  t = document.getElementById('totalista');

  const request = new XMLHttpRequest();
  request.open('POST',u);
  request.onload = () => {
    t.innerHTML = request.response;
  };
  var data = new FormData();
  data.append('m',m)
  request.send(data);

});
