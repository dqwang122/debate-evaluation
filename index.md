---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: An Online Human Evaluation Platform for Debate Performance
---

You'll be evaluating a 20-minute debate where two sides discuss a topic. Your opinion matters - you'll vote both before and after listening the debate. We will use your feedback to improve the debate quality.

The debaters are AI agents or humans. These debates are divided into three stages: opening, rebuttal, and closing. You will be asked to complete a questionnaire, which includes your vote before and after the debate process on a predetermined topic. You need to compare the performance of each side in each stage. Finally, you can provide some optional feedback on how to improve the debate performance.

The process will take about 1 hour and a $30 Amazon gift card will be sent via email as a gift for your participation.

<ul>
  {% for file in site.static_files %}
    {% if file.path contains "forms/1214/pair" and file.extname == ".html" %}
      <li><a href="{{ site.baseurl }}/{{ file.path }}">Case {{ file.name | split: '.html' | first }}</a></li>
    {% endif %}
  {% endfor %}
</ul>
