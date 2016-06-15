---
---
window.posts = window.posts || [];
{% for post in site.posts %}
posts.push({
    "title":{{post.title|jsonify}},
    "url":{{post.url|prepend:site.baseurl|prepend:site.url|jsonify}},
	"type":{{post.type|jsonify}},
	"tags":{{post.tags|jsonify}}
});
{% endfor %}
