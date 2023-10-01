window.addEventListener('DOMContentLoaded', event => {

  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  if (sidebarToggle) {
    if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
      document.body.classList.toggle('sb-sidenav-toggled');
    }
    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
  }
});

// Show hidden / expandable section
function toggleInfo(row) {
  var info = row.nextElementSibling;
  if (info.style.display === "none") {
    info.style.display = "table-row";
  } else {
    info.style.display = "none";
  }
};


var dropdown = document.getElementById("dropdown_names");
var lists = document.querySelectorAll("#pr_list");

dropdown.addEventListener("change", highlightItems);

function highlightItems() {
  var selectedText = dropdown.value;

  lists.forEach(function (list) {
    var items = list.getElementsByTagName("li");

    for (var i = 0; i < items.length; i++) {
      var itemText = items[i].innerText.toLowerCase();

      if (itemText.includes(selectedText.toLowerCase())) {
        items[i].classList.add("name-highlight");
      } else {
        items[i].classList.remove("name-highlight");
      }
    }
  });
}


function copyToClipboard(elementId) {
  var commitShaElement = document.getElementById(elementId);
  var commitShaText = commitShaElement.innerText;

  navigator.clipboard.writeText(commitShaText)
    .catch(function (error) {
      console.error("Error:", error);
    });
}

var toggleButton = document.getElementById("sidebarToggle");
var menuVisible = false;

toggleButton.addEventListener("click", function () {
  if (menuVisible) {
    toggleButton.textContent = "Hide menu";
  } else {
    toggleButton.textContent = "Show menu";
  }

  menuVisible = !menuVisible;
});

var updateButton = document.getElementById("update_button");

// Function to set Update button text to "Loading" and get the spinner visible
function setLoadingState() {
  updateButton.textContent = "";
  updateButton.appendChild(createSpinner());
  updateButton.appendChild(document.createTextNode("Loading"));
  updateButton.disabled = true;

  // Construct the URL with the parameter and navigate to it
  var url = "open_pr?reload_data=true";
  window.location.href = url;
}

// Function to create a spinner element
function createSpinner() {
  var spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm";
  spinner.setAttribute("role", "status");
  spinner.setAttribute("aria-hidden", "true");
  spinner.style.marginRight = "10px";
  return spinner;
}

// Attach the setLoadingState function to the button click event
updateButton.addEventListener("click", () => {
  setLoadingState();
});
