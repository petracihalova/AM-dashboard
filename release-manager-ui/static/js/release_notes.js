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

      // Provide visual feedback or alert
      alert('Content copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy content: ', err);
    }
  });
});
