window.onscroll = function()
{
	if( window.XMLHttpRequest ) { // IE 6 doesn't implement position fixed nicely...
		if ($(window).scrollTop() > "154") {
			document.getElementById('wiki_panel').style.position = 'fixed'; 
			document.getElementById('wiki_panel').style.top = '0';
		} else {
			document.getElementById('wiki_panel').style.position = 'absolute'; 
			document.getElementById('wiki_panel').style.top = 'auto';
		}
	}
}


