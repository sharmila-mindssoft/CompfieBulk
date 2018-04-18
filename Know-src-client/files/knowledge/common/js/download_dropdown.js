$(document).ready(function() {
    $("body").tooltip({ selector: "[data-toggle=tooltip]" })
});

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function showDownloadList() {
    document.getElementById("myDropdown").classList.toggle("show");
    return false;
}
// Close the dropdown if the user clicks outside of it


/*$(".dl-xls-file, .dl-csv-file, .dl-ods-file, .dl-txt-file").on("click", function(){
    alert("Closeee");
    $(".dropdown-content", cloneRow).hide();
    $(".dropdown-content", cloneRow).removeClass("show");

});*/
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
// }

// Close the dropdown if the user clicks outside of it
// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {

//     var dropdowns = document.getElementsByClassName("dropdown-content");
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
//   }
// }