#!/usr/bin/env python3
"""
Self-Improvement Tracking System
Tracks how feedback drives document improvements over time.
"""

import json
import yaml
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import os

class SelfImprovementTracker:
    """Tracks feedback cycles and measures improvement over time."""
    
    def __init__(self, framework_dir: str = None):
        if framework_dir:
            self.framework_dir = Path(framework_dir)
        else:
            # Auto-detect framework directory
            current_dir = Path.cwd()
            if (current_dir / "agent-doc-system" / "framework").exists():
                self.framework_dir = current_dir / "agent-doc-system" / "framework"
            elif (current_dir / "framework").exists():
                self.framework_dir = current_dir / "framework"
            else:
                self.framework_dir = current_dir
                
        self.history_dir = self.framework_dir / "agent_communication" / "history" / "improvement_cycles"
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
    def track_improvement_cycle(self, doc_path: str, feedback_received: List[str], 
                              actions_taken: List[str], results: Dict[str, Any]) -> str:
        """
        Track a complete improvement cycle for a document.
        
        Args:
            doc_path: Path to the document
            feedback_received: List of feedback that triggered improvements
            actions_taken: List of actions taken in response
            results: Measured results of the improvements
            
        Returns:
            Cycle ID for tracking
        """
        cycle_id = f"{Path(doc_path).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cycle_data = {
            "cycle_id": cycle_id,
            "document_path": doc_path,
            "cycle_start": datetime.now().strftime("%Y-%m-%d"),
            "feedback_received": feedback_received,
            "actions_taken": actions_taken,
            "results": {
                "quality_improvement": results.get("quality_improvement", 0),
                "user_satisfaction_change": results.get("user_satisfaction_change", 0),
                "completion_date": results.get("completion_date", datetime.now().strftime("%Y-%m-%d")),
                "metrics": results.get("metrics", {})
            },
            "created_at": datetime.now().isoformat(),
            "next_review_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        
        # Save cycle data
        cycle_file = self.history_dir / f"{cycle_id}.json"
        with open(cycle_file, 'w') as f:
            json.dump(cycle_data, f, indent=2)
            
        return cycle_id
    
    def get_document_improvement_history(self, doc_path: str) -> List[Dict[str, Any]]:
        """Get all improvement cycles for a specific document."""
        doc_name = Path(doc_path).stem
        cycles = []
        
        for cycle_file in self.history_dir.glob(f"{doc_name}_*.json"):
            try:
                with open(cycle_file) as f:
                    cycle_data = json.load(f)
                    cycles.append(cycle_data)
            except Exception as e:
                print(f"Warning: Could not load cycle file {cycle_file}: {e}")
                
        return sorted(cycles, key=lambda x: x.get("created_at", ""))
    
    def analyze_improvement_trends(self, doc_path: str = None) -> Dict[str, Any]:
        """
        Analyze improvement trends across documents or for a specific document.
        
        Args:
            doc_path: Optional specific document path, or None for all documents
            
        Returns:
            Analysis of improvement trends
        """
        if doc_path:
            cycles = self.get_document_improvement_history(doc_path)
            doc_name = Path(doc_path).stem
        else:
            cycles = []
            for cycle_file in self.history_dir.glob("*.json"):
                try:
                    with open(cycle_file) as f:
                        cycles.append(json.load(f))
                except Exception:
                    continue
            doc_name = "all_documents"
            
        if not cycles:
            return {"error": "No improvement cycles found"}
            
        # Calculate trends
        quality_improvements = [c["results"]["quality_improvement"] for c in cycles 
                              if c["results"]["quality_improvement"] != 0]
        satisfaction_changes = [c["results"]["user_satisfaction_change"] for c in cycles 
                              if c["results"]["user_satisfaction_change"] != 0]
        
        analysis = {
            "document": doc_name,
            "total_cycles": len(cycles),
            "date_range": {
                "earliest": min(c["cycle_start"] for c in cycles) if cycles else None,
                "latest": max(c["cycle_start"] for c in cycles) if cycles else None
            },
            "quality_trends": {
                "average_improvement": sum(quality_improvements) / len(quality_improvements) if quality_improvements else 0,
                "total_improvement": sum(quality_improvements),
                "best_improvement": max(quality_improvements) if quality_improvements else 0,
                "improvement_cycles": len(quality_improvements)
            },
            "satisfaction_trends": {
                "average_change": sum(satisfaction_changes) / len(satisfaction_changes) if satisfaction_changes else 0,
                "total_change": sum(satisfaction_changes),
                "best_change": max(satisfaction_changes) if satisfaction_changes else 0,
                "measured_cycles": len(satisfaction_changes)
            },
            "common_feedback_types": self._analyze_feedback_patterns(cycles),
            "effective_actions": self._analyze_action_effectiveness(cycles),
            "recommendations": self._generate_improvement_recommendations(cycles)
        }
        
        return analysis
    
    def _analyze_feedback_patterns(self, cycles: List[Dict]) -> Dict[str, int]:
        """Analyze patterns in feedback received across cycles."""
        feedback_keywords = {}
        
        for cycle in cycles:
            for feedback in cycle.get("feedback_received", []):
                # Extract keywords from feedback
                words = re.findall(r'\b\w+\b', feedback.lower())
                for word in words:
                    if len(word) > 3:  # Ignore short words
                        feedback_keywords[word] = feedback_keywords.get(word, 0) + 1
                        
        # Return top feedback themes
        return dict(sorted(feedback_keywords.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _analyze_action_effectiveness(self, cycles: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze which actions were most effective."""
        action_results = {}
        
        for cycle in cycles:
            quality_improvement = cycle["results"]["quality_improvement"]
            for action in cycle.get("actions_taken", []):
                if action not in action_results:
                    action_results[action] = {"total_improvement": 0, "count": 0}
                action_results[action]["total_improvement"] += quality_improvement
                action_results[action]["count"] += 1
                
        # Calculate average effectiveness
        effectiveness = []
        for action, data in action_results.items():
            if data["count"] > 0:
                avg_improvement = data["total_improvement"] / data["count"]
                effectiveness.append({
                    "action": action,
                    "average_improvement": avg_improvement,
                    "usage_count": data["count"],
                    "total_improvement": data["total_improvement"]
                })
                
        return sorted(effectiveness, key=lambda x: x["average_improvement"], reverse=True)
    
    def _generate_improvement_recommendations(self, cycles: List[Dict]) -> List[str]:
        """Generate recommendations based on improvement history."""
        recommendations = []
        
        if not cycles:
            return ["No improvement history available for analysis"]
            
        # Analyze recent performance
        recent_cycles = [c for c in cycles if self._is_recent(c["cycle_start"])]
        
        if len(recent_cycles) == 0:
            recommendations.append("Consider starting new improvement cycles - no recent activity")
        elif len(recent_cycles) > 5:
            recommendations.append("High improvement activity - ensure changes are being measured effectively")
            
        # Quality trend analysis
        quality_improvements = [c["results"]["quality_improvement"] for c in cycles]
        avg_improvement = sum(quality_improvements) / len(quality_improvements) if quality_improvements else 0
        
        if avg_improvement < 5:
            recommendations.append("Consider more impactful improvement actions - current average improvement is low")
        elif avg_improvement > 20:
            recommendations.append("Excellent improvement results - document and share successful practices")
            
        # Frequency analysis
        if len(cycles) < 2:
            recommendations.append("Establish regular improvement cycles for consistent quality enhancement")
        elif len(cycles) > 10:
            recommendations.append("Consider consolidating improvement efforts - high cycle frequency detected")
            
        return recommendations
    
    def _is_recent(self, date_str: str, days: int = 90) -> bool:
        """Check if a date is within the last N days."""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return (datetime.now() - date).days <= days
        except ValueError:
            return False
    
    def update_document_feedback_with_cycles(self, doc_path: str) -> bool:
        """
        Update a document's feedback section with improvement cycle data.
        
        Args:
            doc_path: Path to the document to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get improvement history
            cycles = self.get_document_improvement_history(doc_path)
            if not cycles:
                return True  # No cycles to add
                
            # Read current document
            content = Path(doc_path).read_text()
            metadata = self._extract_metadata(content)
            
            if not metadata or 'feedback' not in metadata:
                return False  # Can't update without feedback section
                
            # Add self_improvement_tracking to feedback
            if 'self_improvement_tracking' not in metadata['feedback']:
                metadata['feedback']['self_improvement_tracking'] = {}
                
            metadata['feedback']['self_improvement_tracking']['improvement_cycles'] = cycles
            
            # Update the document
            updated_content = self._update_metadata_in_content(content, metadata)
            Path(doc_path).write_text(updated_content)
            
            return True
            
        except Exception as e:
            print(f"Error updating document feedback: {e}")
            return False
    
    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract YAML metadata from markdown content."""
        if match := re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL):
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return None
        return None
    
    def _update_metadata_in_content(self, content: str, metadata: Dict) -> str:
        """Update the YAML metadata section in markdown content."""
        yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        
        # Replace existing metadata
        pattern = r'```yaml\n(.*?)\n```'
        replacement = f'```yaml\n{yaml_str}```'
        
        if re.search(pattern, content, re.DOTALL):
            return re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
            # Add metadata at the beginning
            return f'```yaml\n{yaml_str}```\n\n{content}'
    
    def generate_improvement_report(self, output_path: str = None) -> str:
        """Generate a comprehensive improvement report."""
        if not output_path:
            output_path = self.framework_dir / "agent_communication" / "improvement_report.md"
            
        # Analyze all documents
        analysis = self.analyze_improvement_trends()
        
        report = f"""# Documentation Self-Improvement Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

- **Total Improvement Cycles**: {analysis.get('total_cycles', 0)}
- **Date Range**: {analysis.get('date_range', {}).get('earliest', 'N/A')} to {analysis.get('date_range', {}).get('latest', 'N/A')}
- **Average Quality Improvement**: {analysis.get('quality_trends', {}).get('average_improvement', 0):.1f} points
- **Total Quality Improvement**: {analysis.get('quality_trends', {}).get('total_improvement', 0):.1f} points

## Quality Trends

- **Improvement Cycles with Measured Results**: {analysis.get('quality_trends', {}).get('improvement_cycles', 0)}
- **Best Single Improvement**: {analysis.get('quality_trends', {}).get('best_improvement', 0):.1f} points
- **Average Satisfaction Change**: {analysis.get('satisfaction_trends', {}).get('average_change', 0):.1f} points

## Common Feedback Themes

"""
        
        for theme, count in analysis.get('common_feedback_types', {}).items():
            report += f"- **{theme}**: {count} occurrences\n"
            
        report += "\n## Most Effective Actions\n\n"
        
        for action_data in analysis.get('effective_actions', [])[:5]:
            report += f"- **{action_data['action']}**: {action_data['average_improvement']:.1f} avg improvement ({action_data['usage_count']} uses)\n"
            
        report += "\n## Recommendations\n\n"
        
        for rec in analysis.get('recommendations', []):
            report += f"- {rec}\n"
            
        report += f"""
## Self-Improvement Philosophy

This system embodies the philosophy of continuous improvement through:

1. **Measurable Feedback Cycles**: Every improvement is tracked and measured
2. **Data-Driven Decisions**: Actions are chosen based on proven effectiveness
3. **Continuous Learning**: Patterns are identified and used to inform future improvements
4. **Transparent Progress**: All improvements are documented and traceable

The goal is to create a self-reinforcing cycle where feedback drives improvements, 
which generate better outcomes, which provide more data for even better improvements.
"""
        
        Path(output_path).write_text(report)
        return str(output_path)

def main():
    """CLI interface for the self-improvement tracker."""
    if len(sys.argv) < 2:
        print("Usage: self_improvement_tracker.py <command> [args...]")
        print("Commands:")
        print("  track <doc_path> <feedback_file> <actions_file> <results_file>")
        print("  analyze [doc_path]")
        print("  report [output_path]")
        print("  update <doc_path>")
        sys.exit(1)
        
    command = sys.argv[1]
    tracker = SelfImprovementTracker()
    
    if command == "track":
        if len(sys.argv) != 6:
            print("Usage: track <doc_path> <feedback_file> <actions_file> <results_file>")
            sys.exit(1)
            
        doc_path = sys.argv[2]
        feedback_file = sys.argv[3]
        actions_file = sys.argv[4]
        results_file = sys.argv[5]
        
        # Load data from files
        with open(feedback_file) as f:
            feedback = json.load(f)
        with open(actions_file) as f:
            actions = json.load(f)
        with open(results_file) as f:
            results = json.load(f)
            
        cycle_id = tracker.track_improvement_cycle(doc_path, feedback, actions, results)
        print(f"Tracked improvement cycle: {cycle_id}")
        
    elif command == "analyze":
        doc_path = sys.argv[2] if len(sys.argv) > 2 else None
        analysis = tracker.analyze_improvement_trends(doc_path)
        print(json.dumps(analysis, indent=2))
        
    elif command == "report":
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        report_path = tracker.generate_improvement_report(output_path)
        print(f"Generated improvement report: {report_path}")
        
    elif command == "update":
        if len(sys.argv) != 3:
            print("Usage: update <doc_path>")
            sys.exit(1)
            
        doc_path = sys.argv[2]
        success = tracker.update_document_feedback_with_cycles(doc_path)
        if success:
            print(f"Updated document feedback: {doc_path}")
        else:
            print(f"Failed to update document: {doc_path}")
            
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()