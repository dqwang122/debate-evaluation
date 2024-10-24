---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: An Online Human Evaluation Platform for Debate Performance
---

<!-- ## Debate Performance Evaluation

You'll review a recorded 20-minute debate between two debaters (humans or AI debaters) and evaluate the performance of each side. 
You will be asked to complete a questionnaire, which includes your vote before and after the debate process on a predetermined topic. 
There are three stages (openining, rebuttal, and closing) in the debate process. There are also several fine-grained aspects and you will need to rate the performance between 1 to 5 for each side
Finally, you will rate the performance of each side in the entire debate process and provide some optional feedback.

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/1020/scalar" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul> -->

## Debate Pair Comparison

You'll review a recorded 20-minute debate between two debaters (humans or AI debaters) and evaluate the performance of each side. 
You will be asked to complete a questionnaire, which includes your vote before and after the debate process on a predetermined topic. 
There are three stages (openining, rebuttal, and closing) in the debate process. You need to compare the performance of each side in each stage.
Finally, you will rate the performance of each side in the entire debate process and provide some optional feedback.

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/1020/pair" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
