// This file contains code that is used by games.html mostly for working with the sorting and
// filtering fields. The idea is to store the values of the fields when the page reloads after 
// a POST request in order to populate the fields after the reload. This way, the user can utilize
// multiple filters and orderings at once.

function search(ele) {
    if(event.key == 'Enter'){
        localStorage.setItem('searchParam', document.getElementById('searchbar').value);
        document.getElementById("filters").submit();
    };
};
document.getElementById('sorter').onchange = function() {
    localStorage.setItem('selectedSort', document.getElementById('sorter').value);
    document.getElementById("filters").submit();
};
document.getElementById('order').onchange = function() {
    localStorage.setItem('selectedOrder', document.getElementById('order').value);
    document.getElementById("filters").submit();
};
document.getElementById('platform_select').onchange = function() {
    localStorage.setItem('selectedPlatform', document.getElementById('platform_select').value);
    document.getElementById("filters").submit();
};
document.getElementById('franchise_select').onchange = function() {
    localStorage.setItem('selectedFranchise', document.getElementById('franchise_select').value);
    document.getElementById("filters").submit();
};
document.getElementById('series_select').onchange = function() {
    localStorage.setItem('selectedSeries', document.getElementById('series_select').value);
    document.getElementById("filters").submit();
};
document.getElementById('genre_select').onchange = function() {
    localStorage.setItem('selectedGenre', document.getElementById('genre_select').value);
    document.getElementById("filters").submit();
};
document.getElementById('reset').onclick = function() {
    localStorage.setItem('searchParam', document.getElementById('searchbar').value = "");
    localStorage.setItem('selectedSort', document.getElementById('sorter').value = "title");
    localStorage.setItem('selectedOrder', document.getElementById('order').value = "asc");
    localStorage.setItem('selectedPlatform', document.getElementById('platform_select').value = "All");
    localStorage.setItem('selectedFranchise', document.getElementById('franchise_select').value = "All");
    localStorage.setItem('selectedSeries', document.getElementById('series_select').value = "All");
    localStorage.setItem('selectedGenre', document.getElementById('genre_select').value = "All");
    document.getElementById("filters").submit()
};
function main(sort_by){
    // This function populates the fields with previously stored values and is also responsible for controlling
    // the speed at which the game thumbnails populate the grid
    const items = document.querySelectorAll('.gameGridItem');
        var i = 0.3;
        items.forEach(item => {          
            item.style.animation = "slideFadeUp " + i + "s";
            if(i <= 1){
                i += 0.075;
            };
        })


        if(sort_by != "default"){
            document.getElementById("searchbar").value = localStorage.getItem('searchParam');
            document.getElementById("order").value = localStorage.getItem('selectedOrder');
            document.getElementById("sorter").value = localStorage.getItem('selectedSort');
            document.getElementById("platform_select").value = localStorage.getItem('selectedPlatform');
            document.getElementById("franchise_select").value = localStorage.getItem('selectedFranchise');
            document.getElementById("series_select").value = localStorage.getItem('selectedSeries');
            document.getElementById("genre_select").value = localStorage.getItem('selectedGenre');
        }
        else {
            localStorage.setItem('searchParam', document.getElementById('searchbar').value = "");
            localStorage.setItem('selectedSort', document.getElementById('sorter').value = "title");
            localStorage.setItem('selectedOrder', document.getElementById('order').value = "asc");
            localStorage.setItem('selectedPlatform', document.getElementById('platform_select').value = "All");
            localStorage.setItem('selectedFranchise', document.getElementById('franchise_select').value = "All");
            localStorage.setItem('selectedSeries', document.getElementById('series_select').value = "All");
            localStorage.setItem('selectedGenre', document.getElementById('genre_select').value = "All");
        };
    };
    // This part of the code is important in order to remove the sliding animations for the thumbnails after they have
    // slid up. Otherwise, the thumbnails would slide up every time they are dehighlighted by the user's cursor.
    setTimeout(function removeAnimations() {
        const items = document.querySelectorAll(".gameGridItem")

        items.forEach(item => {
            item.style.animation = "";
            
        });
    }, 1000);