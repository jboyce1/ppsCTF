<ol class="season-list">
{% for event in site.data.season %}
  <li id="{{ event.id }}" class="season-row{% if event.kind == 'break' %} season-break{% endif %}" data-start="{{ event.start }}" data-end="{{ event.end }}" data-kind="{{ event.kind }}">
    <div class="session-date"><strong>{{ event.date }}</strong><span>{{ event.time }}</span><span class="session-marker" hidden></span></div>
    <div class="session-info"><h3 class="session-title">{{ event.title }}</h3>{% if event.description != '' %}<p>{{ event.description }}</p>{% endif %}</div>
    {% if event.links.size > 0 %}<div class="session-resources">{% for link in event.links %}<a href="{{ link.url | relative_url }}">Open {{ link.label }} →</a>{% endfor %}</div>{% endif %}
  </li>
{% endfor %}
</ol>
