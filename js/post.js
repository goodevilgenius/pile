---
---
var nav = document.querySelector('.meta .nav');
var next = nav.querySelector('[rel=next]');

var rand = document.createElement('a');
rand.setAttribute('rel','random');
rand.setAttribute('href', '#');
rand.textContent = "Random";

nav.insertBefore(rand,next);

nav.addEventListener("click", function() {
	var script = document.createElement('script');
	script.setAttribute('src', {{site.baseurl|append:'/js/posts.js'|jsonify}});
	
	var loadNewPage = function() {
		var pn = Math.floor(Math.random() * window.posts.length);
		window.location = window.posts[pn].url;
	};
	script.addEventListener("readystatechange", loadNewPage);
	script.addEventListener("load", loadNewPage);
	
	document.body.appendChild(script);
});
