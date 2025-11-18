"""
Coder Agent - Spezialisiert auf Code-Generierung mit modernen Best Practices (2025)
Implementiert iterative Feedback-Loops und bottom-up compositional structure
"""

from typing import Dict, Any, List, Optional, Tuple
from agents.base_agent import BaseAgent
from utils.code_analyzer import code_analyzer
from config import system, languages
import re


class CoderAgent(BaseAgent):
    """
    Moderner Code-Generator basierend auf 2025 Best Practices:
    - Iterative Feedback-Loops
    - Bottom-up compositional structure
    - Specialized role in multi-agent system
    """

    def __init__(self):
        system_prompt = """You are an expert software engineer with deep knowledge of:
- Clean code principles and best practices
- Modern programming languages and frameworks
- Design patterns and SOLID principles
- Test-driven development
- Security-conscious coding
- Performance optimization

When generating code:
1. Write clean, readable, and well-documented code
2. Follow language-specific conventions and best practices
3. Include error handling and edge cases
4. Add type hints/annotations where applicable
5. Consider security implications
6. Write efficient, maintainable code

Always wrap code in triple backticks with the language specified:
```python
# your code here
```"""

        super().__init__(
            agent_type='coder',
            name='Software Engineer',
            system_prompt=system_prompt
        )
        self.max_iterations = system.MAX_CORRECTION_ATTEMPTS

    def generate_code(
        self,
        task: str,
        language: str,
        context: Optional[str] = None,
        architecture_guidance: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Generiere Code mit iterativem Feedback

        Args:
            task: Die Code-Aufgabe
            language: Ziel-Programmiersprache
            context: Optionaler Kontext (z.B. bestehender Code)
            architecture_guidance: Architektur-Vorgaben

        Returns:
            (code, filename, metadata)
        """
        # Erweitere den Task mit Kontext
        enhanced_task = self._build_enhanced_prompt(
            task, language, context, architecture_guidance
        )

        # Initiale Code-Generierung
        code = self.execute(enhanced_task)

        if not code:
            return None, None, {"error": "Code generation failed"}

        # Extrahiere Code und Sprache aus Markdown
        extracted_code, detected_lang = self._extract_code_from_markdown(code)

        if not extracted_code:
            extracted_code = code  # Fallback wenn kein Markdown

        # Bestimme Dateinamen
        filename = self._generate_filename(task, detected_lang or language)

        # Metadata sammeln
        metadata = {
            "task": task,
            "language": detected_lang or language,
            "filename": filename,
            "iterations": 0,
            "quality_score": 0.0
        }

        return extracted_code, filename, metadata

    def generate_with_validation(
        self,
        task: str,
        language: str,
        context: Optional[str] = None,
        architecture_guidance: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Generiere Code mit automatischer Validierung und Korrektur

        Implementiert Best Practice: Iterative Feedback-Loops
        """
        code, filename, metadata = self.generate_code(
            task, language, context, architecture_guidance
        )

        if not code:
            return None, None, metadata

        # Iterative Verbesserung durch Feedback
        for iteration in range(self.max_iterations):
            # Schreibe temporäre Datei für Analyse
            temp_file = file_path or f"temp_{filename}"
            with open(temp_file, 'w') as f:
                f.write(code)

            # Analysiere Code
            analysis = code_analyzer.analyze_code(code, language, temp_file)

            metadata["quality_score"] = analysis.score
            metadata["iterations"] = iteration + 1

            # Wenn Code gut genug ist, beende
            if analysis.success and analysis.score >= 0.8:
                metadata["validation"] = "passed"
                metadata["errors"] = []
                metadata["warnings"] = analysis.warnings
                break

            # Wenn letzte Iteration, gib aktuellen Code zurück
            if iteration == self.max_iterations - 1:
                metadata["validation"] = "failed"
                metadata["errors"] = analysis.errors
                metadata["warnings"] = analysis.warnings
                break

            # Sonst versuche Code zu korrigieren
            code = self._correct_code(code, analysis, task, language)

            if not code:
                break

        return code, filename, metadata

    def generate_component(
        self,
        component_spec: Dict[str, Any],
        language: str
    ) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Generiere eine einzelne Komponente (bottom-up approach)

        Best Practice: Break down complex tasks into well-defined sub-problems
        """
        task = f"""Generate a {component_spec.get('type', 'component')} with the following specification:

Name: {component_spec.get('name')}
Purpose: {component_spec.get('purpose')}
Inputs: {component_spec.get('inputs', 'none')}
Outputs: {component_spec.get('outputs', 'none')}

Requirements:
{self._format_requirements(component_spec.get('requirements', []))}

Dependencies:
{self._format_list(component_spec.get('dependencies', []))}"""

        return self.generate_with_validation(
            task=task,
            language=language,
            context=component_spec.get('context')
        )

    def refactor_code(
        self,
        code: str,
        language: str,
        refactoring_goals: List[str]
    ) -> Optional[str]:
        """Refaktoriere existierenden Code"""
        goals_text = "\n".join(f"- {goal}" for goal in refactoring_goals)

        task = f"""Refactor the following {language} code to achieve these goals:

{goals_text}

Original code:
```{language}
{code}
```

Provide the refactored code with the same functionality but improved according to the goals."""

        return self.execute(task)

    def add_documentation(
        self,
        code: str,
        language: str,
        doc_style: str = "google"
    ) -> Optional[str]:
        """Füge Dokumentation zu Code hinzu"""
        task = f"""Add comprehensive documentation to this {language} code using {doc_style} style.

Include:
1. Module/file-level docstring
2. Function/method docstrings with parameters and return values
3. Inline comments for complex logic
4. Type hints/annotations where appropriate

Code:
```{language}
{code}
```

Return the fully documented code."""

        return self.execute(task)

    def _build_enhanced_prompt(
        self,
        task: str,
        language: str,
        context: Optional[str],
        architecture_guidance: Optional[str]
    ) -> str:
        """Baue einen erweiterten Prompt mit Kontext"""
        prompt_parts = [f"Generate {language} code for the following task:\n\n{task}"]

        if context:
            prompt_parts.append(f"\n\nContext:\n{context}")

        if architecture_guidance:
            prompt_parts.append(f"\n\nArchitecture Guidance:\n{architecture_guidance}")

        # Füge sprachspezifische Best Practices hinzu
        ext = self._get_extension_for_language(language)
        lang_config = languages.SUPPORTED_LANGUAGES.get(ext, {})

        if lang_config:
            prompt_parts.append(f"\n\nEnsure the code:")
            if 'formatter' in lang_config:
                prompt_parts.append(f"- Follows {lang_config['formatter']} formatting standards")
            if 'test_framework' in lang_config:
                prompt_parts.append(f"- Is testable with {lang_config['test_framework']}")

        return "\n".join(prompt_parts)

    def _extract_code_from_markdown(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extrahiere Code aus Markdown-Code-Blocks"""
        # Suche nach Code-Blocks mit Sprache
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            language, code = matches[0]
            return code.strip(), language.lower()

        # Suche nach Code-Blocks ohne Sprache
        pattern = r'```\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return matches[0].strip(), None

        return None, None

    def _generate_filename(self, task: str, language: str) -> str:
        """Generiere einen Dateinamen basierend auf Aufgabe und Sprache"""
        # Vereinfachte Version - nutze LLM für bessere Namen
        ext = self._get_extension_for_language(language)

        # Extrahiere Schlüsselwörter aus Task
        words = re.findall(r'\b[a-z_]+\b', task.lower())
        if words:
            name = '_'.join(words[:3])  # Erste 3 Wörter
            return f"{name}{ext}"

        return f"generated_code{ext}"

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
            'c++': '.cpp',
            'html': '.html',
            'css': '.css'
        }
        return lang_to_ext.get(language.lower(), '.txt')

    def _format_requirements(self, requirements: List[str]) -> str:
        """Formatiere Anforderungen"""
        if not requirements:
            return "None specified"
        return "\n".join(f"- {req}" for req in requirements)

    def _format_list(self, items: List[str]) -> str:
        """Formatiere Liste von Items"""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)

    def _correct_code(
        self,
        code: str,
        analysis: Any,
        original_task: str,
        language: str
    ) -> Optional[str]:
        """
        Korrigiere Code basierend auf Analyse-Feedback

        Best Practice: Iterative Feedback-Loops
        """
        errors_text = "\n".join(f"- {err}" for err in analysis.errors)
        warnings_text = "\n".join(f"- {warn}" for warn in analysis.warnings[:5])  # Limitiere Warnungen

        correction_task = f"""The following {language} code has issues. Fix them while maintaining the original functionality.

Original Task: {original_task}

Current Code:
```{language}
{code}
```

Errors to fix:
{errors_text}

Warnings to address:
{warnings_text}

Provide the corrected code."""

        return self.execute(correction_task)
