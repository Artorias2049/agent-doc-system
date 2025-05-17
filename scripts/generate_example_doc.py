#!/usr/bin/env python3
# agent_doc_system/scripts/generate_example_doc.py

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Get the directory where the script is located
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# Get the parent directory (agent_doc_system)
parent_dir = script_dir.parent

def generate_example_doc(title, description, author):
    """Generate an example document following the documentation protocol."""
    
    # Create a sanitized filename from the title
    filename = title.lower().replace(' ', '_') + '.md'
    filepath = parent_dir / 'docs' / filename
    
    # Make sure the docs directory exists
    docs_dir = parent_dir / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Generate current date in ISO format
    date_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    date_simple = datetime.now().strftime("%Y-%m-%d")
    
    # Generate document content
    content = f"""# {title} {{#document}}

## Machine-Actionable Metadata
```yaml
schema: "https://schema.org/TechnicalDocument"
id: "doc-{int(time.time())}"
version: "0.1.0"
last_updated: "{date_iso}"
status: "Draft"
author: "{author}"
```

## Overview {{#overview}}

{description}

## Content {{#content}}

This is an example document that follows the documentation protocol.
Replace this content with your actual documentation.

### Code Example {{#code-example}}

```python
def hello_world():
    print("Hello, world!")
    return True
```

## Changelog {{#changelog}}

- **0.1.0** ({date_simple}): Initial draft by {author}
"""
    
    # Write the document to a file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Example document created at: {filepath}")
    return filepath

def main():
    if len(sys.argv) < 4:
        print("Usage: generate_example_doc.py \"Title\" \"Description\" \"Author\"")
        sys.exit(1)
    
    title = sys.argv[1]
    description = sys.argv[2]
    author = sys.argv[3]
    
    generate_example_doc(title, description, author)

if __name__ == "__main__":
    main() 