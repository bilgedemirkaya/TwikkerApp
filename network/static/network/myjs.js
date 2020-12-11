// Dropdown menu
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

function openModel () {
  document.getElementById('myBtn').addEventListener('click', () => {
  document.querySelector('.bg-modal').style.display ='flex';
  });
      
  document.querySelector(".close").addEventListener('click',() => {
  document.querySelector('.bg-modal').style.display ='none';
  });
  
  document.querySelector(".posted").style.display = 'block';
  document.querySelector(".likes").style.display = 'none';
  
  // Use buttons to toggle between views ( Profile section - posts vs liked posts)
  document.querySelector('#userposts').addEventListener('click', () => {
  document.querySelector(".posted").style.display = 'block';
  document.querySelector(".likes").style.display = 'none';
  });

  document.querySelector('#likedposts').addEventListener('click', () => {
  document.querySelector('.posted').style.display = 'none';
  document.querySelector('.likes').style.display = 'block';
  }); 
}
    
    function showLikes () {
      document.getElementById('likeBtn').addEventListener('click', () => {
      document.querySelector('.bg').style.display ='flex';
      });
      document.querySelector(".lclose").addEventListener('click',() => {
      document.querySelector('.bg').style.display ='none';
      });
    }

    function showFollowers () {
      document.getElementById('fBtn').addEventListener('click', () => {
      document.querySelector('.fg-modal').style.display ='flex';
        });
      document.querySelector(".fclose").addEventListener('click',() => {
      document.querySelector('.fg-modal').style.display ='none';
        });
    }

    function showFollowings () {
      document.getElementById('fsBtn').addEventListener('click', () => {
        document.querySelector('.fs-modal').style.display ='flex';
        });
      document.querySelector(".fsclose").addEventListener('click',() => {
          document.querySelector('.fs-modal').style.display ='none';
        });
      }
    
      function showMessage () {
        document.getElementById('msjBtn').addEventListener('click', () => {
          document.querySelector('.msj-modal').style.display ='flex';
          });
        document.querySelector(".f-mclose").addEventListener('click',() => {
            document.querySelector('.msj-modal').style.display ='none';
          });
      }

      function showDelete () {
        document.querySelector('.delete').addEventListener('click', () => {
        document.querySelector('.delete-modal').style.display ='flex';
        });
        document.querySelector('#cancel').addEventListener('click', () => {
          document.querySelector('.delete-modal').style.display ='none';
        });
      }
  
      // listeners
      document.addEventListener('DOMContentLoaded', showLikes);
      document.addEventListener('DOMContentLoaded', openModel);
      document.addEventListener('DOMContentLoaded', showMessage);
      document.addEventListener('DOMContentLoaded', showFollowings);
      document.addEventListener('DOMContentLoaded', showDelete);
      document.addEventListener('DOMContentLoaded', showFollowers);