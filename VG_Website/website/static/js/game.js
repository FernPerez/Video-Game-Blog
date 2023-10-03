// This function is called by game.html to convert the Pythonic date value of the given game
// to a more readable traditional English style date.
function convertDates(date) {
    const months = ["January",
                    "February", 
                    "March", 
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"
                ];
    var releaseDate = date;
    var releaseMonth = parseInt(releaseDate.substring(5, 7));
    releaseMonth = months[releaseMonth - 1];
    var releaseDay = releaseDate.substring(8, 10);
    if(releaseDay[0] == "0"){
        releaseDay = releaseDay.replace("0", "");
    }
    releaseYear = releaseDate.substring(0, 4)
    // console.log(releaseMonth + " " + releaseDay + ", " + releaseYear);

    document.getElementById("release").innerText = ("Release Date: " + releaseMonth + " " + releaseDay + ", " + releaseYear);
};