#!/usr/bin/env python3
"""
Agent Identity Verification System
Prevents agent identity spoofing by verifying locked agent configuration.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Tuple


class AgentIdentityVerifier:
    """Verifies agent identity using locked configuration and multiple validation layers."""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config_dir = self.project_root / ".agent_config"
        self.config_file = self.config_dir / "agent_name.json"
        
    def get_verified_agent_identity(self) -> Tuple[Optional[str], Dict[str, any]]:
        """
        Get verified agent identity with multiple security checks.
        
        Returns:
            Tuple of (agent_name, verification_details)
        """
        verification = {
            "config_exists": False,
            "config_valid": False,
            "env_matches": False,
            "identity_verified": False,
            "security_level": "none",
            "agent_name": None,
            "errors": []
        }
        
        try:
            # Check 1: Configuration file exists and is readable
            if not self.config_file.exists():
                verification["errors"].append("No agent configuration found")
                return None, verification
            
            verification["config_exists"] = True
            
            # Check 2: Load and validate configuration
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                required_fields = ["agent_name", "locked", "locked_at", "project_directory"]
                if not all(field in config for field in required_fields):
                    verification["errors"].append("Invalid configuration format")
                    return None, verification
                    
                if not config.get("locked", False):
                    verification["errors"].append("Agent configuration not locked")
                    return None, verification
                    
                verification["config_valid"] = True
                agent_name = config["agent_name"]
                verification["agent_name"] = agent_name
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                verification["errors"].append(f"Configuration parsing error: {e}")
                return None, verification
            
            # Check 3: Environment variable matches configuration
            env_agent_name = os.getenv('AGENT_NAME')
            if env_agent_name and env_agent_name == agent_name:
                verification["env_matches"] = True
                verification["security_level"] = "basic"
            else:
                verification["errors"].append(f"Environment mismatch: env='{env_agent_name}' config='{agent_name}'")
            
            # Check 4: Project directory verification
            config_project_dir = Path(config.get("project_directory", ""))
            if config_project_dir.resolve() != self.project_root.resolve():
                verification["errors"].append("Project directory mismatch")
                return None, verification
            
            # Check 5: Configuration integrity (basic tamper detection)
            config_timestamp = config.get("locked_at")
            if config_timestamp:
                # Additional integrity checks could go here
                verification["security_level"] = "verified"
                verification["identity_verified"] = True
                
            return agent_name, verification
            
        except Exception as e:
            verification["errors"].append(f"Verification failed: {e}")
            return None, verification
    
    def is_privileged_agent(self, agent_name: str) -> bool:
        """
        Check if agent has framework modification privileges.
        
        Note: Currently only 'DocSystemAgent' is privileged, but this will expand
        with Moirai OVERSEER to include role-based permissions.
        """
        # Current privileged agents
        privileged_agents = {
            "DocSystemAgent",  # Primary framework agent (locked)
            "MoiraiOverseer",  # Future OVERSEER agent
        }
        
        return agent_name in privileged_agents
    
    def verify_framework_access(self, requested_owner: str) -> Tuple[bool, str, Dict]:
        """
        Comprehensive framework access verification.
        
        Args:
            requested_owner: The owner name being claimed
            
        Returns:
            Tuple of (access_granted, verified_agent_name, details)
        """
        # Get actual agent identity
        verified_agent, verification = self.get_verified_agent_identity()
        
        if not verified_agent:
            return False, None, {
                "reason": "Agent identity could not be verified",
                "verification": verification,
                "security_violation": True
            }
        
        # Check if agent is trying to spoof identity
        if requested_owner != verified_agent:
            return False, verified_agent, {
                "reason": f"Identity spoofing detected: claimed '{requested_owner}' but verified as '{verified_agent}'",
                "verification": verification,
                "security_violation": True,
                "spoofing_attempt": True
            }
        
        # Check if agent has framework privileges
        has_privileges = self.is_privileged_agent(verified_agent)
        
        return has_privileges, verified_agent, {
            "reason": "Access granted" if has_privileges else "Insufficient privileges",
            "verification": verification,
            "privileges": has_privileges,
            "security_violation": False
        }


def verify_agent_for_framework_access(requested_owner: str, project_root: str = None) -> Tuple[bool, str, Dict]:
    """
    Convenience function for framework access verification.
    
    Args:
        requested_owner: The owner name being claimed
        project_root: Optional project root path
        
    Returns:
        Tuple of (access_granted, verified_agent_name, verification_details)
    """
    verifier = AgentIdentityVerifier(project_root)
    return verifier.verify_framework_access(requested_owner)


if __name__ == "__main__":
    # Test the verification system
    import sys
    
    requested_owner = sys.argv[1] if len(sys.argv) > 1 else "DocSystemAgent"
    
    access_granted, verified_agent, details = verify_agent_for_framework_access(requested_owner)
    
    print(f"Requested Owner: {requested_owner}")
    print(f"Verified Agent: {verified_agent}")
    print(f"Access Granted: {access_granted}")
    print(f"Details: {details}")
    
    if details.get("security_violation"):
        print("🚨 SECURITY VIOLATION DETECTED!")
        sys.exit(1)
    elif access_granted:
        print("✅ Framework access verified")
        sys.exit(0)
    else:
        print("❌ Framework access denied")
        sys.exit(1)