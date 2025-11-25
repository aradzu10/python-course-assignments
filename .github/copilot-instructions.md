# GitHub Copilot Instructions

## Project Overview

This repository contains Python course assignments organized by day. Each day focuses on different programming concepts and builds upon previous lessons.

## Coding Standards

### Python Style

- Follow PEP 8 conventions
- Use type hints for function parameters and return values (unless return type is None)
- Keep functions small and focused (single responsibility)
- Prefer clarity over cleverness

### Code Organization

- Separate logic from UI/presentation code
- Keep game logic in dedicated modules
- Keep UI/interaction code in main files
- Use simple, descriptive variable names
- Make global parameters in a configuration file or at the top of the relevant module

### Documentation

- Don't add docstrings to functions and classes
- Keep README files short and practical

### Simplicity Principles

- Prefer simple solutions over complex ones
- Avoid over-engineering or premature abstraction
- Remove unnecessary configuration - hardcode sensible defaults
- Use classes only when state management is needed

### Testing

- Write simple, focused tests
- Test core logic, not UI
- Use descriptive test names
- Keep test files alongside the code they test
