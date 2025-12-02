import re

# Read the file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the cost display section
old_pattern = r'</div>\s*<h3 class="card-text text-primary">{{ sub\.cost \| usd }}<small\s*class="text-muted fs-6">/mo</small></h3>'

new_code = '''</div>
                        {% if sub.billing_cycle == 'Weekly' %}
                        <h3 class="card-text text-primary">{{ sub.cost | usd }}<small class="text-muted fs-6">/week</small></h3>
                        <p class="text-muted mb-0"><small>≈ {{ sub.monthly_cost | usd }}/month</small></p>
                        {% elif sub.billing_cycle == 'Quarterly' %}
                        <h3 class="card-text text-primary">{{ sub.cost | usd }}<small class="text-muted fs-6">/quarter</small></h3>
                        <p class="text-muted mb-0"><small>≈ {{ sub.monthly_cost | usd }}/month</small></p>
                        {% elif sub.billing_cycle == 'Annually' %}
                        <h3 class="card-text text-primary">{{ sub.cost | usd }}<small class="text-muted fs-6">/year</small></h3>
                        <p class="text-muted mb-0"><small>≈ {{ sub.monthly_cost | usd }}/month</small></p>
                        {% else %}
                        <h3 class="card-text text-primary">{{ sub.cost | usd }}<small class="text-muted fs-6">/month</small></h3>
                        {% endif %}'''

content = re.sub(old_pattern, new_code, content)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully!")
