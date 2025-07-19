# 🧠 Python Code Style & Project Guidelines

> 🔤 **Nota importante:** Todo el código debe escribirse en **inglés**: nombres de variables, funciones, clases, comentarios, docstrings, pruebas y documentación del proyecto.  
> 💬 Sin embargo, todas nuestras conversaciones (como esta guía) pueden mantenerse en **español**.

---

## ✅ General Principles

- Write clean, readable, and **well-structured code**
- Use **snake_case** for variables and functions
- Use **PascalCase** for class names
- Include **simple and clear docstrings** for all public classes and functions
- Use comments **only when necessary**, placed **above** the code they describe
- Avoid code duplication (**DRY principle**)
- Always consider **separation of environments**: development, testing, production
- Design code to be **modular, scalable, and maintainable**
- Use meaningful and descriptive names

---

## 🐍 Virtual Environments

- Always create isolated virtual environments to manage dependencies.
- Use the following command to create a virtual environment:

```bash
python3 -m venv venv
```

- Activate the environment before installing packages:
  - On Linux/macOS: `source venv/bin/activate`

---

## 🗂️ Project Structure

```text
my_project/
├── app/               # Main application code
│   ├── __init__.py
│   ├── module_a.py
│   └── module_b.py
├── tests/             # Pytest-based tests
│   ├── __init__.py
│   └── test_module_a.py
├── configs/           # Environment-specific settings
│   ├── dev_config.py
│   ├── test_config.py
│   └── prod_config.py
├── utils/             # Reusable helper functions
├── .env               # Environment variables (excluded from Git)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🔬 Testing Standards

- Always use **pytest**
- Use **clear, English-based function names** for test cases
- Use **fixtures** to avoid repetition and setup logic
- Delete all **temporary files** generated during tests (e.g., debug logs, mock files)

```python
def test_area_calculation() -> None:
    """Should return correct area for a given radius."""
    result = calculate_area(2)
    assert round(result, 2) == 12.57
```

---

## 🌎 Environment Awareness

- Use `.env` files and `python-dotenv` to manage sensitive configurations
- Clearly separate logic by environment: dev, test, prod

```python
import os

ENV = os.getenv("APP_ENV", "development")

if ENV == "production":
    from configs.prod_config import *
elif ENV == "testing":
    from configs.test_config import *
else:
    from configs.dev_config import *
```

---

## 🧹 Clean Code Practices

- Use `black` and `isort` to format and organize imports
- Lint with `flake8` or `ruff`
- Use `pre-commit` to automate checks on each commit
- Follow the **Single Responsibility Principle**
- Delete all **debug prints**, **temporary files**, or **unused code** before committing

---

## 📄 Docstrings and Comments

- Keep all **docstrings in English**
- Use short and clear documentation following Google style:

```python
def fetch_user(user_id: int) -> dict:
    """Return user data by ID.

    Args:
        user_id (int): The user's unique identifier.

    Returns:
        dict: User data dictionary.
    """
```

---

## 🚫 Avoid

- Hardcoded values (paths, credentials, settings)
- Deeply nested logic or functions longer than 50 lines
- Repetition of logic (use reusable functions)
- Mixing code responsibilities in a single file

---

## 📚 Documentation Guidelines

- Use Markdown `.md` files in English
- Always include an up-to-date `README.md`
- Explain setup, environment configuration, running the app, and testing

---

## ✅ Summary

| Aspect                | Tool / Practice         |
|-----------------------|-------------------------|
| Language              | English only in code    |
| Code formatting       | `black`, `isort`        |
| Linting               | `flake8`, `ruff`        |
| Testing               | `pytest`                |
| Hooks                 | `pre-commit`            |
| Environments          | `.env` + config modules |
| Documentation         | Markdown + docstrings   |
| Project structure     | Modular folder layout   |
| Temporary files       | Delete after use        |

---
