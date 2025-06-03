#!/usr/bin/env python3
"""
Automated Documentation Creation Tool
Ensures consistent file naming and structure for all agents.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import yaml
import re


class DocumentationCreator:
    """Creates documentation files with proper structure and metadata."""
    
    def __init__(self, framework_dir: str = None):
        if framework_dir:
            self.framework_dir = Path(framework_dir)
            # When framework_dir is provided, set project_docs relative to it
            self.project_docs_dir = self.framework_dir.parent / "project_docs"
        else:
            # Auto-detect framework directory and usage pattern
            current_dir = Path.cwd()
            if (current_dir / "agent-doc-system" / "framework").exists():
                # Nested usage: project_root/agent-doc-system/framework/
                self.framework_dir = current_dir / "agent-doc-system" / "framework"
                self.project_docs_dir = current_dir / "agent-doc-system" / "project_docs"
            elif (current_dir / "framework").exists():
                # Direct usage: framework as project root
                self.framework_dir = current_dir / "framework"
                self.project_docs_dir = current_dir / "project_docs"
            else:
                # Running from within framework directory
                self.framework_dir = current_dir
                self.project_docs_dir = current_dir.parent / "project_docs"
                
        self.templates_dir = self.framework_dir / "docs" / "templates"
        self.api_dir = self.framework_dir / "docs" / "api"
        self.components_dir = self.framework_dir / "docs" / "components"
        
    def sanitize_filename(self, name: str) -> str:
        """
        Convert a name to a safe filename.
        
        Examples:
            "My API Doc" -> "my_api_doc.md"
            "User's Guide" -> "users_guide.md"
            "Component: Auth" -> "component_auth.md"
        """
        # Convert to lowercase
        name = name.lower()
        
        # Replace special characters with underscores
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[-\s]+', '_', name)
        
        # Remove leading/trailing underscores
        name = name.strip('_')
        
        # Add .md extension if not present
        if not name.endswith('.md'):
            name += '.md'
            
        return name
    
    def create_document(self, doc_type: str, title: str, owner: str, 
                       description: str, location: str = None) -> Path:
        """
        Create a new documentation file with proper structure.
        
        IMPORTANT: Only DocSystemAgent can create files in framework/.
        Other agents are restricted to project_docs/ directory.
        
        Args:
            doc_type: Type of document (api, component, project, general)
            title: Document title
            owner: Document owner name
            description: Brief description
            location: Optional custom location (must be within project_docs/ for other agents)
            
        Returns:
            Path to created file
        """
        # Check agent permissions
        if owner != "DocSystemAgent":
            # Other agents can only create in project_docs/
            if doc_type in ["api", "component"]:
                raise PermissionError(f"Only DocSystemAgent can create {doc_type} documentation in framework/. "
                                    f"Other agents must use 'project' or 'general' type in project_docs/.")
            
            # Force location to project_docs for other agents
            if location and not str(location).startswith("project_docs"):
                raise PermissionError("Other agents can only create documentation in project_docs/ directory.")
        
        # Determine template and location based on agent permissions
        if owner == "DocSystemAgent":
            # DocSystemAgent can create anywhere
            if doc_type == "api":
                template_file = self.templates_dir / "api_template.md"
                default_location = self.api_dir
            elif doc_type == "component":
                template_file = self.templates_dir / "component_template.md"
                default_location = self.components_dir
            elif doc_type == "project":
                template_file = self.templates_dir / "project_template.md"
                default_location = self.project_docs_dir
            else:
                template_file = self.templates_dir / "project_template.md"
                default_location = self.project_docs_dir
        else:
            # Other agents restricted to project_docs
            template_file = self.templates_dir / "project_template.md"
            default_location = self.project_docs_dir
            
        # Use provided location or default
        target_dir = Path(location) if location else default_location
        
        # Final permission check for other agents
        if owner != "DocSystemAgent" and not str(target_dir.resolve()).endswith("project_docs"):
            raise PermissionError("Other agents can only create documentation in project_docs/ directory.")
            
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = self.sanitize_filename(title)
        target_path = target_dir / filename
        
        # Check if file already exists
        if target_path.exists():
            raise FileExistsError(f"File already exists: {target_path}")
            
        # Read template
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_file}")
            
        template_content = template_file.read_text()
        
        # Create schema-driven metadata
        metadata = self._create_schema_compliant_metadata(title, description, owner)
        
        # Generate YAML metadata
        yaml_metadata = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        
        # Create document content
        content = f"""# {title}

## Machine-Actionable Metadata
```yaml
{yaml_metadata}```

## Overview

{description}

## Key Features

<!-- TODO: Document the key features of {title} -->

