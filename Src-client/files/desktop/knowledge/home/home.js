function initialize(){
	function onSuccess(data){
		loadNotificationList(data["notifications"]);
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.getNotifications( "Notification",
		function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        }
	);
}
function loadNotificationList(list){
 	$(".notification-ul").find("li").remove();
 	var notificationtext;
 	var notificationtime;
 	if(list.length == 0){
 		$(".notification-container").hide();
 	}
 	else{
 		$.each(list, function(k, value){
			notificationtext = list[k]["notification_text"];
			notificationtime = list[k]["date_and_time"];			
			var tableRow = $('#templates .list');
			var clone = tableRow.clone();
			$('.notification-text', clone).text(notificationtext);
			$('.notification-time', clone).text(notificationtime);
			$('.notification-container .notification-ul').append(clone);
		});	
 	}
}
$(function() {
	initialize();
});