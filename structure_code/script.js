// Function to set the active state
function setActive(element) {
    // Remove active class from all elements
    document.querySelectorAll('.ribbon-button, .sidebar-button').forEach(btn => btn.classList.remove('active'));
    // Add active class to the clicked element
    element.classList.add('active');
  }
  
  // Function to show the selected page
  function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
    // Show the selected page
    document.getElementById(pageId).classList.remove('hidden');
  }