1. **Feature 1**: Description
2. **Feature 2**: Description
3. **Feature 3**: Description

## Implementation

<!-- TODO: Add implementation details -->

### Architecture

Describe the architecture and design decisions.

### Configuration

Document any configuration requirements.

### Dependencies

List dependencies and requirements.

## Usage

<!-- TODO: Add usage examples -->

### Basic Usage

```python
# Example code here
```

### Advanced Usage

```python
# Advanced example here
```

### Common Patterns

Document common usage patterns and best practices.

## Troubleshooting

<!-- TODO: Add troubleshooting guide -->

### Common Issues

1. **Issue 1**: Solution
2. **Issue 2**: Solution

## API Reference

<!-- TODO: Add API documentation if applicable -->

## Changelog

- **1.0.0** ({datetime.now().strftime("%Y-%m-%d")}): Initial documentation

---

*Document created by {owner} using the Agent Documentation System*
"""
        
        # Write file
        target_path.write_text(content)
        
        return target_path
    
    def create_component_structure(self, component_name: str, owner: str) -> Path:
        """
        Create a complete component documentation structure.
        
        IMPORTANT: Only DocSystemAgent can create component structures in framework/.
        Other agents are restricted to project_docs/ directory.
        
        Args:
            component_name: Name of the component
            owner: Component owner
            
        Returns:
            Path to component directory
        """
        # Check permissions
        if owner != "DocSystemAgent":
            raise PermissionError("Only DocSystemAgent can create component structures in framework/. "
                                "Other agents must use 'project' type in project_docs/.")
        
        # Sanitize component name for directory
        safe_name = re.sub(r'[^\w\s-]', '', component_name.lower())
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        
        # Create component directory
        component_dir = self.components_dir / safe_name
        component_dir.mkdir(parents=True, exist_ok=True)
        
        # Create overview
        self.create_document(
            doc_type="component",
            title=f"{component_name} Component Overview",
            owner=owner,
            description=f"Overview of the {component_name} component",
            location=str(component_dir)
        )
        
        # Create API documentation if needed
        api_file = component_dir / "api.md"
        if not api_file.exists():
            self.create_document(
                doc_type="api",
                title=f"{component_name} API",
                owner=owner,
                description=f"API documentation for the {component_name} component",
                location=str(component_dir)
            )
        
        return component_dir
    
    def _load_schema(self) -> dict:
        """Load the document protocol schema."""
        schema_file = self.framework_dir / "schemas" / "document_protocol.yml"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        return yaml.safe_load(schema_file.read_text())
    
    def _create_schema_compliant_metadata(self, title: str, description: str, owner: str) -> dict:
        """
        Create metadata that is fully compliant with the document_protocol.yml schema.
        Pulls all field requirements and allowed values directly from the schema.
        """
        schema = self._load_schema()
        doc_schema = schema['document_schema']
        
        # Extract allowed values from schema
        status_values = doc_schema['properties']['metadata']['properties']['status']['enum']
        priority_values = doc_schema['properties']['feedback']['properties']['observations']['items']['properties']['priority']['enum']
        category_values = doc_schema['properties']['feedback']['properties']['observations']['items']['properties']['category']['enum']
        effort_values = doc_schema['properties']['feedback']['properties']['suggestions']['items']['properties']['effort']['enum']
        status_feedback_values = doc_schema['properties']['feedback']['properties']['status']['properties']['value']['enum']
        validation_values = doc_schema['properties']['feedback']['properties']['status']['properties']['validation']['enum']
        implementation_values = doc_schema['properties']['feedback']['properties']['status']['properties']['implementation']['enum']
        
        return {
            # METADATA Section - All Required Fields
            "metadata": {
                "schema": "https://schema.org/TechnicalDocument",
                "version": "1.0.0",
                "status": status_values[2],  # "Draft" 
                "owner": owner,
                "title": title,
                "description": description
            },
            
            # CONTENT Section - All Required Fields  
            "content": {
                "overview": description,
                "key_components": "TODO: List main components (Component1, Component2, Component3)",
                "sections": [
                    {
                        "title": "Overview", 
                        "content": f"{description} - expand with detailed information"
                    },
                    {
                        "title": "Key Features",
                        "content": "TODO: Document the main features and capabilities"
                    },
                    {
                        "title": "Implementation", 
                        "content": "TODO: Add implementation details, architecture, and design decisions"
                    },
                    {
                        "title": "Usage",
                        "content": "TODO: Provide usage examples, code snippets, and common patterns"
                    },
                    {
                        "title": "Configuration",
                        "content": "TODO: Document configuration options and requirements"
                    },
                    {
                        "title": "Troubleshooting", 
                        "content": "TODO: Add common issues and solutions"
                    }
                ],
                "changelog": [
                    {
                        "version": "1.0.0",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "changes": [
                            "Initial documentation created",
                            "Basic structure and metadata established",
                            "Ready for content development"
                        ]
                    }
                ]
            },
            
            # FEEDBACK Section - All Required Fields with Schema-Compliant Values
            "feedback": {
                "rating": 50,  # Initial rating (1-100 range per schema)
                "comments": f"Initial draft documentation for {title}. Ready for content development and enhancement.",
                "observations": [
                    {
                        "what": "Documentation structure created with proper schema compliance",
                        "impact": "Provides validated foundation for comprehensive documentation",
                        "priority": priority_values[2],  # "medium"
                        "category": category_values[0]   # "quality"
                    },
                    {
                        "what": "All required metadata fields populated according to schema",
                        "impact": "Ensures validation will pass and dashboard integration will work",
                        "priority": priority_values[3],  # "low"
                        "category": category_values[2]   # "usability"
                    }
                ],
                "suggestions": [
                    {
                        "action": "Fill in all TODO sections with detailed, comprehensive content",
                        "priority": priority_values[1],  # "high"
                        "effort": effort_values[2],      # "medium"  
                        "impact": priority_values[1],    # "high"
                        "assignee": owner
                    },
                    {
                        "action": "Add practical code examples and usage demonstrations",
                        "priority": priority_values[2],  # "medium"
                        "effort": effort_values[1],      # "small"
                        "impact": priority_values[2],    # "medium"
                        "assignee": owner
                    },
                    {
                        "action": "Include diagrams or visual aids where appropriate",
                        "priority": priority_values[3],  # "low"
                        "effort": effort_values[1],      # "small" 
                        "impact": priority_values[2],    # "medium"
                        "assignee": owner
                    },
                    {
                        "action": "Run validation and get AI feedback after content completion",
                        "priority": priority_values[1],  # "high"
                        "effort": effort_values[0],      # "minimal"
                        "impact": priority_values[1],    # "high" 
                        "assignee": owner
                    }
                ],
                "status": {
                    "value": status_feedback_values[0],         # "draft"
                    "updated_by": owner,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "validation": validation_values[2],         # "pending"
                    "implementation": implementation_values[3]  # "not_started"
                }
            }
        }


def main():
    """CLI interface for documentation creation."""
    parser = argparse.ArgumentParser(
        description="Create standardized documentation files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create project documentation (all agents can do this)
  python create_documentation.py project "My Project Overview" --owner "AgentName" --description "Overview of the project"
  
  # Create general documentation in project_docs (all agents)
  python create_documentation.py general "User Guide" --owner "AgentName" --description "User guide documentation"
  
  # Create API documentation (DocSystemAgent only)
  python create_documentation.py api "User Authentication API" --owner "DocSystemAgent" --description "REST API for user authentication"
  
  # Create component structure (DocSystemAgent only) 
  python create_documentation.py component "Database Handler" --owner "DocSystemAgent" --description "SQLite database operations"

Permission Notes:
  - Only DocSystemAgent can create 'api' and 'component' types in framework/
  - Other agents are restricted to 'project' and 'general' types in project_docs/
  - All metadata is schema-driven and validation-ready
        """
    )
    
    parser.add_argument(
        'type',
        choices=['api', 'component', 'project', 'general'],
        help='Type of documentation to create'
    )
    parser.add_argument(
        'title',
        help='Document title (will be sanitized for filename)'
    )
    parser.add_argument(
        '--owner',
        required=True,
        help='Document owner name'
    )
    parser.add_argument(
        '--description',
        required=True,
        help='Brief description of the document'
    )
    parser.add_argument(
        '--location',
        help='Custom location for the document (optional)'
    )
    
    args = parser.parse_args()
    
    try:
        creator = DocumentationCreator()
        
        if args.type == 'component' and not args.location:
            # Create complete component structure
            component_dir = creator.create_component_structure(
                component_name=args.title,
                owner=args.owner
            )
            print(f"✅ Created component structure at: {component_dir}")
            print(f"   - {args.title.lower().replace(' ', '_')}_component.md")
            print(f"   - {args.title.lower().replace(' ', '_')}_api.md")
        else:
            # Create single document
            file_path = creator.create_document(
                doc_type=args.type,
                title=args.title,
                owner=args.owner,
                description=args.description,
                location=args.location
            )
            print(f"✅ Created documentation file: {file_path}")
            
        print(f"\n📝 Next steps:")
        print(f"1. Edit the file to add detailed content")
        print(f"2. Run validation: ./framework/scripts/validate.sh")
        print(f"3. Get AI feedback: ./framework/scripts/enhanced_validate.sh --feedback")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()