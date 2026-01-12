# Contributing to GeoGuessr API Documentation

Thank you for your interest in contributing! This documentation is community-maintained and benefits from real-world testing and feedback.

## 🎯 Ways to Contribute

### 1. Report Issues
- Found incorrect information? Open an issue!
- Discovered a new endpoint? Let us know!
- Noticed outdated documentation? Tell us!

### 2. Submit Corrections
- Fix typos or formatting
- Update outdated information
- Correct field names or data structures

### 3. Add New Content
- Document new endpoints
- Add more code examples
- Create tutorials or guides
- Improve existing examples

### 4. Test and Verify
- Verify existing endpoints still work
- Test examples and report issues
- Share API testing results

## 📋 Contribution Guidelines

### Documentation Standards

All contributions should follow these standards:

#### 1. Verify with Real API Testing
- **Never** assume endpoint behavior
- Always test endpoints with real API calls
- Document exact request/response structures
- Include actual response examples from testing

#### 2. Include Complete Structures
- Use TypeScript interfaces for all data structures
- Document all fields (even if unused)
- Note field types accurately (string, number, boolean, object)
- Include nested structures completely

#### 3. Provide Working Examples
- Include both JavaScript and Python examples when possible
- Test examples before submitting
- Use clear, descriptive variable names
- Add comments explaining complex logic

#### 4. Document Edge Cases
- Note authentication requirements
- Document error responses (401, 403, 404, etc.)
- Mention deprecated or broken endpoints
- Include rate limiting information if known

#### 5. Follow File Structure
```
# Endpoint Documentation Format

## Overview
Brief description and key concepts

## Endpoints

### Endpoint Name
**Endpoint:** `METHOD /vX/path`
**Authentication:** Required/Not required
**Response:** Description

**Example Request:**
```language
code here
```

**Example Response:**
```json
{
  "field": "value"
}
```

**Important Notes:**
- Note 1
- Note 2
```

### Code Style

**JavaScript:**
- Use async/await (not promises)
- Use `fetch` API
- Include `credentials: 'include'` for authenticated requests
- Use descriptive function names
- Add JSDoc comments

**Python:**
- Use `requests` library
- Use `os.getenv()` for environment variables
- Include error handling
- Add docstrings
- Follow PEP 8

## 🔬 Testing Guidelines

Before submitting documentation for an endpoint:

1. **Test the endpoint** yourself using:
   - Browser developer console
   - Python script
   - Postman or similar tool

2. **Document what you find:**
   - Exact URL and HTTP method
   - Required headers
   - Request body structure
   - Response body structure
   - Status codes returned

3. **Test edge cases:**
   - What happens without authentication?
   - What happens with invalid parameters?
   - What happens when the resource doesn't exist?

4. **Save test results:**
   - Keep testing scripts for future verification
   - Note the date of testing
   - Document API version if available

## 📝 Pull Request Process

### 1. Before You Start
- Check existing issues and PRs to avoid duplicates
- Open an issue to discuss major changes
- Fork the repository

### 2. Making Changes
- Create a new branch: `git checkout -b feature/your-feature-name`
- Make your changes following our guidelines
- Test your changes thoroughly
- Update relevant documentation

### 3. Submitting
- Write clear commit messages
- Reference related issues
- Submit a pull request with:
  - Clear description of changes
  - Testing methodology
  - Screenshots/output if applicable

### 4. PR Review
- Address reviewer feedback
- Make requested changes
- Keep the PR up to date with main branch

## ✅ Checklist for New Endpoints

When documenting a new endpoint:

- [ ] Tested endpoint with real API calls
- [ ] Documented full request structure
- [ ] Documented full response structure
- [ ] Created TypeScript interfaces for data structures
- [ ] Added JavaScript example (browser console)
- [ ] Added Python example (script)
- [ ] Documented authentication requirements
- [ ] Tested error cases (401, 403, 404)
- [ ] Added notes about quirks or special behavior
- [ ] Updated relevant category file
- [ ] Added example to examples/ directory
- [ ] Updated examples/README.md

## 🔒 Security Considerations

### What NOT to Include
- **Never** commit real cookies or authentication tokens
- **Never** include real email addresses or passwords
- **Never** share personal user data
- **Never** include API keys or secrets

### What TO Include
- Placeholder values (e.g., `YOUR_COOKIE_VALUE`)
- Example data structures
- Anonymized response examples
- Security warnings where appropriate

## 📚 Documentation Structure

Our repository is organized as:
.
|-- README.md              # Main documentation
|-- authentication.md      # Auth endpoints
|-- challenges.md          # Challenge endpoints
|-- duels.md               # Duels endpoints (game-server API)
|-- feed.md                # Feed endpoints
|-- games.md               # Game endpoints
|-- maps.md                # Map endpoints
|-- profiles.md            # Profile endpoints
|-- social.md              # Social endpoints
|-- subscriptions.md       # Subscription endpoints
|-- websocket.md           # WebSocket API
|-- examples/
|   |-- README.md          # Examples guide
|   |-- javascript/        # JS examples by category
|   +-- python/            # Python examples by category
+-- tests/                 # Internal testing files
```

## 🎨 Writing Style

- Use clear, concise language
- Write in present tense
- Use active voice
- Be specific and technical
- Avoid assumptions
- Include context when needed

**Good:** "Returns an array of friend objects with userId field"
**Bad:** "Gets friends"

## 🐛 Reporting Bugs in Documentation

When reporting documentation issues:

1. **Be specific:** Quote the incorrect information
2. **Provide correct info:** Include verified API behavior
3. **Show your testing:** Share request/response examples
4. **Suggest a fix:** Propose updated documentation

## 💡 Suggesting Enhancements

We welcome suggestions for:
- New example types
- Additional documentation sections
- Improved organization
- Better explanations
- More use cases

Open an issue with:
- Clear description of enhancement
- Why it would be valuable
- Proposed implementation (if applicable)

## 🤝 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Provide constructive feedback
- Focus on the documentation quality
- Help others learn
- Give credit where due

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Unprofessional conduct

## 📞 Getting Help

- **Questions:** Open a GitHub issue
- **Discussions:** Use GitHub Discussions
- **Quick questions:** Check existing issues first

## 🙏 Recognition

Contributors will be:
- Listed in commit history
- Mentioned in release notes (for significant contributions)
- Appreciated by the community!

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (provided for educational purposes, respecting GeoGuessr's Terms of Service).

---

## Quick Start for Contributors

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-contribution`
3. Make your changes following guidelines above
4. Test thoroughly
5. Commit: `git commit -m "Add: description of changes"`
6. Push: `git push origin feature/my-contribution`
7. Create a Pull Request

---

**Thank you for contributing to the GeoGuessr API documentation! Your efforts help the entire community.** 🎉
