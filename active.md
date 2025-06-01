---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---


## Current Action Versions:

<!-- Here are several IBM samples:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0117/admin" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul> -->


<!-- Here are several examples for expert debaters:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0511/expert" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul> -->


Here are several examples for full pairwise comparison:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0515/comparison" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>


Here are several examples for stage-wise comparison:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0515/mixed" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>


Here are several examples for common audience:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0511/common" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>