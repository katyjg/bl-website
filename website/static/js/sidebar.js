window.onscroll = function()
{
	if( window.XMLHttpRequest ) { // IE 6 doesn't implement position fixed nicely...
		if ($(window).scrollTop() > "0") {
			document.getElementById('wiki_panel').style.position = 'fixed'; 
			document.getElementById('wiki_panel').style.top = '58px';
			document.getElementById('wiki_panel').style.right = '15px';
			$("#wiki_panel").css("padding-left", "15px");
			$("#wiki_panel").addClass('col-sm-3 col-xs-4');
		} else {
			document.getElementById('wiki_panel').style.position = 'absolute'; 
			document.getElementById('wiki_panel').style.top = 'auto';
			$("#wiki_panel").removeClass('col-sm-3 col-xs-4');
		}
	}
}


