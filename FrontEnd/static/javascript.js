window.setInterval(function() {
  var elem =
      document.getElementById("response");
  elem.scrollTop = elem.scrollHeight;
}, 500);

document.addEventListener("keyup", function(e) {
	if (e.keyCode == 13) {
		reply();
	}
});

function reply() {
	var input = document.getElementById("userInput").value;
	var chatbox = document.getElementById("response");
	var userInput = input.toUpperCase();

	chatbox.innerHTML += "<br/> <span style='color: blue;'>You:</span> " + input;
	document.getElementById("userInput").value = '';
}
