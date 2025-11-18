"""
AIRO Orchestrator - Moderne Multi-Agent-Orchestrierung (2025)
Koordiniert spezialisierte Agenten für Software-Entwicklung

Basierend auf Best Practices:
- Einfache Agent-Architekturen (Analyst-Coder Pattern)
- Iterative Feedback-Loops
- Bottom-up Compositional Structure
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

from agents.architect_agent import ArchitectAgent
from agents.coder_agent import CoderAgent
from agents.test_generator_agent import TestGeneratorAgent
from agents.code_reviewer_agent import CodeReviewerAgent
from config import system


@dataclass
class ProjectContext:
    """Kontext eines Projekts"""
    name: str
    description: str
    architecture: Optional[Dict[str, Any]] = None
    components: List[Dict[str, Any]] = None
    output_dir: str = ""

    def __post_init__(self):
        if self.components is None:
            self.components = []
        if not self.output_dir:
            self.output_dir = os.path.join(system.OUTPUT_DIR, self.name)


class AIROOrchestrator:
    """
    Haupt-Orchestrator für AIRO
    Koordiniert alle Agenten und den Entwicklungsprozess
    """

    def __init__(self, project_name: str, verbose: bool = False):
        self.project_name = project_name
        self.verbose = verbose

        # Initialisiere Agenten
        self.architect = ArchitectAgent()
        self.coder = CoderAgent()
        self.test_generator = TestGeneratorAgent()
        self.reviewer = CodeReviewerAgent()

        self.context: Optional[ProjectContext] = None

        self._log("AIRO Orchestrator initialized", "info")

    def create_project(
        self,
        description: str,
        primary_language: str = "python",
        include_tests: bool = True,
        include_review: bool = True
    ) -> bool:
        """
        Erstelle ein komplettes Projekt von einer Beschreibung

        Args:
            description: Projekt-Beschreibung
            primary_language: Haupt-Programmiersprache
            include_tests: Generiere Tests
            include_review: Führe Code-Review durch

        Returns:
            True bei Erfolg
        """
        try:
            self._log("🚀 Starting project creation...", "info")

            # Phase 1: Architektur-Design
            self._log("📐 Phase 1: Designing architecture...", "info")
            architecture = self.architect.design_architecture(description)

            if not architecture:
                self._log("Failed to design architecture", "error")
                return False

            # Erstelle Projekt-Kontext
            self.context = ProjectContext(
                name=self.project_name,
                description=description,
                architecture=architecture
            )

            # Erstelle Output-Verzeichnis
            os.makedirs(self.context.output_dir, exist_ok=True)

            # Speichere Architektur
            self._save_architecture(architecture)

            self._log(f"Architecture: {architecture.get('architecture_type', 'N/A')}", "info")

            # Phase 2: Komponenten identifizieren und generieren
            self._log("🔨 Phase 2: Generating components...", "info")
            components = architecture.get('components', [])

            if not components:
                # Fallback: Erstelle Basis-Komponente
                components = [{
                    'name': 'main',
                    'purpose': description,
                    'requirements': [],
                    'dependencies': []
                }]

            # Bottom-up: Generiere Komponenten von unten nach oben
            generated_components = []
            for i, component in enumerate(components, 1):
                self._log(f"  Generating component {i}/{len(components)}: {component.get('name')}...", "info")

                code, filename, metadata = self.coder.generate_with_validation(
                    task=self._create_component_task(component),
                    language=primary_language,
                    architecture_guidance=json.dumps(architecture, indent=2)
                )

                if code and filename:
                    # Speichere Code
                    file_path = os.path.join(self.context.output_dir, filename)
                    with open(file_path, 'w') as f:
                        f.write(code)

                    component_info = {
                        'name': component.get('name'),
                        'file_path': file_path,
                        'filename': filename,
                        'code': code,
                        'metadata': metadata
                    }
                    generated_components.append(component_info)

                    self._log(f"    ✓ Generated {filename} (quality: {metadata.get('quality_score', 0):.2f})", "success")
                else:
                    self._log(f"    ✗ Failed to generate {component.get('name')}", "error")

            self.context.components = generated_components

            # Phase 3: Code Review
            if include_review:
                self._log("🔍 Phase 3: Reviewing code...", "info")
                self._review_components(generated_components, primary_language)

            # Phase 4: Test-Generierung
            if include_tests:
                self._log("🧪 Phase 4: Generating tests...", "info")
                self._generate_tests(generated_components, primary_language)

            # Phase 5: Projekt-Dokumentation
            self._log("📝 Phase 5: Creating documentation...", "info")
            self._create_project_documentation()

            # Phase 6: Dependencies
            self._log("📦 Phase 6: Setting up dependencies...", "info")
            self._setup_dependencies(primary_language)

            self._log(f"✨ Project created successfully in {self.context.output_dir}", "success")
            return True

        except Exception as e:
            self._log(f"Error during project creation: {str(e)}", "error")
            return False

    def _create_component_task(self, component: Dict[str, Any]) -> str:
        """Erstelle detaillierte Task-Beschreibung für Komponente"""
        task_parts = [
            f"Create a component named '{component.get('name')}' with the following specification:",
            f"\nPurpose: {component.get('purpose')}",
        ]

        if component.get('responsibility'):
            task_parts.append(f"\nResponsibility: {component.get('responsibility')}")

        if component.get('dependencies'):
            deps = ', '.join(component.get('dependencies', []))
            task_parts.append(f"\nDependencies: {deps}")

        task_parts.append("\nEnsure the code is:")
        task_parts.append("- Well-structured and maintainable")
        task_parts.append("- Properly documented")
        task_parts.append("- Follows best practices")
        task_parts.append("- Includes error handling")

        return "\n".join(task_parts)

    def _review_components(
        self,
        components: List[Dict[str, Any]],
        language: str
    ):
        """Führe Code-Review für alle Komponenten durch"""
        reviews = []

        for component in components:
            name = component.get('name')
            code = component.get('code')

            if not code:
                continue

            self._log(f"  Reviewing {name}...", "info")

            review = self.reviewer.review_code(code, language)

            if review:
                # Speichere Review
                review_file = os.path.join(
                    self.context.output_dir,
                    f"review_{component.get('filename', 'unknown')}.json"
                )

                with open(review_file, 'w') as f:
                    json.dump(review, f, indent=2)

                rating = review.get('overall_rating', 0)
                self._log(f"    Rating: {rating}/5", "info")

                # Zeige kritische Issues
                issues = review.get('issues', [])
                critical = [i for i in issues if i.get('severity') == 'CRITICAL']

                if critical:
                    self._log(f"    ⚠️  {len(critical)} critical issue(s) found", "warning")

                reviews.append(review)

        # Speichere Gesamt-Review
        summary_file = os.path.join(self.context.output_dir, "code_review_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(reviews, f, indent=2)

    def _generate_tests(
        self,
        components: List[Dict[str, Any]],
        language: str
    ):
        """Generiere Tests für alle Komponenten"""
        test_suite = self.test_generator.generate_test_suite(components, language)

        for test_file, test_code in test_suite.items():
            test_path = os.path.join(self.context.output_dir, test_file)

            # Erstelle test-Verzeichnis falls nötig
            os.makedirs(os.path.dirname(test_path), exist_ok=True)

            with open(test_path, 'w') as f:
                f.write(test_code)

            self._log(f"  ✓ Generated {test_file}", "success")

        self._log(f"  Generated {len(test_suite)} test file(s)", "info")

    def _create_project_documentation(self):
        """Erstelle Projekt-Dokumentation"""
        readme_content = [
            f"# {self.context.name}\n",
            f"{self.context.description}\n",
            "## Architecture\n",
        ]

        if self.context.architecture:
            arch = self.context.architecture
            readme_content.append(f"Architecture Type: {arch.get('architecture_type', 'N/A')}\n")
            readme_content.append(f"\n{arch.get('description', '')}\n")

            # Tech Stack
            if arch.get('tech_stack'):
                readme_content.append("\n## Technology Stack\n")
                tech = arch.get('tech_stack', {})
                for category, items in tech.items():
                    if items:
                        readme_content.append(f"\n**{category.title()}**: {', '.join(items)}")

        # Komponenten
        readme_content.append("\n\n## Components\n")
        for comp in self.context.components:
            name = comp.get('name')
            filename = comp.get('filename')
            quality = comp.get('metadata', {}).get('quality_score', 0)
            readme_content.append(f"\n- **{name}** (`{filename}`) - Quality: {quality:.2f}")

        # Speichere README
        readme_path = os.path.join(self.context.output_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write("\n".join(readme_content))

    def _save_architecture(self, architecture: Dict[str, Any]):
        """Speichere Architektur-Design"""
        arch_file = os.path.join(self.context.output_dir, "architecture.json")
        with open(arch_file, 'w') as f:
            json.dump(architecture, f, indent=2)

    def _setup_dependencies(self, language: str):
        """Richte Dependency-Management ein"""
        if language == 'python':
            # Erstelle requirements.txt
            requirements = [
                "# Generated by AIRO",
                "# Add your project dependencies here",
            ]

            req_file = os.path.join(self.context.output_dir, "requirements.txt")
            with open(req_file, 'w') as f:
                f.write("\n".join(requirements))

        elif language in ['javascript', 'typescript']:
            # Erstelle package.json
            package = {
                "name": self.context.name,
                "version": "1.0.0",
                "description": self.context.description,
                "scripts": {
                    "test": "jest"
                },
                "devDependencies": {}
            }

            pkg_file = os.path.join(self.context.output_dir, "package.json")
            with open(pkg_file, 'w') as f:
                json.dump(package, f, indent=2)

    def _log(self, message: str, level: str = "info"):
        """Logging mit optionaler Verbosity"""
        if level == "error" or level == "warning" or self.verbose:
            prefix = {
                "info": "ℹ️ ",
                "success": "✓ ",
                "warning": "⚠️ ",
                "error": "✗ ",
            }.get(level, "")

            print(f"{prefix}{message}")

    def get_project_summary(self) -> Dict[str, Any]:
        """Hole Projekt-Zusammenfassung"""
        if not self.context:
            return {}

        return {
            "name": self.context.name,
            "description": self.context.description,
            "output_dir": self.context.output_dir,
            "architecture_type": self.context.architecture.get('architecture_type') if self.context.architecture else None,
            "num_components": len(self.context.components),
            "components": [
                {
                    "name": c.get('name'),
                    "file": c.get('filename'),
                    "quality": c.get('metadata', {}).get('quality_score')
                }
                for c in self.context.components
            ]
        }
