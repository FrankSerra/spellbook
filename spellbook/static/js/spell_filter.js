//loading bar
var timer;

$(document).on('keypress', '#namesearch', function(event) {
	if ( event.which == 13 ) {
		addSpellParameter('name', $('#namesearch').val(), true, false);
	}
});

$(document).ajaxStart(function() {
  timer = setTimeout(function() {
	  startLoad();
  }, 350);
});

$(document).ajaxStop(function() {
  clearTimeout(timer);
  stopLoad();
});

function startLoad() {
	$(".page").css("opacity", 0.2);	
	$("#loadingbar").css("display","block");
}

function stopLoad() {
	$("#loadingbar").css("display","none");
	$(".page").css("opacity", 1);
}

//spellbook buttons
function addSpellbook(elem, spellid) {
	doSpellbookchange(elem, encodeURIComponent(spellid), "add");
}

function removeSpellbook(elem, spellid) {
	doSpellbookchange(elem, encodeURIComponent(spellid), "remove");
}

function doSpellbookchange(elem, spellid, action) {
	url = "";
	if(action == "add")
	  url = $SCRIPT_ROOT + '/addspell/' + spellid + window.location.search;
	else if(action == "remove")
	  url = $SCRIPT_ROOT + '/removespell/' + spellid + window.location.search;

	if(url != "" && spellid != "")
	{
	  $.get(url, function( data ) { 
		  $(elem).parent('li').html( data['data'] ); 
		});
	}
}

//spell filters
function addSpellParameter(key, value, main=true, nav=true) {
	if(key == 'name')
	{
		if(value == '') 
		{
			removeSpellParameter(key, main, nav);
			return;
		}
	}
	else if (value == 'None')
	{
		removeSpellParameter(key, main, nav);
		return;
	}
	
	var queryParameters = {}, 
			queryString = window.location.search.substring(1),
			re = /([^&=]+)=([^&]*)/g, m;
	
	while (m = re.exec(queryString)) { queryParameters[decodeURIComponent(m[1])] = decodeURIComponent(m[2]); }

	queryParameters[key] = value;

	doSpellFilter($.param(queryParameters), main, nav);
	
}

function removeSpellParameter(key, main=true, nav=true) {
	var queryParameters = {}, 
			queryString = window.location.search.substring(1),
    	re = /([^&=]+)=([^&]*)/g, m;
	
	while (m = re.exec(queryString)) { 
		if(m[1] != key)	
			queryParameters[decodeURIComponent(m[1])] = decodeURIComponent(m[2]); 
	}
	
	doSpellFilter($.param(queryParameters), main, nav);
}

function doSpellFilter(newquerystring, main, nav) {
	if(newquerystring != "")
		newquerystring = "?" + newquerystring;

	history.pushState(null, null, window.location.pathname + newquerystring);

	if(main) {
		url = $SCRIPT_ROOT + '/spellfilter' + newquerystring;
		$.get(url, function( data ) { 
			$("#mainbodydiv").html( data['data'] );
		});
	}

	if(nav) {
		url = $SCRIPT_ROOT + '/spellfilternav' + newquerystring;
		$.get(url, function( data ) { 
			$("#spellfilternav").html( data['data'] ); 
		});
	}
}