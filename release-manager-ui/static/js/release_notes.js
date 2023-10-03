document.addEventListener('DOMContentLoaded', function () {
  var copyButton = document.getElementById("copy_button");
  var contentToCopy = document.getElementById("releaseNotes");

  copyButton.addEventListener("click", async function () {
    try {
      // Create a new ClipboardItem with the HTML content
      var clipboardItem = new ClipboardItem({
        'text/html': new Blob([contentToCopy.innerHTML], { type: 'text/html' })
      });

      // Write the ClipboardItem to the clipboard
      await navigator.clipboard.write([clipboardItem]);

    } catch (err) {
      console.error('Failed to copy content: ', err);
    }
  });

  // Function to format a date as "yyyy-mm-dd"
  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Add leading zero if needed
    const day = String(date.getDate()).padStart(2, '0'); // Add leading zero if needed
    return `${year}-${month}-${day}`;
  }

  // Get the current date
  const currentDate = new Date();

  // Format the date
  const formattedDate = formatDate(currentDate);

  // Insert the formatted date into the H2 element
  const dateDisplayElement = document.getElementById("dateDisplay");
  dateDisplayElement.textContent = formattedDate;

});
