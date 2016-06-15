---
---
var nav = document.querySelector('.meta .nav');
var next = nav.querySelector('[rel=next]');

var rand = document.createElement('a');
rand.setAttribute('rel','random');
rand.setAttribute('href', '#');
rand.className = 'post-random';
var img = document.createElement('img');
img.className = "icon";
rand.appendChild(img);

nav.insertBefore(rand,next);

rand.addEventListener("click", function() {
	var loadNewPage = function() {
		var pn = Math.floor(Math.random() * window.posts.length);
		window.location = window.posts[pn].url;
	};

	var script = document.createElement('script');
	script.setAttribute('src', {{site.baseurl|append:'/js/posts.js'|jsonify}});
	script.addEventListener("readystatechange", loadNewPage);
	script.addEventListener("load", loadNewPage);
	
	document.body.appendChild(script);
});
