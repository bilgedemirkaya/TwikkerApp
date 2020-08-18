function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.profilebutton')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("mainbutton").addEventListener('click',() => {
    document.querySelector(".thirdcol").style.backgroundColor = "black";
  })
      document.querySelector(".posted").style.display = 'block';
      document.querySelector(".likes").style.display = 'none';
    // Use buttons to toggle between views
    document.querySelector('#userposts').addEventListener('click', () => {
      document.querySelector(".posted").style.display = 'block';
      document.querySelector(".likes").style.display = 'none';
    });
    document.querySelector('#likedposts').addEventListener('click', () => {
      document.querySelector('.posted').style.display = 'none';
      document.querySelector('.likes').style.display = 'block';
    });
  
});
