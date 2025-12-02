import re

# Read the file
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the issue - replace the problematic lines
# The issue is on line 128-129
# From: const entSpent = {{ent_spent }
#     };
# To: const entSpent = {{ ent_spent }};

# Use multiline regex to fix
old_pattern = r'const entSpent = \{\{ ent_spent \}\r?\n\s+\};'
new_pattern = 'const entSpent = {{ ent_spent }};'

content = re.sub(old_pattern, new_pattern, content)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File fixed successfully!")
