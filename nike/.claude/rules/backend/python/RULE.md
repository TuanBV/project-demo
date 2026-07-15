---
paths:
  - "api/**/*.py"
  - "worker/**/*.py"
  - "queue/**/*.py"
  - "storage/**/*.py"
---
# Python Rules
- Target Python 3.11 and add type hints to public functions and service/repository boundaries.
- Avoid mutable default arguments, broad `except Exception`, and `print` for application logging.
- Raise domain exceptions from services and translate them once at the HTTP boundary.
- Keep imports acyclic and remove copied constants/enums from unrelated systems.
