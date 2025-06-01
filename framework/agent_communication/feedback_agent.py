#!/usr/bin/env python3
"""
AI Feedback Agent for Documentation Analysis
Provides automated feedback generation and assessment for documentation files.
"""

import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys
import os

class DocumentationFeedbackAgent:
    """AI agent for automated documentation feedback and assessment."""
    
    def __init__(self, agent_name: str = "FeedbackAgent"):
        self.agent_name = agent_name
        self.assessment_timestamp = datetime.now().isoformat()
        
    def analyze_document(self, doc_path: str) -> Dict[str, Any]:
        """
        Analyze a documentation file and provide comprehensive feedback.
        
        Args:
            doc_path: Path to the documentation file
            
        Returns:
            Complete feedback assessment dictionary
        """
        try:
            content = Path(doc_path).read_text()
            metadata = self._extract_metadata(content)
            
            # Generate all feedback components
            feedback = {
                "rating": self._calculate_overall_rating(content, metadata),
                "comments": self._generate_comments(content, metadata),
                "observations": self._generate_observations(content, metadata),
                "suggestions": self._generate_suggestions(content, metadata),
                "status": self._generate_status_assessment(content, metadata),
                "current_state": self._assess_current_state(content, metadata),
                "planned_state": self._suggest_planned_state(content, metadata),
                "importance": self._assess_importance(content, metadata),
                "agent_assessment": self._generate_agent_assessment(content, metadata)
            }
            
            return feedback
            
        except Exception as e:
            return self._generate_error_feedback(str(e))
    
    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract YAML metadata from markdown content."""
        if match := re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL):
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None
    
    def _calculate_overall_rating(self, content: str, metadata: Optional[Dict]) -> int:
        """Calculate overall quality rating (1-100)."""
        score = 50  # Base score
        
        # Content analysis
        if len(content) > 1000:
            score += 10  # Substantial content
        if len(content) > 3000:
            score += 5   # Comprehensive content
            
        # Structure analysis
        sections = re.findall(r'^#+\s', content, re.MULTILINE)
        if len(sections) >= 3:
            score += 10  # Well-structured
        if len(sections) >= 6:
            score += 5   # Very detailed
            
        # Metadata quality
        if metadata:
            score += 15  # Has metadata
            if metadata.get('feedback'):
                score += 10  # Has feedback section
        else:
            score -= 20  # Missing metadata
            
        # Code examples
        code_blocks = re.findall(r'```', content)
        if len(code_blocks) >= 2:  # At least one code block
            score += 8
        if len(code_blocks) >= 6:  # Multiple code blocks
            score += 7
            
        # Links and references
        links = re.findall(r'\[.*?\]\(.*?\)', content)
        if len(links) >= 3:
            score += 5
            
        return min(100, max(1, score))
    
    def _generate_comments(self, content: str, metadata: Optional[Dict]) -> str:
        """Generate human-readable feedback comments."""
        issues = []
        strengths = []
        
        # Analyze content
        if len(content) < 500:
            issues.append("document appears brief")
        else:
            strengths.append("substantial content")
            
        if not metadata:
            issues.append("missing metadata section")
        else:
            strengths.append("includes metadata")
            
        # Structure analysis
        sections = re.findall(r'^#+\s', content, re.MULTILINE)
        if len(sections) < 3:
            issues.append("could benefit from more sections")
        else:
            strengths.append("well-structured with multiple sections")
            
        # Generate comment
        comment_parts = []
        if strengths:
            comment_parts.append(f"Strengths: {', '.join(strengths)}")
        if issues:
            comment_parts.append(f"Areas for improvement: {', '.join(issues)}")
            
        return ". ".join(comment_parts) if comment_parts else "Document appears adequate."
    
    def _generate_observations(self, content: str, metadata: Optional[Dict]) -> List[Dict[str, str]]:
        """Generate structured observations."""
        observations = []
        
        # Content length observation
        word_count = len(content.split())
        if word_count < 200:
            observations.append({
                "what": "Document is relatively short",
                "impact": "May lack comprehensive coverage",
                "priority": "medium",
                "category": "quality"
            })
        elif word_count > 2000:
            observations.append({
                "what": "Document is comprehensive and detailed",
                "impact": "Provides thorough coverage but may be overwhelming",
                "priority": "low",
                "category": "usability"
            })
            
        # Metadata observation
        if not metadata:
            observations.append({
                "what": "Missing metadata section",
                "impact": "Reduces discoverability and validation compliance",
                "priority": "high",
                "category": "quality"
            })
            
        # Code examples
        code_blocks = re.findall(r'```', content)
        if len(code_blocks) < 2:
            observations.append({
                "what": "Limited or no code examples",
                "impact": "May reduce practical value for developers",
                "priority": "medium",
                "category": "usability"
            })
            
        return observations
    
    def _generate_suggestions(self, content: str, metadata: Optional[Dict]) -> List[Dict[str, str]]:
        """Generate actionable suggestions."""
        suggestions = []
        
        if not metadata:
            suggestions.append({
                "action": "Add machine-actionable metadata section",
                "priority": "high",
                "effort": "small",
                "impact": "high",
                "assignee": "documentation_team"
            })
            
        # Check for examples
        code_blocks = re.findall(r'```', content)
        if len(code_blocks) < 2:
            suggestions.append({
                "action": "Add practical code examples",
                "priority": "medium",
                "effort": "medium",
                "impact": "medium",
                "assignee": "technical_writer"
            })
            
        # Check for links
        links = re.findall(r'\[.*?\]\(.*?\)', content)
        if len(links) < 2:
            suggestions.append({
                "action": "Add relevant links and references",
                "priority": "low",
                "effort": "small",
                "impact": "low",
                "assignee": "documentation_team"
            })
            
        return suggestions
    
    def _generate_status_assessment(self, content: str, metadata: Optional[Dict]) -> Dict[str, str]:
        """Generate status assessment."""
        # Determine status based on analysis
        if not metadata:
            status_value = "needs_improvement"
            validation = "failed"
        elif len(content) < 300:
            status_value = "draft"
            validation = "pending"
        else:
            status_value = "approved"
            validation = "passed"
            
        return {
            "value": status_value,
            "updated_by": self.agent_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "validation": validation,
            "implementation": "complete" if status_value == "approved" else "in_progress"
        }
    
    def _assess_current_state(self, content: str, metadata: Optional[Dict]) -> Dict[str, Any]:
        """Assess current document state."""
        quality_score = self._calculate_overall_rating(content, metadata)
        
        # Calculate completeness
        sections = re.findall(r'^#+\s', content, re.MULTILINE)
        completeness = min(100, (len(sections) / 6) * 100)  # Expect ~6 sections for complete doc
        
        # Calculate accuracy (based on structure and metadata presence)
        accuracy = 90 if metadata else 60
        if len(content) > 1000:
            accuracy += 10
            
        # Calculate usability (based on examples and clarity)
        code_blocks = re.findall(r'```', content)
        usability = 70
        if len(code_blocks) >= 2:
            usability += 20
        if len(re.findall(r'\[.*?\]\(.*?\)', content)) >= 3:
            usability += 10
            
        return {
            "quality_score": quality_score,
            "completeness": min(100, completeness),
            "accuracy": min(100, accuracy),
            "usability": min(100, usability),
            "last_updated": self.assessment_timestamp,
            "assessed_by": self.agent_name
        }
    
    def _suggest_planned_state(self, content: str, metadata: Optional[Dict]) -> Dict[str, Any]:
        """Suggest planned improvements."""
        current_score = self._calculate_overall_rating(content, metadata)
        target_score = min(100, current_score + 20)
        
        improvements = []
        if not metadata:
            improvements.append({
                "improvement": "Add comprehensive metadata section",
                "expected_impact": 15,
                "effort_estimate": "small",
                "assigned_to": "documentation_team"
            })
            
        if len(re.findall(r'```', content)) < 2:
            improvements.append({
                "improvement": "Add practical code examples and demonstrations",
                "expected_impact": 10,
                "effort_estimate": "medium",
                "assigned_to": "technical_writer"
            })
            
        return {
            "target_quality_score": target_score,
            "target_date": (datetime.now().replace(month=datetime.now().month + 1) if datetime.now().month < 12 
                          else datetime.now().replace(year=datetime.now().year + 1, month=1)).strftime("%Y-%m-%d"),
            "planned_improvements": improvements
        }
    
    def _assess_importance(self, content: str, metadata: Optional[Dict]) -> Dict[str, str]:
        """Assess document importance."""
        # Simple heuristics for importance
        word_count = len(content.split())
        
        if word_count > 2000 or (metadata and "protocol" in str(metadata).lower()):
            business_value = "high"
            technical_priority = "high"
            user_impact = "high"
        elif word_count > 1000:
            business_value = "medium"
            technical_priority = "medium"
            user_impact = "medium"
        else:
            business_value = "low"
            technical_priority = "low"
            user_impact = "low"
            
        return {
            "business_value": business_value,
            "technical_priority": technical_priority,
            "user_impact": user_impact,
            "strategic_alignment": "medium",
            "dependency_level": "medium"
        }
    
    def _generate_agent_assessment(self, content: str, metadata: Optional[Dict]) -> Dict[str, Any]:
        """Generate honest AI assessment."""
        strengths = []
        weaknesses = []
        
        # Analyze strengths
        if metadata:
            strengths.append("includes structured metadata")
        if len(content) > 1500:
            strengths.append("comprehensive content coverage")
        if len(re.findall(r'```', content)) >= 2:
            strengths.append("includes practical code examples")
        if len(re.findall(r'^#+\s', content, re.MULTILINE)) >= 4:
            strengths.append("well-organized section structure")
            
        # Analyze weaknesses
        if not metadata:
            weaknesses.append("lacks machine-actionable metadata")
        if len(content) < 800:
            weaknesses.append("could be more comprehensive")
        if len(re.findall(r'```', content)) < 2:
            weaknesses.append("needs more practical examples")
        if len(re.findall(r'\[.*?\]\(.*?\)', content)) < 3:
            weaknesses.append("could benefit from more references")
            
        # Generate overall impression
        if len(strengths) > len(weaknesses):
            impression = "This is a well-structured document with good coverage. Minor improvements could enhance its value."
        elif len(weaknesses) > len(strengths):
            impression = "This document has potential but needs significant improvements to meet quality standards."
        else:
            impression = "This document is adequate but has room for improvement in several areas."
            
        confidence = min(95, 60 + (len(content) / 100))  # Higher confidence for longer documents
        
        return {
            "honest_thoughts": {
                "overall_impression": impression,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "confidence_level": confidence,
                "assessment_timestamp": self.assessment_timestamp
            },
            "automated_analysis": {
                "readability_score": self._calculate_readability(content),
                "technical_accuracy": 85 if metadata else 70,
                "completeness_gaps": self._identify_completeness_gaps(content, metadata),
                "consistency_issues": self._identify_consistency_issues(content)
            },
            "recommendations": self._generate_recommendations(content, metadata)
        }
    
    def _calculate_readability(self, content: str) -> float:
        """Simple readability assessment."""
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        
        if sentences == 0:
            return 50.0
            
        avg_sentence_length = words / sentences
        
        # Simple heuristic: optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            return 90.0
        elif 10 <= avg_sentence_length <= 25:
            return 75.0
        else:
            return 60.0
    
    def _identify_completeness_gaps(self, content: str, metadata: Optional[Dict]) -> List[str]:
        """Identify gaps in document completeness."""
        gaps = []
        
        if not re.search(r'(?i)example|demo|tutorial', content):
            gaps.append("Missing practical examples or tutorials")
        if not re.search(r'(?i)install|setup|getting.started', content):
            gaps.append("Missing installation or setup instructions")
        if not metadata or not metadata.get('changelog'):
            gaps.append("Missing or incomplete changelog")
            
        return gaps
    
    def _identify_consistency_issues(self, content: str) -> List[str]:
        """Identify consistency issues in the document."""
        issues = []
        
        # Check for consistent heading styles
        headings = re.findall(r'^(#+)\s', content, re.MULTILINE)
        if len(set(headings)) > 4:  # Too many heading levels
            issues.append("Inconsistent heading hierarchy")
            
        # Check for broken internal links (simple check)
        internal_links = re.findall(r'\[.*?\]\(#.*?\)', content)
        if internal_links:
            issues.append("Potential internal link validation needed")
            
        return issues
    
    def _generate_recommendations(self, content: str, metadata: Optional[Dict]) -> Dict[str, List[Dict]]:
        """Generate immediate and long-term recommendations."""
        immediate = []
        long_term = []
        
        if not metadata:
            immediate.append({
                "action": "Add metadata section with schema validation",
                "reason": "Required for automated validation and discoverability",
                "effort": "small",
                "expected_improvement": 15
            })
            
        if len(re.findall(r'```', content)) < 2:
            immediate.append({
                "action": "Add code examples and practical demonstrations",
                "reason": "Improves usability and practical value",
                "effort": "medium",
                "expected_improvement": 12
            })
            
        long_term.append({
            "improvement": "Implement automated content freshness monitoring",
            "justification": "Ensures document remains accurate and up-to-date",
            "estimated_effort": "medium",
            "strategic_value": "high"
        })
        
        long_term.append({
            "improvement": "Add interactive elements and user feedback collection",
            "justification": "Enables continuous improvement based on user needs",
            "estimated_effort": "large",
            "strategic_value": "medium"
        })
        
        return {
            "immediate_actions": immediate,
            "long_term_improvements": long_term
        }
    
    def _generate_error_feedback(self, error: str) -> Dict[str, Any]:
        """Generate feedback for documents that couldn't be analyzed."""
        return {
            "rating": 1,
            "comments": f"Document analysis failed: {error}",
            "observations": [{
                "what": "Document could not be analyzed",
                "impact": "Unable to provide feedback",
                "priority": "critical",
                "category": "quality"
            }],
            "suggestions": [{
                "action": "Fix document format and try analysis again",
                "priority": "critical",
                "effort": "small",
                "impact": "critical",
                "assignee": "documentation_team"
            }],
            "status": {
                "value": "needs_improvement",
                "updated_by": self.agent_name,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "validation": "failed",
                "implementation": "not_started"
            }
        }

def main():
    """CLI interface for the feedback agent."""
    if len(sys.argv) != 2:
        print("Usage: feedback_agent.py <document_path>")
        sys.exit(1)
        
    doc_path = sys.argv[1]
    if not Path(doc_path).exists():
        print(f"Error: Document not found: {doc_path}")
        sys.exit(1)
        
    agent = DocumentationFeedbackAgent()
    feedback = agent.analyze_document(doc_path)
    
    print(json.dumps(feedback, indent=2))

if __name__ == "__main__":
    main()