---
title: Posts
layout: base
#site-map: true
---

<ul>
{% for post in site.posts %}
  {% include post_summary.html post=post %}
{% endfor %}
<ul>
