---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

**An Online Human Evaluation Platform for Debate Performance**

You'll be evaluating a 20-minute debate where two sides discuss a topic. Your opinion matters - you'll vote both before and after listening the debate. We will use your feedback to improve the debate quality.

The debaters are AI agents or humans. These debates are divided into three stages: opening, rebuttal, and closing. You will be asked to complete a questionnaire, which includes your vote before and after the debate process on a predetermined topic. You need to compare the performance of each side in each stage. Finally, you can provide some optional feedback on how to improve the debate performance.

<!-- Here are several IBM samples:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0117/admin" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul> -->


Here are several examples for expert debaters:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0331/expert" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>


Here are several examples for full pairwise comparison:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0331/comparison" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>


Here are several examples for single stage-wise comparison:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0331/mixed" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>


Here are several examples for common audience:

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/0320/common" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>