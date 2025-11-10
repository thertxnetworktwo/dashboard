# Contributing to Telegram Bot Dashboard

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit and push
7. Create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd dashboard

# Run setup
./dashboard.sh setup

# Start development
./dashboard.sh start
```

## Code Style Guidelines

### Python (Backend)

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Type hints are encouraged
- Maximum line length: 100 characters

Example:
```python
def check_phone(phone_number: str) -> Dict[str, Any]:
    """
    Check if a phone number exists in the registry.
    
    Args:
        phone_number: Phone number to check (e.g., "+1234567890")
    
    Returns:
        Dictionary with existence status and registration timestamp
    """
    # Implementation
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow ESLint rules
- Use functional components with hooks
- Type all props and state
- Use meaningful component names

Example:
```typescript
interface ProductProps {
  product: Product;
  onUpdate: (id: number) => void;
}

export const ProductCard: React.FC<ProductProps> = ({ product, onUpdate }) => {
  // Implementation
};
```

### CSS/Styling

- Use Tailwind CSS utility classes
- Follow mobile-first approach
- Ensure responsive design
- Test on multiple screen sizes

## Testing

### Backend Tests

Run tests before submitting:
```bash
cd backend
source venv/bin/activate
python manage.py test

# Or with pytest
pytest

# With coverage
coverage run -m pytest
coverage report
```

Write tests for:
- New models
- New API endpoints
- Business logic
- Utility functions

### Frontend Tests

```bash
cd frontend
npm test
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(products): add bulk delete functionality

Add ability to delete multiple products at once through the UI
and API endpoint.

Closes #123
```

```
fix(phone-registry): handle timeout errors gracefully

Add proper error handling for timeout scenarios when calling
external API. Show user-friendly error message.

Fixes #456
```

## Pull Request Process

1. **Update Documentation**: If you add features, update README.md and API.md
2. **Add Tests**: Ensure your changes are tested
3. **Run Linters**: Fix any linting errors
4. **Update Changelog**: Add your changes to CHANGELOG.md (if exists)
5. **Request Review**: Tag maintainers for review

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No console errors or warnings
- [ ] Tested on multiple browsers (frontend changes)
- [ ] Backward compatible (or breaking changes documented)

## Areas for Contribution

### High Priority

- [ ] Additional unit tests
- [ ] Integration tests
- [ ] Performance optimizations
- [ ] Accessibility improvements
- [ ] Mobile UI enhancements

### Feature Requests

- [ ] User authentication system
- [ ] Role-based access control
- [ ] Email notifications for expiring products
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Export to Excel format
- [ ] Webhook support
- [ ] API rate limiting

### Documentation

- [ ] Video tutorials
- [ ] More code examples
- [ ] Troubleshooting guide expansion
- [ ] Architecture diagrams
- [ ] API client libraries

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. Submit PR with clear description
2. Address reviewer comments
3. Maintainer approves and merges

## Bug Reports

### Before Submitting

- Check existing issues
- Verify it's reproducible
- Test with latest version

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.10]
- Node version: [e.g., 18.0]
- Browser: [e.g., Chrome 90]

**Additional context**
Any other relevant information.
```

## Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features.

**Additional context**
Any other context or screenshots.
```

## Development Tips

### Backend Development

```bash
# Run development server with auto-reload
cd backend
source venv/bin/activate
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Django shell for testing
python manage.py shell
```

### Frontend Development

```bash
# Run dev server with hot reload
cd frontend
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

### Database

```bash
# Access PostgreSQL
psql dashboard_db

# Reset database (development only!)
dropdb dashboard_db
createdb dashboard_db
python manage.py migrate
python manage.py loaddata apps/products/fixtures/sample_products.json
```

## Questions?

- Open an issue for general questions
- Join our community chat (if available)
- Email maintainers directly for private matters

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers.

---

Thank you for contributing! 🎉
