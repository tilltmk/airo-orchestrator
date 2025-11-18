"""
Code Reviewer Agent - Führt umfassende Code-Reviews durch
Implementiert Best Practices für Code-Qualität und Security
"""

from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent


class CodeReviewerAgent(BaseAgent):
    """
    Agent für Code-Review mit Fokus auf Qualität, Security und Best Practices
    """

    def __init__(self):
        system_prompt = """You are an experienced senior software engineer and code reviewer with expertise in:
- Code quality and maintainability
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- Best practices and design patterns
- Language-specific idioms and conventions
- Code smells and anti-patterns

When reviewing code, evaluate:
1. Correctness: Does it work as intended?
2. Security: Are there vulnerabilities?
3. Performance: Any obvious inefficiencies?
4. Maintainability: Is it readable and well-structured?
5. Best practices: Does it follow conventions?
6. Testing: Is it testable?

Provide constructive, specific feedback with examples."""

        super().__init__(
            agent_type='code_reviewer',
            name='Senior Code Reviewer',
            system_prompt=system_prompt
        )

    def review_code(
        self,
        code: str,
        language: str,
        context: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Führe umfassendes Code-Review durch

        Returns:
            Dict mit Review-Ergebnissen
        """
        context_text = f"\n\nContext:\n{context}" if context else ""

        task = f"""Review the following {language} code comprehensively.{context_text}

Code:
```{language}
{code}
```

Provide a structured review with:

1. **Overall Assessment** (1-5 stars)
   - Brief summary of code quality

2. **Strengths**
   - What is done well

3. **Issues** (categorized by severity)
   - CRITICAL: Security vulnerabilities, major bugs
   - HIGH: Significant problems affecting functionality/performance
   - MEDIUM: Code smells, maintainability issues
   - LOW: Minor style issues, suggestions

4. **Specific Recommendations**
   - Concrete suggestions with code examples where helpful

5. **Security Considerations**
   - Any security concerns or vulnerabilities

6. **Performance Considerations**
   - Potential performance issues or optimizations

Respond in JSON format matching this structure:
{{
  "overall_rating": 4,
  "summary": "string",
  "strengths": ["string"],
  "issues": [
    {{
      "severity": "HIGH",
      "category": "security",
      "description": "string",
      "location": "line X or function name",
      "suggestion": "string"
    }}
  ],
  "recommendations": ["string"],
  "security_score": 4,
  "performance_score": 4,
  "maintainability_score": 3
}}"""

        return self.execute_structured(task, {})

    def review_changes(
        self,
        old_code: str,
        new_code: str,
        language: str
    ) -> Optional[str]:
        """Review von Code-Änderungen (wie Git Diff)"""
        task = f"""Review the changes between old and new versions of this {language} code.

Old code:
```{language}
{old_code}
```

New code:
```{language}
{new_code}
```

Evaluate:
1. Are the changes appropriate?
2. Do they introduce any issues?
3. Is functionality preserved?
4. Are there any regressions?
5. Could the changes be improved?

Provide detailed feedback on the changes."""

        return self.execute(task)

    def check_security(
        self,
        code: str,
        language: str
    ) -> Optional[List[Dict[str, str]]]:
        """Fokussierte Security-Analyse"""
        task = f"""Perform a security-focused analysis of this {language} code.

Code:
```{language}
{code}
```

Check for common vulnerabilities:
1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Authentication/Authorization issues
4. Insecure data handling
5. Use of deprecated/insecure functions
6. Input validation issues
7. Error handling that leaks information
8. Hardcoded secrets or credentials

For each issue found, provide:
- Type of vulnerability
- Severity (Critical, High, Medium, Low)
- Location in code
- Description of the issue
- Recommended fix

Respond in JSON format with array of issues."""

        result = self.execute(task, json_mode=True)
        if result:
            import json
            try:
                return json.loads(result)
            except:
                pass
        return None

    def suggest_refactoring(
        self,
        code: str,
        language: str,
        focus_areas: Optional[List[str]] = None
    ) -> Optional[str]:
        """Schlage Refactorings vor"""
        focus_text = ""
        if focus_areas:
            focus_text = f"\n\nFocus particularly on:\n" + "\n".join(f"- {area}" for area in focus_areas)

        task = f"""Analyze this {language} code and suggest refactoring opportunities.{focus_text}

Code:
```{language}
{code}
```

Look for:
1. Code duplication
2. Long functions/methods
3. Complex conditionals
4. Poor naming
5. Violation of SOLID principles
6. Applicable design patterns
7. Opportunities for simplification

For each refactoring suggestion:
1. Explain the issue
2. Show the refactored code
3. Explain the benefits"""

        return self.execute(task)

    def compare_implementations(
        self,
        implementations: List[Dict[str, str]],
        language: str,
        criteria: Optional[List[str]] = None
    ) -> Optional[str]:
        """Vergleiche verschiedene Implementierungen"""
        impls_text = "\n\n".join([
            f"Implementation {i+1} ({impl.get('name', 'unnamed')}):\n```{language}\n{impl.get('code', '')}\n```"
            for i, impl in enumerate(implementations)
        ])

        criteria_text = ""
        if criteria:
            criteria_text = f"\n\nEvaluate based on:\n" + "\n".join(f"- {c}" for c in criteria)

        task = f"""Compare the following {language} implementations of the same functionality.

{impls_text}{criteria_text}

For each implementation, evaluate:
1. Correctness
2. Performance
3. Readability
4. Maintainability
5. Security

Provide:
1. Comparison table/summary
2. Pros and cons of each
3. Recommendation with justification
4. Best elements from each that could be combined"""

        return self.execute(task)

    def review_architecture_alignment(
        self,
        code: str,
        language: str,
        architecture_guidelines: str
    ) -> Optional[str]:
        """Prüfe Alignment mit Architektur-Vorgaben"""
        task = f"""Review if this {language} code aligns with the architectural guidelines.

Code:
```{language}
{code}
```

Architecture Guidelines:
{architecture_guidelines}

Evaluate:
1. Does it follow the specified architecture?
2. Are there any violations?
3. Are dependencies appropriate?
4. Is separation of concerns maintained?
5. Does it fit into the overall system design?

Provide specific feedback on alignment and any deviations."""

        return self.execute(task)
