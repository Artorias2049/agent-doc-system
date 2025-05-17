# Agent Documentation System

A self-contained documentation system with machine-actionable metadata for projects.

## How to Use

1. **Install dependencies**:
   ```bash
   # Install node dependencies
   npm install -g remark-cli
   npm install remark-frontmatter remark-lint-frontmatter-schema js-yaml
   
   # Install Python dependencies
   pip install pyyaml
   ```

2. **Generate an example document**:
   ```bash
   ./agent_doc_system/scripts/generate_example_doc.py "Example Document" "This is an example document for testing" "Your Name"
   ```

3. **Validate documentation**:
   ```bash
   ./agent_doc_system/scripts/validate_docs.py
   ```

4. **Run full validation**:
   ```bash
   ./agent_doc_system/scripts/doc_validation.sh
   ```

## Setup Cursor Integration

To set up the Cursor integration files in your project:

```bash
# From your project root
./agent_doc_system/scripts/setup_cursor.sh

# OR specify a different target directory
./agent_doc_system/scripts/setup_cursor.sh /path/to/project
```

This will create all necessary `.cursor` files for the documentation system to work with Cursor, including:

- Documentation protocol rules
- Validation pipeline configuration
- Security rules
- Python expert agent rules for Python development assistance

The script also sets up VSCode configuration for better editor integration.

## Integration with Cursor

Cursor will automatically recognize the documentation protocol when you:

1. Create documentation in the `agent_doc_system/docs/` directory
2. Follow the documentation protocol with proper YAML metadata
3. Use section headers with anchor tags {#section-name}
4. Include language identifiers in code blocks
5. Maintain a changelog section

## VSCode Integration

The setup includes VSCode configuration that provides:
- Tasks for validating documentation and generating new documents
- Recommended extensions for working with Markdown and YAML
- Schema validation for documentation files
- Editor settings optimized for documentation work
- Cursor integration settings

## Moving the System

To use this system in another project:

1. Copy the entire `agent_doc_system/` folder to your new project
2. Run the setup script to create Cursor integration files:
   ```bash
   ./agent_doc_system/scripts/setup_cursor.sh
   ```
3. Start creating and validating documentation 