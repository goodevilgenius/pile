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

head.appendChild(rand);

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
			case "day":
				var d = new Date(p.date);
				var ymd = "" + d.getFullYear() + (d.getMonth() < 9 ? "-0" : "-") + (d.getMonth()+1) + (d.getDate() < 10 ? "-0" : "-") + d.getDate();
				return ymd == head.dataset.archiveYearMonthDay;
			case "month":
				var d = new Date(p.date);
				var ym = "" + d.getFullYear() + (d.getMonth() < 9 ? "-0" : "-") + (d.getMonth()+1);
				return ym == head.dataset.archiveYearMonth;
			case "year":
				var d = new Date(p.date);
				return d.getFullYear() == head.dataset.archiveYear;
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
