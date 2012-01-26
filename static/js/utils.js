$(document).ready(function(){
	
	// Django CSRF AJAX helper (https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax)
	$('html').ajaxSend(function(event, xhr, settings) {
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			// Only send the token to relative URLs i.e. locally.
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
	});
	
	
	// post commentForm
	$("#commentForm").submit(function() {
		// serialize comment form
		var commentData = $("#commentForm").serialize();
		// comment content
		var commentTxt = $("#id_comment").val();
		$.ajax({
			type: "POST",
			url: "/comments/post/",
			data: commentData,
			success: function(msg){
				$("ul.comments").append("<li><a href='#' class='title'>You</a>: " + commentTxt + "<div class='meta'>Posted just now</div></li>");
				if ($("h3.comments").length === 0) { 
					// insert the header in case of first comment
					$("ul.comments").before("<h3 class='comments'>Discussion:</h3>");
				}
				// empty textarea
				$("#id_comment").val("");
			}
		}).responseText;
		// don't really POST
		return false;
	});

});

// star rating
var init_rating = function (start_score, readonly, img_path, item_id) {
	$('#rating').raty({
		readOnly: readonly,
		start: start_score,
		path: img_path,
		click: function(score, evt) {
			$.post('/rate/item/' + item_id,
				{
					score: score, 
				}
				// no success handler required, 
				// raty plugin provides good visual feedback
			)
			.error(
				function() { 
					// cancel the rating, no stars highlighted
					$.fn.raty.cancel('#rating');
				}
			);
		  }
	});
}