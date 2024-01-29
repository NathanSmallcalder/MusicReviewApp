$(document).ready(function() {
    $("#search-input").on("input", function() {
        var searchTerm = $(this).val().trim();

        if (searchTerm !== "") {
            // Make an Ajax request to the server
            $.ajax({
                url: "/search",
                method: "POST",
                data: { searchTerm: searchTerm },
                dataType: "json",
                success: function(response) {
                    // Handle the received data and update the UI
                    displaySearchResults(response);
                },
                error: function(error) {
                    console.error("Ajax request failed:", error);
                }
            });
        } else {
            // Clear the search results if the search bar is empty
            $("#search-results").empty();
        }
    });

    function displaySearchResults(data) {
        console.log("displaySearchResults called with data:", data);
        var resultsContainer = $("#search-results");
        resultsContainer.empty();
    
        if (Array.isArray(data) && data.length > 0) {
            data.forEach(function (result, index) {
                var listItem = $("<li>");
                listItem.text(result.name);
    
                listItem.addClass("typing-animation clickable-item");
    
                listItem.attr("data-id", result.id);
    
                resultsContainer.append(listItem);
    
                setTimeout(function () {
                    listItem.removeClass("typing-animation");
                }, index * 100); // Adjust the delay as needed
            });
        } else {
            console.log("No results found.");
        }
    }
    $(document).ready(function() {
        // Event delegation to handle clicks on dynamically added elements
        $("#search-results").on("click", ".clickable-item", function() {
            // Get the ID from the data-id attribute
            var itemId = $(this).attr("data-id");
    
            // Redirect to the new page with the ID
            window.location.href = "/album?album=" + itemId;
        });
    });
});