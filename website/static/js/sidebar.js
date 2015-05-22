window.onscroll = function()
{
	if( window.XMLHttpRequest ) { // IE 6 doesn't implement position fixed nicely...
		if ($(window).scrollTop() > "46") {
			document.getElementById('wiki_panel').style.position = 'absolute'; 
			document.getElementById('wiki_panel').style.top = '46px';
			document.getElementById('wiki_panel').style.right = '15px';
		} else {
			document.getElementById('wiki_panel').style.position = 'absolute'; 
			document.getElementById('wiki_panel').style.top = 'auto';
		}
	}
}


