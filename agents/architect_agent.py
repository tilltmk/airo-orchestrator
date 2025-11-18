"""
Architect Agent - Verantwortlich für System-Design und Architektur-Entscheidungen
"""

from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent


class ArchitectAgent(BaseAgent):
    """Agent für Software-Architektur und System-Design"""

    def __init__(self):
        system_prompt = """You are an expert software architect with deep knowledge of:
- Software design patterns and architectural patterns
- System design and scalability
- Best practices for different technology stacks
- Clean code principles and SOLID principles
- Modern software architecture (microservices, event-driven, etc.)

Your role is to design robust, maintainable, and scalable software architectures.
Always consider:
1. Separation of concerns
2. Maintainability and testability
3. Performance and scalability
4. Security best practices
5. Technology stack appropriateness"""

        super().__init__(
            agent_type='architect',
            name='Software Architect',
            system_prompt=system_prompt
        )

    def design_architecture(self, project_description: str) -> Optional[Dict[str, Any]]:
        """
        Entwerfe eine Software-Architektur für ein Projekt

        Returns:
            Dict mit:
            - architecture_type: z.B. "monolithic", "microservices", "serverless"
            - components: Liste von Komponenten
            - tech_stack: Empfohlene Technologien
            - folder_structure: Projekt-Struktur
            - design_patterns: Zu verwendende Patterns
        """
        schema = {
            "architecture_type": "string",
            "description": "string",
            "components": [
                {
                    "name": "string",
                    "responsibility": "string",
                    "dependencies": ["string"]
                }
            ],
            "tech_stack": {
                "backend": ["string"],
                "frontend": ["string"],
                "database": ["string"],
                "tools": ["string"]
            },
            "folder_structure": {
                "root": ["string"]
            },
            "design_patterns": ["string"],
            "considerations": ["string"]
        }

        task = f"""Design a complete software architecture for the following project:

{project_description}

Consider:
1. What type of architecture is most appropriate?
2. What are the main components and their responsibilities?
3. What technology stack would you recommend?
4. How should the project be structured (folders/files)?
5. Which design patterns should be used?
6. What are important architectural considerations?"""

        return self.execute_structured(task, schema)

    def review_architecture(
        self,
        current_architecture: str,
        concerns: Optional[List[str]] = None
    ) -> str:
        """Überprüfe und verbessere eine existierende Architektur"""
        concerns_text = ""
        if concerns:
            concerns_text = f"\n\nSpecific concerns to address:\n" + "\n".join(f"- {c}" for c in concerns)

        task = f"""Review the following software architecture and suggest improvements:

{current_architecture}{concerns_text}

Provide:
1. Strengths of the current architecture
2. Potential issues or weaknesses
3. Specific recommendations for improvement
4. Alternative approaches to consider"""

        return self.execute(task)

    def choose_tech_stack(
        self,
        project_type: str,
        requirements: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Wähle einen geeigneten Technology Stack"""
        schema = {
            "recommendations": {
                "backend": {
                    "language": "string",
                    "framework": "string",
                    "reasoning": "string"
                },
                "frontend": {
                    "framework": "string",
                    "reasoning": "string"
                },
                "database": {
                    "type": "string",
                    "system": "string",
                    "reasoning": "string"
                },
                "additional_tools": [
                    {
                        "tool": "string",
                        "purpose": "string"
                    }
                ]
            },
            "alternatives": ["string"]
        }

        requirements_text = "\n".join(f"- {r}" for r in requirements)

        task = f"""Recommend a technology stack for a {project_type} project with these requirements:

{requirements_text}

Consider:
1. Development speed and ease of use
2. Performance and scalability
3. Community support and ecosystem
4. Long-term maintainability
5. Team expertise (assume intermediate level)

Provide specific recommendations with reasoning."""

        return self.execute_structured(task, schema)
