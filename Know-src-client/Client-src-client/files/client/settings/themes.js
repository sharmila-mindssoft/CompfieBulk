$(function() {
    $('.themes-settings').click(function() {
        $('.themes-settings').removeClass('theme-active');
        $(this).addClass('theme-active');
        $('#theme_name').val($(this).attr('id'));
    });

    var theme_name = "";
    if (window.sessionStorage.theme_name)
        theme_name = window.sessionStorage.theme_name;
    else
        theme_name = "one";

    $(".themes-settings").each(function(index) {
        if ($(this).attr('id') === theme_name) {
            $(this).addClass('theme-active');
            $('#theme_name').val(theme_name);
        }
    });
});

function change_theme() {
    var theme_name = $('#theme_name').val();
    displayLoader();
    client_mirror.changeThemes(theme_name, function(error, response) {
        if (error == null) {
            window.sessionStorage.theme_name = response.theme;
            location.reload();
        } else {
            displayMessage(error);
        }
        hideLoader();
    });
}
''
