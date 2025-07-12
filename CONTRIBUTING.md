# Contributing to AI Agents System

Thank you for your interest in contributing to AI Agents System! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features
- **Code Contributions**: Submit pull requests
- **Documentation**: Improve or add documentation
- **Testing**: Write or improve tests
- **Translation**: Help with internationalization

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- Git installed
- Docker and Docker Compose (for full system testing)
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)
- PostgreSQL (for local development)

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/agent_ia.git
   cd agent_ia
   ```

2. **Set up the development environment**
   ```bash
   # Start all services
   ./scripts/up_all.sh
   
   # Or set up individually
   cd backend && python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   
   cd ../frontend
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   # Edit the .env files with your configuration
   ```

## 📝 Development Guidelines

### Code Style

#### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 88 characters (Black formatter)

```bash
# Format code
black .
isort .

# Lint code
flake8
mypy .
```

#### Frontend (JavaScript/React)
- Follow ESLint configuration
- Use Prettier for formatting
- Use functional components with hooks
- Follow React best practices

```bash
# Format and lint
npm run lint
npm run lint:fix
```

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add OAuth2 support
fix(api): resolve database connection issue
docs(readme): add troubleshooting section
```

### Testing

#### Backend Testing
```bash
cd backend
pytest
pytest --cov=app
pytest --cov=app --cov-report=html
```

#### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend && pytest
   
   # Frontend tests
   cd frontend && npm test
   
   # Full system test
   ./scripts/verify_setup.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use the PR template
   - Describe your changes clearly
   - Link any related issues
   - Request reviews from maintainers

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, browser, versions
- **Screenshots**: If applicable
- **Logs**: Error logs and stack traces

## 💡 Feature Requests

When requesting features, please include:

- **Description**: Clear description of the feature
- **Use case**: Why this feature is needed
- **Proposed solution**: How you think it should work
- **Alternatives**: Any alternatives you've considered

## 📚 Documentation

### Adding Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update API documentation if endpoints change
- Add examples for new features

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up to date

## 🔒 Security

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do NOT** create a public issue
2. Email the maintainers directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed

### Security Guidelines

- Never commit sensitive information (API keys, passwords)
- Use environment variables for configuration
- Validate all user inputs
- Follow security best practices

## 🏷️ Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

Before releasing:

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version numbers are updated
- [ ] Security review completed
- [ ] Performance testing completed

## 🎯 Areas for Contribution

### High Priority
- Bug fixes
- Security improvements
- Performance optimizations
- Documentation improvements

### Medium Priority
- New AI model integrations
- UI/UX improvements
- Additional API endpoints
- Testing improvements

### Low Priority
- New features
- Refactoring
- Code style improvements

## 📞 Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact maintainers directly for security issues

## 🙏 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI Agents System! 🚀 