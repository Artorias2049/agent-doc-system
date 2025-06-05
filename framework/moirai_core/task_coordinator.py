"""
Task Coordinator for Moirai

Responsible for assigning tasks from project plans to available
agents in the Agora marketplace using intelligent matching algorithms.
"""

from typing import Dict, List, Optional, Any, Tuple
import json
from datetime import datetime

from ..mcp_integration.agora_client import AgoraClient


class TaskCoordinator:
    """
    Intelligently assigns tasks to available agents based on:
    - Agent capabilities and proficiency levels
    - Current workload and availability
    - Task requirements and complexity
    - Performance history (future enhancement)
    """
    
    def __init__(self, agora_client: AgoraClient):
        """
        Initialize the task coordinator.
        
        Args:
            agora_client: Connected Agora client for coordination
        """
        self.agora = agora_client
        
        # Scoring weights for agent selection
        self.selection_weights = {
            'capability_match': 0.40,    # How well capabilities match requirements
            'availability': 0.20,        # Current workload and availability
            'performance': 0.30,         # Historical performance (placeholder)
            'workload_balance': 0.10     # Helps distribute work evenly
        }
    
    async def assign_tasks(self, 
                          project_plan: Dict[str, Any], 
                          available_agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assign tasks from a project plan to available agents.
        
        Args:
            project_plan: Project plan containing epics and requirements
            available_agents: List of agents available in Agora
            
        Returns:
            List of task assignments with agent mappings
        """
        assignments = []
        epics = project_plan.get('epics', [])
        
        print(f"🎯 Assigning {len(epics)} epics to {len(available_agents)} available agents...")
        
        # Convert epics to individual tasks
        all_tasks = []
        for epic in epics:
            epic_tasks = self.epic_to_tasks(epic)
            all_tasks.extend(epic_tasks)
        
        print(f"📋 Decomposed into {len(all_tasks)} individual tasks")
        
        # Score and rank agents for each task
        for task in all_tasks:
            best_agent = await self.find_best_agent_for_task(task, available_agents)
            
            if best_agent:
                assignment = {
                    'task': task,
                    'agent_id': best_agent['agent_id'],
                    'agent_name': best_agent.get('agent_name', best_agent['agent_id']),
                    'match_score': best_agent.get('match_score', 0),
                    'assignment_reason': best_agent.get('assignment_reason', 'Best available match'),
                    'assigned_at': datetime.now().isoformat()
                }
                assignments.append(assignment)
                
                # Update agent workload for subsequent assignments
                self.update_agent_workload(available_agents, best_agent['agent_id'], task)
            else:
                print(f"⚠️  No suitable agent found for task: {task['name']}")
                # Create unassigned task entry
                assignments.append({
                    'task': task,
                    'agent_id': None,
                    'status': 'unassigned',
                    'reason': 'No suitable agent available'
                })
        
        assigned_count = len([a for a in assignments if a.get('agent_id')])
        print(f"✅ Successfully assigned {assigned_count}/{len(all_tasks)} tasks")
        
        return assignments
    
    def epic_to_tasks(self, epic: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break down an epic into individual tasks.
        
        Args:
            epic: Epic definition from project plan
            
        Returns:
            List of individual task definitions
        """
        tasks = []
        epic_tasks = epic.get('tasks', [])
        
        if not epic_tasks:
            # If no tasks specified, create one task for the entire epic
            tasks.append({
                'name': epic['name'],
                'description': epic['description'],
                'type': 'epic_implementation',
                'priority': epic.get('priority', 'medium'),
                'estimated_hours': epic.get('estimated_hours', 8),
                'required_capabilities': epic.get('required_capabilities', []),
                'epic_name': epic['name']
            })
        else:
            # Create individual tasks
            hours_per_task = epic.get('estimated_hours', 8) / len(epic_tasks)
            
            for i, task_name in enumerate(epic_tasks):
                task = {
                    'name': task_name,
                    'description': f"{task_name} (part of {epic['name']})",
                    'type': 'epic_task',
                    'priority': epic.get('priority', 'medium'),
                    'estimated_hours': hours_per_task,
                    'required_capabilities': epic.get('required_capabilities', []),
                    'epic_name': epic['name'],
                    'task_index': i
                }
                tasks.append(task)
        
        return tasks
    
    async def find_best_agent_for_task(self, 
                                      task: Dict[str, Any], 
                                      available_agents: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Find the best agent for a specific task using multi-criteria scoring.
        
        Args:
            task: Task definition
            available_agents: List of available agents
            
        Returns:
            Best agent for the task, or None if no suitable agent found
        """
        if not available_agents:
            return None
        
        required_capabilities = task.get('required_capabilities', [])
        
        # Score each agent for this task
        agent_scores = []
        
        for agent in available_agents:
            score = self.score_agent_for_task(agent, task)
            
            if score > 0:  # Only consider agents with positive scores
                agent_copy = agent.copy()
                agent_copy['match_score'] = score
                agent_copy['assignment_reason'] = self.generate_assignment_reason(agent, task, score)
                agent_scores.append(agent_copy)
        
        if not agent_scores:
            return None
        
        # Sort by score (highest first) and return best match
        agent_scores.sort(key=lambda x: x['match_score'], reverse=True)
        return agent_scores[0]
    
    def score_agent_for_task(self, agent: Dict[str, Any], task: Dict[str, Any]) -> float:
        """
        Score how well an agent matches a task using multiple criteria.
        
        Args:
            agent: Agent information
            task: Task definition
            
        Returns:
            Score between 0-100 (higher is better match)
        """
        required_capabilities = task.get('required_capabilities', [])
        agent_capabilities = agent.get('capabilities', [])
        
        # 1. Capability Match Score (40% weight)
        capability_score = self.calculate_capability_match(agent_capabilities, required_capabilities)
        
        # 2. Availability Score (20% weight)
        availability_score = self.calculate_availability_score(agent)
        
        # 3. Performance Score (30% weight) - placeholder for now
        performance_score = self.calculate_performance_score(agent, task)
        
        # 4. Workload Balance Score (10% weight)
        workload_score = self.calculate_workload_balance_score(agent)
        
        # Calculate weighted total
        total_score = (
            capability_score * self.selection_weights['capability_match'] +
            availability_score * self.selection_weights['availability'] +
            performance_score * self.selection_weights['performance'] +
            workload_score * self.selection_weights['workload_balance']
        )
        
        return total_score
    
    def calculate_capability_match(self, agent_capabilities: List[str], required_capabilities: List[str]) -> float:
        """
        Calculate how well agent capabilities match task requirements.
        
        Args:
            agent_capabilities: Capabilities the agent has
            required_capabilities: Capabilities the task needs
            
        Returns:
            Score 0-100
        """
        if not required_capabilities:
            return 50  # Neutral score if no specific requirements
        
        # Direct matches
        direct_matches = set(agent_capabilities) & set(required_capabilities)
        match_ratio = len(direct_matches) / len(required_capabilities)
        
        # Bonus for having more capabilities than required
        extra_capabilities = len(agent_capabilities) - len(required_capabilities)
        extra_bonus = min(10, extra_capabilities * 2)  # Max 10 bonus points
        
        # Related capability matching (simplified)
        related_score = self.calculate_related_capability_score(agent_capabilities, required_capabilities)
        
        base_score = match_ratio * 80  # Up to 80 points for direct matches
        total_score = min(100, base_score + extra_bonus + related_score)
        
        return total_score
    
    def calculate_related_capability_score(self, agent_caps: List[str], required_caps: List[str]) -> float:
        """
        Calculate score for related but not exact capability matches.
        
        Args:
            agent_caps: Agent capabilities
            required_caps: Required capabilities
            
        Returns:
            Additional score for related capabilities (0-20)
        """
        # Define related capability groups
        capability_groups = {
            'frontend': ['react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css', 'ui_design'],
            'backend': ['nodejs', 'python', 'java', 'django', 'flask', 'api_design', 'microservices'],
            'database': ['postgresql', 'mysql', 'mongodb', 'redis', 'database_design', 'sql'],
            'mobile': ['react_native', 'flutter', 'ios', 'android', 'mobile_design'],
            'devops': ['docker', 'kubernetes', 'aws', 'gcp', 'azure', 'deployment', 'ci_cd'],
            'testing': ['unit_testing', 'integration_testing', 'automated_testing', 'quality_assurance'],
            'documentation': ['technical_writing', 'api_documentation', 'user_guides', 'documentation']
        }
        
        related_score = 0
        
        for required_cap in required_caps:
            if required_cap in agent_caps:
                continue  # Already counted in direct matches
            
            # Find which group this capability belongs to
            for group_name, group_caps in capability_groups.items():
                if required_cap in group_caps:
                    # Check if agent has other capabilities in this group
                    agent_group_caps = set(agent_caps) & set(group_caps)
                    if agent_group_caps:
                        related_score += 5  # 5 points per related capability
                        break
        
        return min(20, related_score)  # Max 20 points for related capabilities
    
    def calculate_availability_score(self, agent: Dict[str, Any]) -> float:
        """
        Calculate agent availability score based on current workload.
        
        Args:
            agent: Agent information
            
        Returns:
            Score 0-100 (higher = more available)
        """
        # Get current workload (this would be enhanced with real data)
        current_workload = agent.get('current_workload', 0)
        max_workload = agent.get('max_workload', 10)
        
        if max_workload == 0:
            return 50  # Neutral if no workload info
        
        utilization = current_workload / max_workload
        
        if utilization <= 0.5:
            return 100  # Highly available
        elif utilization <= 0.7:
            return 80   # Good availability
        elif utilization <= 0.9:
            return 60   # Moderate availability
        else:
            return 20   # Low availability
    
    def calculate_performance_score(self, agent: Dict[str, Any], task: Dict[str, Any]) -> float:
        """
        Calculate performance score based on historical performance.
        
        Args:
            agent: Agent information
            task: Task definition
            
        Returns:
            Score 0-100
        """
        # Placeholder - would use real performance metrics
        base_performance = agent.get('performance_rating', 75)  # Default to 75
        
        # Adjust based on task type experience
        task_type = task.get('type', 'general')
        agent_experience = agent.get('task_experience', {})
        
        if task_type in agent_experience:
            experience_modifier = min(15, agent_experience[task_type] * 3)  # Max 15 bonus
            return min(100, base_performance + experience_modifier)
        
        return base_performance
    
    def calculate_workload_balance_score(self, agent: Dict[str, Any]) -> float:
        """
        Calculate score to promote workload balancing across agents.
        
        Args:
            agent: Agent information
            
        Returns:
            Score 0-100
        """
        current_workload = agent.get('current_workload', 0)
        
        # Prefer agents with lower current workload
        if current_workload == 0:
            return 100
        elif current_workload <= 2:
            return 80
        elif current_workload <= 5:
            return 60
        else:
            return 40
    
    def update_agent_workload(self, 
                             available_agents: List[Dict[str, Any]], 
                             agent_id: str, 
                             task: Dict[str, Any]) -> None:
        """
        Update an agent's workload after task assignment.
        
        Args:
            available_agents: List of available agents to update
            agent_id: ID of agent to update
            task: Task that was assigned
        """
        for agent in available_agents:
            if agent.get('agent_id') == agent_id:
                current_workload = agent.get('current_workload', 0)
                task_workload = self.estimate_task_workload(task)
                agent['current_workload'] = current_workload + task_workload
                break
    
    def estimate_task_workload(self, task: Dict[str, Any]) -> int:
        """
        Estimate workload impact of a task.
        
        Args:
            task: Task definition
            
        Returns:
            Workload impact (1-5 scale)
        """
        estimated_hours = task.get('estimated_hours', 4)
        priority = task.get('priority', 'medium')
        
        # Base workload from hours
        if estimated_hours <= 2:
            base_workload = 1
        elif estimated_hours <= 8:
            base_workload = 2
        elif estimated_hours <= 16:
            base_workload = 3
        else:
            base_workload = 4
        
        # Priority modifier
        if priority == 'high':
            base_workload += 1
        
        return min(5, base_workload)
    
    def generate_assignment_reason(self, 
                                  agent: Dict[str, Any], 
                                  task: Dict[str, Any], 
                                  score: float) -> str:
        """
        Generate human-readable reason for task assignment.
        
        Args:
            agent: Assigned agent
            task: Task that was assigned
            score: Match score
            
        Returns:
            Human-readable assignment reason
        """
        agent_capabilities = agent.get('capabilities', [])
        required_capabilities = task.get('required_capabilities', [])
        
        matches = set(agent_capabilities) & set(required_capabilities)
        
        if score >= 90:
            reason = f"Excellent match - has all required capabilities: {', '.join(matches)}"
        elif score >= 75:
            reason = f"Strong match - has key capabilities: {', '.join(matches)}"
        elif score >= 60:
            reason = f"Good match - has relevant experience and some required capabilities"
        elif score >= 40:
            reason = f"Moderate match - available and has some relevant skills"
        else:
            reason = f"Best available option - limited alternatives"
        
        return reason