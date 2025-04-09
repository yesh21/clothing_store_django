document.addEventListener("DOMContentLoaded", function() {
    function activateTab() {
      var hash = window.location.hash; // Get the hash from the URL
      var tabs = document.querySelectorAll('.tab-content'); // Select all tab contents
      // Hide all tabs initially
      tabs.forEach(function(tab) {
        tab.style.display = 'none';
      });
      // Show the tab that matches the hash
      if (hash) {
        var activeTab = document.querySelector(hash);
        if (activeTab) {
          activeTab.style.display = 'block'; // Show the active tab
        }
      } else {
        // Optionally show a default tab if no hash is present
        tabs[0].style.display = 'block'; // Show first tab by default
      }
    }
    activateTab(); // Call the function to activate the correct tab
    // Optional: Change tab on hash change
    window.addEventListener('hashchange', activateTab);
  });
