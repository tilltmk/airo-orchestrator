# AIRO v2.0 - Automated Idea Realization with Ollama

> **Modernisierte Multi-Agent-Architektur für KI-gestützte Software-Entwicklung (2025)**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Required-green.svg)](https://ollama.ai)

AIRO ist ein fortschrittliches Tool zur automatisierten Software-Entwicklung, das moderne Multi-Agent-Architekturen und Large Language Models (LLMs) nutzt, um aus natürlichsprachlichen Beschreibungen vollständige, produktionsreife Software-Projekte zu erstellen.

## 🌟 Highlights v2.0

- **🤖 Multi-Agent-Architektur**: Spezialisierte KI-Agenten für Architektur, Coding, Testing und Review
- **🔄 Iterative Feedback-Loops**: Automatische Code-Verbesserung durch Analyse und Korrektur
- **🏗️ Bottom-up Compositional Structure**: Komponenten werden von unten nach oben aufgebaut
- **🛡️ Security & Quality**: Integriertes Linting, Type-Checking und Security-Scanning
- **🧪 Automatische Tests**: KI-generierte Unit- und Integrationstests
- **📊 Code-Review**: Automatische Qualitätsprüfung durch Reviewer-Agent
- **🎨 Moderne CLI**: Rich-basierte Benutzeroberfläche mit interaktivem Modus
- **🔧 Hochgradig konfigurierbar**: Umfassende .env-basierte Konfiguration

## 🏛️ Architektur

AIRO v2 basiert auf **Best Practices für 2025**:

### Spezialisierte Agenten

```
┌─────────────────────────────────────────────────────────┐
│                  AIRO Orchestrator                      │
│          (Koordiniert alle Agenten)                     │
└──────────┬─────────┬──────────┬──────────┬──────────────┘
           │         │          │          │
    ┌──────▼──┐ ┌───▼────┐ ┌──▼─────┐ ┌──▼─────────┐
    │Architect│ │ Coder  │ │ Tester │ │  Reviewer  │
    │  Agent  │ │ Agent  │ │ Agent  │ │   Agent    │
    └─────────┘ └────────┘ └────────┘ └────────────┘
```

1. **Architect Agent**: System-Design und Architektur-Entscheidungen
2. **Coder Agent**: Code-Generierung mit Validierung
3. **Test Generator Agent**: Umfassende Test-Suite-Erstellung
4. **Code Reviewer Agent**: Qualitäts- und Security-Prüfung

### Workflow

```
1. Projekt-Beschreibung
        ↓
2. Architektur-Design (Architect Agent)
        ↓
3. Komponenten-Generierung (Coder Agent)
        ↓  ← Iterative Feedback-Loops
4. Code-Analyse & Validierung
        ↓
5. Code-Review (Reviewer Agent)
        ↓
6. Test-Generierung (Test Generator)
        ↓
7. Dokumentation & Setup
        ↓
8. ✨ Fertiges Projekt
```

## 🚀 Installation

### Voraussetzungen

1. **Python 3.8+**
2. **Ollama** installiert und laufend
   ```bash
   # Ollama installieren (siehe https://ollama.ai)
   curl -fsSL https://ollama.ai/install.sh | sh

   # Empfohlene Modelle herunterladen
   ollama pull llama3.1:70b        # Für Planung & Architektur
   ollama pull deepseek-coder:33b  # Für Code-Generierung
   ollama pull codellama:34b       # Für Code-Review
   ```

### Setup

```bash
# Repository klonen
git clone https://github.com/yourusername/airo-orchestrator.git
cd airo-orchestrator

# Dependencies installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeiten Sie .env nach Ihren Bedürfnissen
```

### Konfiguration

Bearbeiten Sie `.env` um die Modelle und Einstellungen anzupassen:

```bash
# Modelle (empfohlene Defaults für 2025)
PROJECT_PLANNER_MODEL=llama3.1:70b
CODER_MODEL=deepseek-coder:33b
CODE_REVIEWER_MODEL=codellama:34b
TEST_GENERATOR_MODEL=deepseek-coder:33b

# Features aktivieren/deaktivieren
ENABLE_LINTING=true
ENABLE_TYPE_CHECKING=true
ENABLE_SECURITY_SCAN=true
ENABLE_STREAMING=true

# Siehe .env.example für alle Optionen
```

## 💻 Verwendung

### Interaktiver Modus (Empfohlen)

```bash
python airo_v2.py
```

Der interaktive Modus führt Sie Schritt für Schritt durch:
1. Projekt-Name eingeben
2. Projekt beschreiben
3. Programmiersprache wählen
4. Optionen konfigurieren
5. Projekt wird automatisch erstellt

### Direkter CLI-Modus

```bash
# Einfaches Beispiel
python airo_v2.py -p "todo_app" -d "Eine Todo-Verwaltungs-App mit REST API"

# Mit Optionen
python airo_v2.py \
  -p "blog_system" \
  -d "Ein Blog-System mit Authentifizierung und Markdown-Support" \
  -l python \
  --no-tests \
  -v

# Hilfe anzeigen
python airo_v2.py --help
```

### Parameter

- `-i, --interactive`: Interaktiver Modus
- `-p, --project`: Projekt-Name
- `-d, --description`: Projekt-Beschreibung
- `-l, --language`: Programmiersprache (python, javascript, typescript, rust, go, java)
- `--no-tests`: Tests nicht generieren
- `--no-review`: Kein Code-Review
- `-v, --verbose`: Ausführliche Ausgabe

## 📦 Unterstützte Programmiersprachen

| Sprache    | Code-Gen | Tests | Linting | Type-Check | Formatter |
|------------|----------|-------|---------|------------|-----------|
| Python     | ✅       | ✅    | ✅ ruff | ✅ mypy    | ✅ black  |
| JavaScript | ✅       | ✅    | ✅ eslint| ❌        | ✅ prettier|
| TypeScript | ✅       | ✅    | ✅ eslint| ✅ tsc    | ✅ prettier|
| Rust       | ✅       | ✅    | ✅ clippy| ✅ (built-in)| ✅ rustfmt|
| Go         | ✅       | ✅    | ✅ golangci-lint| ✅ (built-in)| ✅ gofmt|
| Java       | ✅       | ✅    | ✅ checkstyle| ❌    | ✅ google-java-format|

## 🎯 Features im Detail

### Architektur-Design

Der **Architect Agent** analysiert Ihre Projekt-Beschreibung und erstellt:
- Passende Architektur-Empfehlung (Monolith, Microservices, etc.)
- Komponenten-Design mit Verantwortlichkeiten
- Technology Stack-Empfehlungen
- Projekt-Struktur
- Design Patterns

### Code-Generierung

Der **Coder Agent** generiert qualitativ hochwertigen Code:
- Mehrere Iterationen mit automatischer Verbesserung
- Syntax-Validierung
- Linting (Ruff, ESLint, etc.)
- Type-Checking (MyPy, TypeScript)
- Security-Scanning (Bandit)
- Best Practices für jede Sprache

### Code-Review

Der **Reviewer Agent** führt umfassende Reviews durch:
- Qualitäts-Bewertung (1-5 Sterne)
- Security-Analyse (OWASP Top 10)
- Performance-Überlegungen
- Maintainability-Check
- Konkrete Verbesserungsvorschläge

### Test-Generierung

Der **Test Generator Agent** erstellt:
- Unit-Tests für alle Komponenten
- Integration-Tests
- Edge-Cases und Error-Conditions
- Hohe Test-Coverage (Ziel: >80%)
- Framework-spezifische Best Practices

## 📁 Generierte Projekt-Struktur

```
generated_projects/
└── mein_projekt/
    ├── README.md                    # Projekt-Dokumentation
    ├── architecture.json            # Architektur-Details
    ├── requirements.txt             # Python Dependencies (oder package.json)
    ├── main.py                      # Haupt-Komponente
    ├── component_x.py               # Weitere Komponenten
    ├── test_main.py                 # Tests
    ├── code_review_summary.json     # Review-Ergebnisse
    └── review_main.py.json          # Detaillierte Reviews
```

## 🔧 Erweiterte Verwendung

### Programmatische Nutzung

```python
from orchestrator import AIROOrchestrator

# Orchestrator erstellen
orchestrator = AIROOrchestrator("mein_projekt", verbose=True)

# Projekt erstellen
success = orchestrator.create_project(
    description="Eine REST API für Benutzerverwaltung",
    primary_language="python",
    include_tests=True,
    include_review=True
)

# Projekt-Zusammenfassung
if success:
    summary = orchestrator.get_project_summary()
    print(f"Projekt erstellt: {summary['output_dir']}")
```

### Einzelne Agenten verwenden

```python
from agents.coder_agent import CoderAgent
from agents.architect_agent import ArchitectAgent

# Architektur designen
architect = ArchitectAgent()
architecture = architect.design_architecture(
    "Eine E-Commerce-Plattform"
)

# Code generieren
coder = CoderAgent()
code, filename, metadata = coder.generate_with_validation(
    task="Erstelle eine User-Klasse mit Authentication",
    language="python"
)
```

## 🎓 Best Practices (2025)

AIRO v2 implementiert moderne Best Practices:

1. **Einfache Multi-Agent-Architekturen** sind effektiver als komplexe
2. **Iterative Feedback-Loops** für Code-Qualität
3. **Bottom-up Compositional Structure** für stabile Komponenten
4. **Spezialisierte Agent-Rollen** statt generischer Agents
5. **Debugging-Mechanismen** kombiniert mit Multi-Agent-Ansatz

Quellen: ACM TOSEM 2025, arXiv Papers zu LLM-based Multi-Agent Systems

## 📊 Empfohlene Ollama-Modelle

### Code-Generierung
- **DeepSeek Coder 33B**: Hervorragend für Code (87 Sprachen, 2T tokens)
- **DeepSeek-R1**: Mit Reasoning-Capabilities für komplexe Aufgaben
- **CodeLlama 34B**: Starke Alternative, besonders für Python

### Planung & Architektur
- **Llama 3.1 70B**: Ausgezeichnetes Reasoning, gute Balance
- **Llama 3.1 405B**: Best-in-class (wenn Hardware ausreicht)

### Schnelle Tasks
- **Llama 3.1 8B**: Für einfache Aufgaben (Dateinamen, etc.)
- **Mistral 7B**: Gute Alternative

## 🆚 v1 vs v2

| Feature | v1 (Original) | v2 (Modernisiert) |
|---------|---------------|-------------------|
| Architektur | Single-Agent | Multi-Agent |
| Code-Qualität | Basis | Linting, Type-Check, Security |
| Feedback-Loops | ❌ | ✅ Iterativ |
| Tests | Manuell | Automatisch generiert |
| Code-Review | ❌ | ✅ Automatisch |
| CLI | Basis | Rich UI, Interaktiv |
| Konfiguration | Hardcoded | .env-basiert |
| Sprachen | 3 | 6+ |
| Modelle | Alte | 2025 State-of-the-Art |

## 🤝 Contributing

Contributions sind willkommen! Bitte erstellen Sie ein Issue oder Pull Request.

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagungen

- [Ollama](https://ollama.ai) für die lokale LLM-Infrastruktur
- Open-Source LLM-Community (Meta, DeepSeek, Mistral)
- Moderne Multi-Agent-System-Forschung

## 📚 Weiterführende Ressourcen

- [Ollama Dokumentation](https://github.com/ollama/ollama)
- [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder)
- [Multi-Agent Systems for Software Engineering (ACM)](https://dl.acm.org/doi/10.1145/3712003)
- [Agentic AI Best Practices 2025](https://arxiv.org/abs/2508.11126)

---

**AIRO v2.0** - Von Ideen zu Software in Minuten statt Tagen 🚀
