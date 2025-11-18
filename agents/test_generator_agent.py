"""
Test Generator Agent - Generiert umfassende Unit-Tests
Basierend auf 2025 Best Practices für Test-Driven Development
"""

from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from config import languages
import os


class TestGeneratorAgent(BaseAgent):
    """Agent für Test-Generierung mit modernen Testing-Praktiken"""

    def __init__(self):
        system_prompt = """You are an expert test engineer specializing in:
- Test-Driven Development (TDD)
- Behavior-Driven Development (BDD)
- Unit testing, integration testing, and E2E testing
- Test coverage and quality
- Modern testing frameworks (pytest, jest, JUnit, etc.)
- Edge cases and error conditions
- Mocking and test isolation

When generating tests:
1. Cover all main functionality paths
2. Include edge cases and error conditions
3. Test both positive and negative scenarios
4. Use descriptive test names
5. Follow AAA pattern (Arrange, Act, Assert)
6. Ensure tests are isolated and repeatable
7. Add comments explaining complex test scenarios"""

        super().__init__(
            agent_type='test_generator',
            name='Test Engineer',
            system_prompt=system_prompt
        )

    def generate_tests(
        self,
        code: str,
        language: str,
        test_type: str = 'unit'
    ) -> Optional[str]:
        """
        Generiere Tests für gegebenen Code

        Args:
            code: Der zu testende Code
            language: Programmiersprache
            test_type: Art des Tests (unit, integration, e2e)

        Returns:
            Test-Code
        """
        ext = self._get_extension_for_language(language)
        lang_config = languages.SUPPORTED_LANGUAGES.get(ext, {})
        framework = lang_config.get('test_framework', 'standard')

        task = f"""Generate comprehensive {test_type} tests for the following {language} code using {framework}.

Code to test:
```{language}
{code}
```

Requirements:
1. Test all public functions/methods
2. Cover edge cases and error conditions
3. Include both positive and negative test cases
4. Use appropriate mocking where needed
5. Follow {framework} best practices
6. Aim for high code coverage (>80%)
7. Use descriptive test names that explain what is being tested

Provide complete, runnable test code."""

        return self.execute(task)

    def generate_test_suite(
        self,
        components: List[Dict[str, Any]],
        language: str
    ) -> Dict[str, str]:
        """
        Generiere eine komplette Test-Suite für mehrere Komponenten

        Args:
            components: Liste von Komponenten mit {name, code, file_path}
            language: Programmiersprache

        Returns:
            Dict mit {test_file: test_code}
        """
        test_suite = {}

        for component in components:
            name = component.get('name', 'unknown')
            code = component.get('code', '')
            file_path = component.get('file_path', '')

            if not code:
                continue

            # Generiere Tests
            tests = self.generate_tests(code, language)

            if tests:
                test_filename = self._get_test_filename(file_path, language)
                test_suite[test_filename] = tests

        return test_suite

    def generate_integration_tests(
        self,
        components: List[Dict[str, Any]],
        language: str,
        integration_points: List[str]
    ) -> Optional[str]:
        """Generiere Integrationstests für Komponenten-Interaktionen"""
        components_info = "\n\n".join([
            f"Component: {c.get('name')}\n```{language}\n{c.get('code', '')}\n```"
            for c in components
        ])

        integration_info = "\n".join(f"- {point}" for point in integration_points)

        task = f"""Generate integration tests for the following {language} components and their interactions.

Components:
{components_info}

Integration points to test:
{integration_info}

Create tests that:
1. Verify components work together correctly
2. Test data flow between components
3. Validate error propagation
4. Check system behavior under various conditions

Provide complete integration test code."""

        return self.execute(task)

    def suggest_test_improvements(
        self,
        test_code: str,
        code: str,
        language: str
    ) -> Optional[str]:
        """Analysiere Tests und schlage Verbesserungen vor"""
        task = f"""Analyze the following {language} tests and suggest improvements.

Code under test:
```{language}
{code}
```

Current tests:
```{language}
{test_code}
```

Analyze:
1. Test coverage - what's missing?
2. Edge cases not covered
3. Test quality and maintainability
4. Potential flaky tests
5. Performance of tests

Provide:
1. Analysis of current test quality
2. List of missing test cases
3. Specific suggestions for improvement
4. Updated test code if significant improvements needed"""

        return self.execute(task)

    def generate_test_data(
        self,
        schema: Dict[str, Any],
        num_samples: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Generiere Test-Daten basierend auf Schema"""
        schema_json = str(schema)

        task = f"""Generate {num_samples} realistic test data samples matching this schema:

{schema_json}

Include:
1. Normal/valid cases
2. Edge cases (empty, null, min/max values)
3. Invalid cases for negative testing
4. Diverse data for thorough testing

Return as a JSON array of test cases with labels."""

        result = self.execute(task, json_mode=True)
        if result:
            import json
            try:
                return json.loads(result)
            except:
                pass
        return None

    def _get_extension_for_language(self, language: str) -> str:
        """Bestimme Dateiendung für Sprache"""
        lang_to_ext = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'rust': '.rs',
            'go': '.go',
            'java': '.java',
            'cpp': '.cpp',
        }
        return lang_to_ext.get(language.lower(), '.txt')

    def _get_test_filename(self, source_file: str, language: str) -> str:
        """Generiere Test-Dateinamen basierend auf Source-Datei"""
        if not source_file:
            return f"test_generated{self._get_extension_for_language(language)}"

        base, ext = os.path.splitext(source_file)

        # Sprachspezifische Namenskonventionen
        if language == 'python':
            # Python: test_<name>.py
            return f"test_{os.path.basename(base)}{ext}"
        elif language in ['javascript', 'typescript']:
            # JS/TS: <name>.test.js
            return f"{os.path.basename(base)}.test{ext}"
        elif language == 'rust':
            # Rust: Tests sind meist inline oder in tests/
            return f"tests/{os.path.basename(base)}_test.rs"
        elif language == 'go':
            # Go: <name>_test.go
            return f"{os.path.basename(base)}_test.go"
        elif language == 'java':
            # Java: <Name>Test.java
            name = os.path.basename(base)
            return f"{name}Test.java"
        else:
            return f"test_{os.path.basename(base)}{ext}"
