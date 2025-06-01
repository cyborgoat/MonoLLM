# MonoLLM Documentation

This directory contains the Sphinx documentation for MonoLLM.

## Building the Documentation

### Prerequisites

- Python 3.12+
- Sphinx and related packages

### Installation

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser linkify-it-py mdit-py-plugins

# Or if using uv
uv pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser linkify-it-py mdit-py-plugins
```

### Building

```bash
# Build HTML documentation
cd docs
make html

# Build and watch for changes (if you have sphinx-autobuild)
pip install sphinx-autobuild
sphinx-autobuild . _build/html
```

### Viewing

After building, open `_build/html/index.html` in your browser, or serve it locally:

```bash
# Simple HTTP server
cd _build/html
python -m http.server 8000

# Then visit http://localhost:8000
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation page
├── installation.rst     # Installation guide
├── quickstart.rst       # Quick start guide
├── configuration.rst    # Configuration documentation
├── examples.rst         # Usage examples
├── cli.rst              # CLI documentation
├── api/                 # API reference
│   ├── client.rst       # Client API
│   ├── models.rst       # Data models
│   ├── providers.rst    # Provider implementations
│   └── exceptions.rst   # Exception classes
├── development/         # Developer documentation
│   ├── setup.rst        # Development setup
│   ├── contributing.rst # Contributing guide
│   ├── testing.rst      # Testing guide
│   └── providers.rst    # Provider development
├── _static/             # Static assets
│   ├── custom.css       # Custom CSS
│   ├── logo.png         # Logo
│   └── favicon.ico      # Favicon
└── _templates/          # Custom templates
```

## Writing Documentation

### reStructuredText (.rst)

Most documentation is written in reStructuredText format:

```rst
Section Title
=============

Subsection
----------

**Bold text** and *italic text*

Code blocks:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient

Lists:

* Item 1
* Item 2
* Item 3

Links:

:doc:`other-page`
:class:`~monollm.core.client.UnifiedLLMClient`
```

### Markdown (.md)

Some files use Markdown with MyST parser:

```markdown
# Section Title

## Subsection

**Bold text** and *italic text*

```python
import asyncio
from monollm import UnifiedLLMClient
```

- Item 1
- Item 2
- Item 3
```

### API Documentation

API documentation is auto-generated using Sphinx autodoc:

```rst
.. autoclass:: monollm.core.client.UnifiedLLMClient
   :members:
   :undoc-members:
   :show-inheritance:
```

## Contributing

1. **Edit documentation files** in the appropriate `.rst` or `.md` files
2. **Build locally** to test your changes: `make html`
3. **Check for warnings** and fix any issues
4. **Submit a pull request** with your changes

### Guidelines

- Use clear, concise language
- Include code examples for complex concepts
- Add cross-references to related sections
- Test all code examples
- Follow the existing structure and style

## Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

### Manual Deployment

If needed, you can deploy manually:

```bash
# Build documentation
make html

# Deploy to GitHub Pages (requires gh-pages branch setup)
# This is handled automatically by GitHub Actions
```

## Troubleshooting

### Common Issues

**Build errors:**
- Check that all dependencies are installed
- Verify Python path in `conf.py`
- Look for syntax errors in `.rst` files

**Missing modules:**
- Ensure MonoLLM is installed in development mode: `pip install -e .`
- Check that all imports in the source code are available

**Broken links:**
- Use `make linkcheck` to find broken external links
- Verify internal references with `:doc:` and `:ref:`

### Getting Help

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review existing documentation files for examples
- Ask questions in GitHub discussions

## Theme and Styling

The documentation uses the Read the Docs theme with custom CSS:

- **Theme**: `sphinx_rtd_theme`
- **Custom CSS**: `_static/custom.css`
- **Colors**: Blue primary (#2980B9), with accent colors
- **Features**: Responsive design, search, navigation

### Customizing

To modify the appearance:

1. Edit `_static/custom.css` for styling changes
2. Modify `conf.py` for theme options
3. Add custom templates in `_templates/` if needed

## Automation

### GitHub Actions

The `.github/workflows/docs.yml` workflow:

1. Builds documentation on every push
2. Deploys to GitHub Pages on main branch
3. Runs link checking and validation

### Local Development

For efficient local development:

```bash
# Install development dependencies
pip install sphinx-autobuild

# Auto-rebuild on changes
sphinx-autobuild . _build/html --open-browser
```

This will automatically rebuild and refresh your browser when files change. 