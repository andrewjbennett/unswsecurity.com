---
title: Posts
layout: base
site-map: true
---

<ul>
{% for post in site.posts %}
  <li>
    <p><a href="{{ post.url | absolute-url }}">{{ post.title }}</a></p>
    <ul>
    {% for category in post.categories %}
      <li>{{ category }}</li>
    {% endfor %}
    </ul>
  </li>
{% endfor %}
<ul>
