"""
AIRO Configuration Module
Zentrale Konfiguration für modernisierte AIRO-Architektur
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    """Konfiguration für verschiedene AI-Modelle mit modernen Optionen"""

    # Projekt-Planung: Größere Modelle für komplexe Reasoning
    PROJECT_PLANNER: str = os.getenv("PROJECT_PLANNER_MODEL", "llama3.1:70b")

    # Code-Generierung: Spezialisierte Code-Modelle
    CODER: str = os.getenv("CODER_MODEL", "deepseek-coder:33b")

    # Code-Review: Modell für Qualitätsprüfung
    CODE_REVIEWER: str = os.getenv("CODE_REVIEWER_MODEL", "codellama:34b")

    # Dokumentation: Modell für technische Dokumentation
    DOCUMENTATION: str = os.getenv("DOCUMENTATION_MODEL", "mistral:7b-instruct")

    # Architektur-Design: Für System-Design Entscheidungen
    ARCHITECT: str = os.getenv("ARCHITECT_MODEL", "llama3.1:70b")

    # Test-Generierung: Spezialisiert auf Test-Code
    TEST_GENERATOR: str = os.getenv("TEST_GENERATOR_MODEL", "deepseek-coder:33b")

    # Security-Analyse: Für Sicherheitsprüfungen
    SECURITY_ANALYZER: str = os.getenv("SECURITY_ANALYZER_MODEL", "llama3.1:70b")

    # Dateinamen-Generierung: Kleines, schnelles Modell
    TASKNAMER: str = os.getenv("TASKNAMER_MODEL", "llama3.1:8b")


@dataclass
class SystemConfig:
    """System-weite Konfigurationsparameter"""

    # Ollama API Einstellungen
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))

    # Temperatur-Einstellungen für verschiedene Tasks
    TEMP_PLANNING: float = float(os.getenv("TEMP_PLANNING", "0.7"))
    TEMP_CODING: float = float(os.getenv("TEMP_CODING", "0.2"))
    TEMP_REVIEW: float = float(os.getenv("TEMP_REVIEW", "0.3"))
    TEMP_CREATIVE: float = float(os.getenv("TEMP_CREATIVE", "0.8"))

    # Retry-Einstellungen
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "2"))

    # Code-Testing Einstellungen
    MAX_CORRECTION_ATTEMPTS: int = int(os.getenv("MAX_CORRECTION_ATTEMPTS", "3"))
    ENABLE_LINTING: bool = os.getenv("ENABLE_LINTING", "true").lower() == "true"
    ENABLE_TYPE_CHECKING: bool = os.getenv("ENABLE_TYPE_CHECKING", "true").lower() == "true"
    ENABLE_SECURITY_SCAN: bool = os.getenv("ENABLE_SECURITY_SCAN", "true").lower() == "true"

    # Feature Flags
    ENABLE_STREAMING: bool = os.getenv("ENABLE_STREAMING", "true").lower() == "true"
    ENABLE_RAG: bool = os.getenv("ENABLE_RAG", "false").lower() == "true"
    ENABLE_GIT_INTEGRATION: bool = os.getenv("ENABLE_GIT_INTEGRATION", "true").lower() == "true"
    USE_JSON_MODE: bool = os.getenv("USE_JSON_MODE", "true").lower() == "true"

    # Output-Einstellungen
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./generated_projects")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    VERBOSE: bool = os.getenv("VERBOSE", "false").lower() == "true"


@dataclass
class LanguageConfig:
    """Unterstützte Programmiersprachen und ihre Konfiguration"""

    SUPPORTED_LANGUAGES = {
        '.py': {
            'name': 'python',
            'test_framework': 'pytest',
            'linter': 'ruff',
            'type_checker': 'mypy',
            'formatter': 'black',
            'package_manager': 'pip',
            'package_file': 'requirements.txt'
        },
        '.js': {
            'name': 'javascript',
            'test_framework': 'jest',
            'linter': 'eslint',
            'formatter': 'prettier',
            'package_manager': 'npm',
            'package_file': 'package.json'
        },
        '.ts': {
            'name': 'typescript',
            'test_framework': 'jest',
            'linter': 'eslint',
            'type_checker': 'tsc',
            'formatter': 'prettier',
            'package_manager': 'npm',
            'package_file': 'package.json'
        },
        '.rs': {
            'name': 'rust',
            'test_framework': 'cargo test',
            'linter': 'clippy',
            'formatter': 'rustfmt',
            'package_manager': 'cargo',
            'package_file': 'Cargo.toml'
        },
        '.go': {
            'name': 'go',
            'test_framework': 'go test',
            'linter': 'golangci-lint',
            'formatter': 'gofmt',
            'package_manager': 'go',
            'package_file': 'go.mod'
        },
        '.java': {
            'name': 'java',
            'test_framework': 'junit',
            'linter': 'checkstyle',
            'formatter': 'google-java-format',
            'package_manager': 'maven',
            'package_file': 'pom.xml'
        },
        '.html': {
            'name': 'html',
            'linter': 'htmlhint',
            'formatter': 'prettier'
        },
        '.css': {
            'name': 'css',
            'linter': 'stylelint',
            'formatter': 'prettier'
        },
        '.cpp': {
            'name': 'cpp',
            'test_framework': 'googletest',
            'linter': 'clang-tidy',
            'formatter': 'clang-format',
            'package_manager': 'cmake'
        }
    }


# Globale Konfigurations-Instanzen
models = ModelConfig()
system = SystemConfig()
languages = LanguageConfig()
