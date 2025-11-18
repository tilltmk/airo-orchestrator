"""
Code-Analyse-Tools für AIRO
Linting, Type-Checking, Security-Scanning und Qualitätsprüfung
"""

import os
import subprocess
import ast
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from config import system, languages


@dataclass
class AnalysisResult:
    """Ergebnis einer Code-Analyse"""
    success: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    score: float  # 0.0 - 1.0


class CodeAnalyzer:
    """Erweiterte Code-Analyse mit modernen Tools"""

    def __init__(self):
        self.enable_linting = system.ENABLE_LINTING
        self.enable_type_checking = system.ENABLE_TYPE_CHECKING
        self.enable_security_scan = system.ENABLE_SECURITY_SCAN

    def analyze_code(
        self,
        code: str,
        language: str,
        file_path: Optional[str] = None
    ) -> AnalysisResult:
        """
        Umfassende Code-Analyse

        Args:
            code: Der zu analysierende Code
            language: Programmiersprache
            file_path: Optionaler Pfad zur Datei (für File-based Tools)

        Returns:
            AnalysisResult mit Fehler, Warnungen und Score
        """
        errors = []
        warnings = []
        info = []

        # Basis-Syntax-Prüfung
        syntax_ok, syntax_errors = self._check_syntax(code, language)
        if not syntax_ok:
            errors.extend(syntax_errors)
            return AnalysisResult(False, errors, warnings, info, 0.0)

        # Linting
        if self.enable_linting and file_path:
            lint_result = self._run_linting(file_path, language)
            errors.extend(lint_result.get('errors', []))
            warnings.extend(lint_result.get('warnings', []))

        # Type-Checking
        if self.enable_type_checking and file_path:
            type_result = self._run_type_checking(file_path, language)
            errors.extend(type_result.get('errors', []))
            warnings.extend(type_result.get('warnings', []))

        # Security-Scanning
        if self.enable_security_scan and file_path:
            security_result = self._run_security_scan(file_path, language)
            errors.extend(security_result.get('errors', []))
            warnings.extend(security_result.get('warnings', []))
            info.extend(security_result.get('info', []))

        # Code-Komplexität prüfen
        if language == 'python':
            complexity_warnings = self._check_complexity_python(code)
            warnings.extend(complexity_warnings)

        # Score berechnen
        score = self._calculate_score(errors, warnings)
        success = len(errors) == 0

        return AnalysisResult(success, errors, warnings, info, score)

    def _check_syntax(self, code: str, language: str) -> Tuple[bool, List[str]]:
        """Prüfe Basis-Syntax des Codes"""
        errors = []

        try:
            if language == 'python':
                ast.parse(code)
            elif language == 'javascript' or language == 'typescript':
                # Für JS/TS könnten wir acorn oder esprima verwenden
                # Hier vereinfachte Prüfung
                pass
            # Weitere Sprachen können hier hinzugefügt werden

            return True, []

        except SyntaxError as e:
            errors.append(f"Syntax-Fehler: {str(e)}")
            return False, errors
        except Exception as e:
            errors.append(f"Unerwarteter Fehler bei Syntax-Prüfung: {str(e)}")
            return False, errors

    def _run_linting(self, file_path: str, language: str) -> Dict[str, List[str]]:
        """Führe Linting mit sprachspezifischen Tools aus"""
        result = {'errors': [], 'warnings': []}

        # Hole Linter-Konfiguration
        ext = os.path.splitext(file_path)[1]
        lang_config = languages.SUPPORTED_LANGUAGES.get(ext, {})
        linter = lang_config.get('linter')

        if not linter:
            return result

        try:
            if language == 'python' and linter == 'ruff':
                # Ruff ist ein moderner, schneller Python-Linter
                output = subprocess.run(
                    ['ruff', 'check', file_path, '--output-format', 'json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                # Parse Ruff JSON output
                if output.stdout:
                    import json
                    issues = json.loads(output.stdout)
                    for issue in issues:
                        msg = f"{issue.get('code')}: {issue.get('message')} (line {issue.get('location', {}).get('row')})"
                        if issue.get('severity') == 'error':
                            result['errors'].append(msg)
                        else:
                            result['warnings'].append(msg)

            elif language in ['javascript', 'typescript'] and linter == 'eslint':
                output = subprocess.run(
                    ['eslint', file_path, '--format', 'json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                # Parse ESLint JSON output
                if output.stdout:
                    import json
                    results = json.loads(output.stdout)
                    for file_result in results:
                        for message in file_result.get('messages', []):
                            msg = f"{message.get('ruleId')}: {message.get('message')} (line {message.get('line')})"
                            if message.get('severity') == 2:
                                result['errors'].append(msg)
                            else:
                                result['warnings'].append(msg)

        except FileNotFoundError:
            result['warnings'].append(f"Linter '{linter}' nicht gefunden. Installieren Sie es für bessere Code-Qualität.")
        except subprocess.TimeoutExpired:
            result['warnings'].append(f"Linting Timeout für {file_path}")
        except Exception as e:
            result['warnings'].append(f"Linting-Fehler: {str(e)}")

        return result

    def _run_type_checking(self, file_path: str, language: str) -> Dict[str, List[str]]:
        """Führe Type-Checking aus"""
        result = {'errors': [], 'warnings': []}

        ext = os.path.splitext(file_path)[1]
        lang_config = languages.SUPPORTED_LANGUAGES.get(ext, {})
        type_checker = lang_config.get('type_checker')

        if not type_checker:
            return result

        try:
            if language == 'python' and type_checker == 'mypy':
                output = subprocess.run(
                    ['mypy', file_path, '--show-error-codes', '--no-error-summary'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if output.stdout:
                    for line in output.stdout.strip().split('\n'):
                        if line and ':' in line:
                            if 'error:' in line:
                                result['errors'].append(line)
                            else:
                                result['warnings'].append(line)

            elif language == 'typescript' and type_checker == 'tsc':
                output = subprocess.run(
                    ['tsc', '--noEmit', file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if output.stdout:
                    result['errors'].extend(output.stdout.strip().split('\n'))

        except FileNotFoundError:
            result['warnings'].append(f"Type-Checker '{type_checker}' nicht gefunden.")
        except subprocess.TimeoutExpired:
            result['warnings'].append(f"Type-Checking Timeout für {file_path}")
        except Exception as e:
            result['warnings'].append(f"Type-Checking-Fehler: {str(e)}")

        return result

    def _run_security_scan(self, file_path: str, language: str) -> Dict[str, List[str]]:
        """Führe Security-Scanning aus"""
        result = {'errors': [], 'warnings': [], 'info': []}

        try:
            if language == 'python':
                # Bandit für Python Security-Scanning
                output = subprocess.run(
                    ['bandit', '-f', 'json', file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if output.stdout:
                    import json
                    scan_result = json.loads(output.stdout)
                    for issue in scan_result.get('results', []):
                        severity = issue.get('issue_severity', 'LOW')
                        msg = f"Security: {issue.get('issue_text')} (line {issue.get('line_number')})"

                        if severity == 'HIGH':
                            result['errors'].append(msg)
                        elif severity == 'MEDIUM':
                            result['warnings'].append(msg)
                        else:
                            result['info'].append(msg)

            elif language in ['javascript', 'typescript']:
                # npm audit könnte hier verwendet werden
                pass

        except FileNotFoundError:
            # Security-Scanner nicht installiert ist kein kritischer Fehler
            pass
        except subprocess.TimeoutExpired:
            result['warnings'].append(f"Security-Scan Timeout für {file_path}")
        except Exception as e:
            result['warnings'].append(f"Security-Scan-Fehler: {str(e)}")

        return result

    def _check_complexity_python(self, code: str) -> List[str]:
        """Prüfe Code-Komplexität für Python"""
        warnings = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                # Prüfe Funktionslänge
                if isinstance(node, ast.FunctionDef):
                    func_lines = len(node.body)
                    if func_lines > 50:
                        warnings.append(
                            f"Funktion '{node.name}' ist sehr lang ({func_lines} Zeilen). "
                            "Erwägen Sie, sie zu refaktorieren."
                        )

                    # Prüfe Anzahl der Parameter
                    num_params = len(node.args.args)
                    if num_params > 7:
                        warnings.append(
                            f"Funktion '{node.name}' hat viele Parameter ({num_params}). "
                            "Erwägen Sie, Objekte zu verwenden."
                        )

                # Prüfe Verschachtelungstiefe
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    depth = self._calculate_nesting_depth(node)
                    if depth > 4:
                        warnings.append(
                            f"Tiefe Verschachtelung erkannt (Tiefe: {depth}). "
                            "Dies kann die Lesbarkeit beeinträchtigen."
                        )

        except Exception as e:
            warnings.append(f"Komplexitätsanalyse fehlgeschlagen: {str(e)}")

        return warnings

    def _calculate_nesting_depth(self, node, current_depth=1) -> int:
        """Berechne maximale Verschachtelungstiefe"""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)

        return max_depth

    def _calculate_score(self, errors: List[str], warnings: List[str]) -> float:
        """Berechne Qualitäts-Score basierend auf Fehler und Warnungen"""
        if not errors and not warnings:
            return 1.0

        # Jeder Fehler zählt mehr als eine Warnung
        penalty = len(errors) * 0.2 + len(warnings) * 0.05
        score = max(0.0, 1.0 - penalty)

        return round(score, 2)


# Globale Analyzer-Instanz
code_analyzer = CodeAnalyzer()
