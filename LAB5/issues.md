\# Static Code Analysis – Gym Membership System



\## 1. Introduction



The Gym Membership System Python program was analyzed using three static code analysis tools:



\- Pylint – checks code quality, naming conventions, and programming practices.

\- Bandit – identifies potential security vulnerabilities.

\- Flake8 – checks Python coding style and formatting.



\## 2. Issues Identified and Fixes



| Tool | Original issue | Correction made |

|---|---|---|

| Pylint | Missing function docstrings | Added docstrings to functions |

| Pylint | Function names not following snake\_case | Renamed functions using snake\_case |

| Pylint | Mutable default argument `\[]` | Replaced with `None` |

| Pylint | Unused variables and imports | Removed unnecessary variables and imports |

| Pylint | Use of `eval()` | Replaced with normal arithmetic |

| Pylint | Missing final newline | Added final newline |

| Bandit | Use of `eval()` | Replaced with safe arithmetic |

| Bandit | Weak MD5 hashing | Replaced with SHA-256 |

| Bandit | Insecure random number generation | Replaced `random` with `secrets` |

| Bandit | Use of `os.system()` | Removed shell command execution |

| Bandit | Hardcoded secret | Used an environment variable |

| Bandit | Bare exception handling | Caught the specific `KeyError` |

| Flake8 | Unused import | Removed unused import |

| Flake8 | Lines exceeding 79 characters | Reformatted long lines |

| Flake8 | Bare except statement | Replaced with specific exception |

| Flake8 | Comparison with `None` using `==` | Used `is None` |

| Flake8 | Unused local variables | Removed unused variables |

| Flake8 | Missing final newline | Added final newline |



\## 3. Before and After Results



\### Pylint

\- Before fixing: 4.81/10

\- After fixing: 10.00/10



\### Bandit

\- Before fixing: 6 security issues

\- After fixing: 0 security issues



\### Flake8

\- Before fixing: 9 reported violations

\- After fixing: 0 reported violations



\## 4. Conclusion



Static code analysis helped identify code quality problems, security vulnerabilities, and formatting violations in the Gym Membership System.



After correcting the identified issues, the program achieved a Pylint score of 10.00/10, Bandit reported no security issues, and Flake8 reported no formatting errors.



The exercise improved the code's readability, maintainability, and security.

