\# Reflection – Static Code Analysis Lab



\## 1. What did I learn from this lab?



I learned how to use Pylint, Bandit, and Flake8 to analyze Python code. I understood how static code analysis helps identify programming mistakes, security vulnerabilities, and coding style violations.



\## 2. What problems did I identify?



Initially, the program had several issues, including improper function naming, missing docstrings, unsafe use of eval(), weak MD5 hashing, insecure random number generation, and formatting violations.



\## 3. How did I fix the problems?



I corrected the function names, added docstrings, removed unused variables, replaced eval() with arithmetic operations, used SHA-256 hashing, replaced random with secrets, removed os.system(), and corrected formatting issues.



\## 4. What did I learn about security?



I learned that unsafe functions and weak cryptographic methods can create security vulnerabilities. Using safer alternatives helps improve application security.



\## 5. What is the final outcome?



After fixing the issues, Pylint gave a score of 10.00/10, Bandit reported zero security issues, and Flake8 reported zero errors.



\## 6. Conclusion



This lab helped me understand the importance of static code analysis in software development. I learned how to improve code quality, readability, maintainability, and security using automated analysis tools.

