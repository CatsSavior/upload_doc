var button = document.getElementById("copyID"),
    input =  document.getElementById("box-content"),
    html_for_copy = document.getElementById("html_for_copy").textContent;

document.querySelector("textarea[name=box-content]").setAttribute('value',html_for_copy);

button.addEventListener("click", function(event) {

  event.preventDefault();
  input.select();
  document.execCommand("copy");

});