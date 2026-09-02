import re

with open('portfolio/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove budget from models.py
content = re.sub(r'    budget = models\.CharField\(.*?\)\n', '', content)

with open('portfolio/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('portfolio/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove budget from serializers.py
content = content.replace("'budget', ", "")

with open('portfolio/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('portfolio/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove budget from views.py
content = re.sub(r'Budget: \{message_obj\.budget\}\n', '', content)

with open('portfolio/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
