// The purpose of this function is to populate the fields in the update_game.html page with the current 
// genre and gameCover fields so the user does not have to enter them every time.
function main(genres, cover) {
    genres = genres.replaceAll('"', '');
    genres = genres.replaceAll('[', '');
    genres = genres.replaceAll(']', '');
    genres = genres.replaceAll(' ', '');
    genres = genres.split(',');

    console.log(genres);

    document.getElementById("genre1").value = genres[0];
    if(genres[1] == '') {
        document.getElementById("genre2").value = 'N/A';
    }
    else {
        document.getElementById("genre2").value = genres[1];
    }
    if(genres[2] == '') {
        document .getElementById("genre3").value = 'N/A';
    }
    else {
        document.getElementById("genre3").value = genres[2];
    }
    document.getElementById("gameCover").value = cover
}