"""
Agile Project Planner for Moirai

Responsible for analyzing user requirements and breaking them down
into actionable epics and tasks that can be distributed to agents
in the Agora marketplace.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from ..mcp_integration.agora_client import AgoraClient


class AgileProjectPlanner:
    """
    Analyzes user requirements and creates structured project plans
    using agile methodology principles.
    """
    
    def __init__(self, agora_client: AgoraClient):
        """
        Initialize the project planner.
        
        Args:
            agora_client: Connected Agora client for coordination
        """
        self.agora = agora_client
        
        # Common project patterns and their typical requirements
        self.project_patterns = {
            'web_application': {
                'keywords': ['web app', 'website', 'frontend', 'backend', 'full stack'],
                'typical_agents': ['frontend', 'backend', 'database', 'ui_design'],
                'typical_duration': 'weeks'
            },
            'api_service': {
                'keywords': ['api', 'rest', 'graphql', 'service', 'endpoint'],
                'typical_agents': ['backend', 'database', 'documentation', 'testing'],
                'typical_duration': 'days'
            },
            'documentation': {
                'keywords': ['docs', 'documentation', 'guide', 'manual', 'readme'],
                'typical_agents': ['documentation', 'technical_writing'],
                'typical_duration': 'days'
            },
            'mobile_app': {
                'keywords': ['mobile', 'ios', 'android', 'react native', 'flutter'],
                'typical_agents': ['mobile', 'ui_design', 'backend', 'testing'],
                'typical_duration': 'weeks'
            },
            'data_analysis': {
                'keywords': ['data', 'analytics', 'dashboard', 'visualization', 'report'],
                'typical_agents': ['data_scientist', 'backend', 'frontend', 'database'],
                'typical_duration': 'days'
            }
        }
    
    async def create_project_plan(self, user_requirements: str) -> Dict[str, Any]:
        """
        Create a comprehensive project plan from user requirements.
        
        Args:
            user_requirements: Natural language description of what the user wants
            
        Returns:
            Dictionary containing the structured project plan
        """
        try:
            # Step 1: Analyze the requirements
            analysis = await self.analyze_requirements(user_requirements)
            
            # Step 2: Identify project type and complexity
            project_type = self.identify_project_type(user_requirements)
            complexity = self.assess_complexity(user_requirements, project_type)
            
            # Step 3: Decompose into epics and stories
            epics = await self.decompose_to_epics(analysis, project_type, complexity)
            
            # Step 4: Identify required agent capabilities
            required_capabilities = self.identify_agent_requirements(epics, project_type)
            
            # Step 5: Estimate timeline
            timeline = self.estimate_timeline(epics, complexity)
            
            # Step 6: Create execution strategy
            execution_strategy = self.create_execution_strategy(epics, required_capabilities)
            
            project_plan = {
                "summary": analysis.get('project_summary', 'Custom project'),
                "project_type": project_type,
                "complexity": complexity,
                "user_requirements": user_requirements,
                "analysis": analysis,
                "epics": epics,
                "required_capabilities": required_capabilities,
                "timeline": timeline,
                "execution_strategy": execution_strategy,
                "created_at": datetime.now().isoformat(),
                "total_estimated_hours": sum(epic.get('estimated_hours', 8) for epic in epics)
            }
            
            print(f"📋 Project plan created: {len(epics)} epics, ~{project_plan['total_estimated_hours']} hours")
            return project_plan
            
        except Exception as e:
            print(f"❌ Error creating project plan: {e}")
            return None
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """
        Analyze user requirements to extract key information.
        
        Args:
            requirements: Raw user requirements text
            
        Returns:
            Dictionary containing analyzed requirements
        """
        # Extract key entities and concepts
        words = requirements.lower().split()
        
        # Identify technical keywords
        technical_keywords = []
        for word in words:
            if word in ['react', 'vue', 'angular', 'nodejs', 'python', 'django', 'flask',
                       'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
                       'aws', 'gcp', 'azure', 'typescript', 'javascript', 'html', 'css']:
                technical_keywords.append(word)
        
        # Identify action verbs
        action_verbs = []
        for word in words:
            if word in ['create', 'build', 'develop', 'implement', 'design', 'optimize',
                       'integrate', 'deploy', 'test', 'document', 'analyze', 'visualize']:
                action_verbs.append(word)
        
        # Extract feature mentions
        features = []
        feature_patterns = [
            r'user\s+(?:authentication|login|registration)',
            r'(?:shopping|cart)',
            r'(?:payment|checkout)',
            r'(?:dashboard|admin\s+panel)',
            r'(?:real[- ]?time|live)\s+(?:updates|notifications|chat)',
            r'(?:search|filter)',
            r'(?:file\s+upload|image\s+upload)',
            r'(?:email|notification)s?',
            r'(?:api|rest|graphql)',
            r'(?:database|data\s+storage)',
            r'(?:mobile|responsive)',
            r'(?:testing|unit\s+tests)',
            r'(?:deployment|hosting)'
        ]
        
        for pattern in feature_patterns:
            matches = re.finditer(pattern, requirements.lower())
            for match in matches:
                features.append(match.group().strip())
        
        # Generate project summary
        if 'dashboard' in requirements.lower():
            project_summary = "Dashboard/Analytics Application"
        elif 'api' in requirements.lower():
            project_summary = "API Service"
        elif any(word in requirements.lower() for word in ['web', 'website', 'app']):
            project_summary = "Web Application"
        elif 'mobile' in requirements.lower():
            project_summary = "Mobile Application"
        elif any(word in requirements.lower() for word in ['docs', 'documentation', 'guide']):
            project_summary = "Documentation Project"
        else:
            project_summary = "Custom Software Project"
        
        return {
            "project_summary": project_summary,
            "technical_keywords": technical_keywords,
            "action_verbs": action_verbs,
            "features": features,
            "estimated_complexity": "medium",  # Will be refined
            "primary_focus": self.identify_primary_focus(requirements)
        }
    
    def identify_project_type(self, requirements: str) -> str:
        """
        Identify the type of project based on requirements.
        
        Args:
            requirements: User requirements text
            
        Returns:
            String identifying project type
        """
        req_lower = requirements.lower()
        
        for project_type, config in self.project_patterns.items():
            if any(keyword in req_lower for keyword in config['keywords']):
                return project_type
        
        return 'custom'
    
    def assess_complexity(self, requirements: str, project_type: str) -> str:
        """
        Assess project complexity based on requirements and type.
        
        Args:
            requirements: User requirements text
            project_type: Identified project type
            
        Returns:
            Complexity level: 'low', 'medium', 'high', or 'enterprise'
        """
        complexity_indicators = {
            'high': ['microservices', 'distributed', 'scalable', 'enterprise', 'multi-tenant',
                    'real-time', 'high-performance', 'machine learning', 'ai', 'big data'],
            'medium': ['authentication', 'database', 'api', 'integration', 'deployment',
                      'testing', 'responsive', 'mobile', 'dashboard'],
            'low': ['simple', 'basic', 'quick', 'prototype', 'mvp', 'landing page']
        }
        
        req_lower = requirements.lower()
        
        # Count indicators for each complexity level
        scores = {}
        for level, indicators in complexity_indicators.items():
            scores[level] = sum(1 for indicator in indicators if indicator in req_lower)
        
        # Determine complexity
        if scores['high'] >= 2:
            return 'high'
        elif scores['high'] >= 1 or scores['medium'] >= 3:
            return 'medium'
        elif scores['low'] >= 1 and scores['medium'] <= 1:
            return 'low'
        else:
            return 'medium'  # Default
    
    async def decompose_to_epics(self, analysis: Dict, project_type: str, complexity: str) -> List[Dict[str, Any]]:
        """
        Decompose the project into manageable epics.
        
        Args:
            analysis: Analyzed requirements
            project_type: Type of project
            complexity: Project complexity level
            
        Returns:
            List of epic definitions
        """
        epics = []
        
        # Base epics common to most projects
        if project_type in ['web_application', 'mobile_app']:
            epics.extend([
                {
                    "name": "Project Setup and Infrastructure",
                    "description": "Set up development environment, project structure, and basic infrastructure",
                    "priority": "high",
                    "estimated_hours": 8,
                    "required_capabilities": ["development_setup", "infrastructure"],
                    "tasks": [
                        "Initialize project repository",
                        "Set up development environment",
                        "Configure basic project structure",
                        "Set up CI/CD pipeline basics"
                    ]
                },
                {
                    "name": "Core Application Development",
                    "description": "Implement main application functionality and features",
                    "priority": "high", 
                    "estimated_hours": 24,
                    "required_capabilities": ["frontend", "backend"] if project_type == 'web_application' else ["mobile", "backend"],
                    "tasks": [
                        "Implement core business logic",
                        "Create user interface components",
                        "Set up data models and storage",
                        "Implement main user workflows"
                    ]
                }
            ])
        
        elif project_type == 'api_service':
            epics.extend([
                {
                    "name": "API Design and Setup",
                    "description": "Design API endpoints and set up service infrastructure",
                    "priority": "high",
                    "estimated_hours": 12,
                    "required_capabilities": ["backend", "api_design"],
                    "tasks": [
                        "Design API endpoints and schema",
                        "Set up service framework",
                        "Implement basic routing",
                        "Set up request/response handling"
                    ]
                },
                {
                    "name": "Business Logic Implementation", 
                    "description": "Implement core API functionality and business rules",
                    "priority": "high",
                    "estimated_hours": 16,
                    "required_capabilities": ["backend", "database"],
                    "tasks": [
                        "Implement core business logic",
                        "Set up data persistence",
                        "Add input validation",
                        "Implement error handling"
                    ]
                }
            ])
        
        elif project_type == 'documentation':
            epics.extend([
                {
                    "name": "Documentation Planning and Structure",
                    "description": "Plan documentation structure and create templates",
                    "priority": "high",
                    "estimated_hours": 6,
                    "required_capabilities": ["documentation", "technical_writing"],
                    "tasks": [
                        "Analyze documentation requirements",
                        "Create documentation structure",
                        "Set up templates and standards",
                        "Plan content organization"
                    ]
                },
                {
                    "name": "Content Creation",
                    "description": "Write and organize documentation content",
                    "priority": "high",
                    "estimated_hours": 16,
                    "required_capabilities": ["documentation", "technical_writing"],
                    "tasks": [
                        "Write main documentation content",
                        "Create examples and tutorials",
                        "Add diagrams and illustrations",
                        "Review and validate content"
                    ]
                }
            ])
        
        # Add feature-specific epics based on analysis
        if 'authentication' in analysis.get('features', []):
            epics.append({
                "name": "User Authentication System",
                "description": "Implement user registration, login, and authentication",
                "priority": "medium",
                "estimated_hours": 12,
                "required_capabilities": ["backend", "security"],
                "tasks": [
                    "Design authentication flow",
                    "Implement user registration",
                    "Add login/logout functionality", 
                    "Set up session management"
                ]
            })
        
        if any(feature in analysis.get('features', []) for feature in ['dashboard', 'admin panel']):
            epics.append({
                "name": "Dashboard and Admin Interface",
                "description": "Create administrative dashboard and management interface",
                "priority": "medium",
                "estimated_hours": 16,
                "required_capabilities": ["frontend", "ui_design"],
                "tasks": [
                    "Design dashboard layout",
                    "Implement data visualization",
                    "Add administrative controls",
                    "Create user management interface"
                ]
            })
        
        # Always add testing and deployment epics for medium/high complexity
        if complexity in ['medium', 'high']:
            epics.extend([
                {
                    "name": "Testing and Quality Assurance",
                    "description": "Implement comprehensive testing and quality checks",
                    "priority": "medium",
                    "estimated_hours": 8,
                    "required_capabilities": ["testing", "quality_assurance"],
                    "tasks": [
                        "Write unit tests",
                        "Implement integration tests",
                        "Set up automated testing",
                        "Perform quality review"
                    ]
                },
                {
                    "name": "Deployment and Launch",
                    "description": "Deploy application and prepare for production use",
                    "priority": "medium",
                    "estimated_hours": 6,
                    "required_capabilities": ["devops", "deployment"],
                    "tasks": [
                        "Set up production environment",
                        "Configure deployment pipeline",
                        "Perform production deployment",
                        "Monitor and validate launch"
                    ]
                }
            ])
        
        return epics
    
    def identify_agent_requirements(self, epics: List[Dict], project_type: str) -> List[str]:
        """
        Identify what types of agents are needed for this project.
        
        Args:
            epics: List of project epics
            project_type: Type of project
            
        Returns:
            List of required agent capabilities
        """
        required_capabilities = set()
        
        # Extract capabilities from all epics
        for epic in epics:
            epic_capabilities = epic.get('required_capabilities', [])
            required_capabilities.update(epic_capabilities)
        
        # Add default capabilities based on project type
        if project_type in self.project_patterns:
            typical_agents = self.project_patterns[project_type]['typical_agents']
            required_capabilities.update(typical_agents)
        
        return list(required_capabilities)
    
    def estimate_timeline(self, epics: List[Dict], complexity: str) -> Dict[str, Any]:
        """
        Estimate project timeline based on epics and complexity.
        
        Args:
            epics: List of project epics
            complexity: Project complexity level
            
        Returns:
            Dictionary containing timeline estimates
        """
        total_hours = sum(epic.get('estimated_hours', 8) for epic in epics)
        
        # Adjust for complexity
        complexity_multipliers = {
            'low': 1.0,
            'medium': 1.2,
            'high': 1.5,
            'enterprise': 2.0
        }
        
        adjusted_hours = total_hours * complexity_multipliers.get(complexity, 1.2)
        
        # Estimate based on parallel work
        estimated_days = max(3, adjusted_hours / 6)  # Assuming 6 productive hours per day
        estimated_completion = datetime.now() + timedelta(days=estimated_days)
        
        return {
            "total_estimated_hours": adjusted_hours,
            "estimated_days": estimated_days,
            "estimated_completion": estimated_completion.isoformat(),
            "complexity_adjustment": complexity_multipliers.get(complexity, 1.2),
            "confidence": "medium"  # Could be enhanced with historical data
        }
    
    def create_execution_strategy(self, epics: List[Dict], required_capabilities: List[str]) -> Dict[str, Any]:
        """
        Create an execution strategy for the project.
        
        Args:
            epics: List of project epics
            required_capabilities: Required agent capabilities
            
        Returns:
            Dictionary containing execution strategy
        """
        # Determine epic priorities and dependencies
        high_priority_epics = [epic for epic in epics if epic.get('priority') == 'high']
        medium_priority_epics = [epic for epic in epics if epic.get('priority') == 'medium']
        
        strategy = {
            "approach": "agile_iterative",
            "phases": [
                {
                    "name": "Foundation",
                    "epics": [epic['name'] for epic in high_priority_epics[:2]],
                    "parallel_execution": True
                },
                {
                    "name": "Core Development", 
                    "epics": [epic['name'] for epic in high_priority_epics[2:] + medium_priority_epics[:2]],
                    "parallel_execution": True
                },
                {
                    "name": "Finalization",
                    "epics": [epic['name'] for epic in medium_priority_epics[2:]],
                    "parallel_execution": False
                }
            ],
            "coordination_strategy": "daily_check_ins",
            "risk_mitigation": "regular_progress_reviews",
            "success_criteria": "all_epics_completed_successfully"
        }
        
        return strategy
    
    def identify_primary_focus(self, requirements: str) -> str:
        """
        Identify the primary focus area of the project.
        
        Args:
            requirements: User requirements text
            
        Returns:
            Primary focus area
        """
        focus_keywords = {
            'frontend': ['ui', 'interface', 'design', 'user experience', 'responsive'],
            'backend': ['api', 'server', 'database', 'logic', 'processing'],
            'data': ['analytics', 'dashboard', 'visualization', 'reports', 'data'],
            'integration': ['connect', 'integrate', 'sync', 'import', 'export'],
            'performance': ['fast', 'optimize', 'performance', 'scalable', 'efficient']
        }
        
        req_lower = requirements.lower()
        scores = {}
        
        for focus, keywords in focus_keywords.items():
            scores[focus] = sum(1 for keyword in keywords if keyword in req_lower)
        
        if not scores or max(scores.values()) == 0:
            return 'general'
        
        return max(scores, key=scores.get)