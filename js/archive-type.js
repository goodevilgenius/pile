---
---
var head = document.querySelector('#main > h1');
var type = head.dataset.archive;

var rand = document.createElement('a');
rand.setAttribute('rel','random');
rand.setAttribute('href', '#');
rand.className = 'post-random';
var img = document.createElement('img');
img.className = "icon";
rand.appendChild(img);

if (type == "tag" || type == "type") head.appendChild(rand);

rand.addEventListener("click", function() {
	var loadNewPage = function() {
		var newposts = window.posts.filter(function(p){
			switch (type) {
			case "tag":
				return p.tags.includes(head.dataset.archiveTag);
				break;
			case "type":
				return p.type == head.dataset.archiveType;
				break;
			default:
				return false;
			}
		});
		var pn = Math.floor(Math.random() * newposts.length);
		window.location = newposts[pn].url;
	};

	var script = document.createElement('script');
	script.setAttribute('src', {{site.baseurl|append:'/js/posts.js'|jsonify}});
	script.addEventListener("readystatechange", loadNewPage);
	script.addEventListener("load", loadNewPage);
	
	document.body.appendChild(script);
});
