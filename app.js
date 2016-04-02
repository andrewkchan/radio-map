$(document).ready(function() {
	$('.roadtrip').fadeOut(0);
	$('#landing-hits').click(function() {
		$('.landing').hide();
		$('.roadtrip').show();
		$('html').css('background-color', 'white');
		$('body').css('background-color', 'white');
	});
	$('#landing-logo').click(function() {
		('.roadtrip').hide();
		('.landing').show();
		$('html').css('background-color', '#27ae60');
		$('body').css('background-color', '#27ae60');
	})
});

function showRoadtrip() {

}

// var screenHeight = $(window).height(); 
// var row = $('.row');

// // Assign that height to the .row
// row.css({
//     'height': screenHeight + 'px',
// });

// // This makes the div's height responsive when you resize the screen or the window of the browser.
// $(window).resize(function () {
//     screenHeight = $(window).height();
//     row.css({
//         'height': screenHeight + 'px',
//     });
// });