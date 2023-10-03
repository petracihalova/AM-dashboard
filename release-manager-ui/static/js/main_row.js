// Show hidden / expandable section
function toggleInfo(row) {
    var info = row.nextElementSibling;
    if (info.style.display === "none") {
      info.style.display = "table-row";
    } else {
      info.style.display = "none";
    }
  };
  