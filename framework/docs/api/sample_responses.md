# Enhanced Metadata API Sample Responses

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "DocSystemAgent"
  title: "Enhanced Metadata API Sample Responses"
  description: "Real-world examples of API responses for UI integration reference"
content:
  overview: "This document provides real-world examples of API responses that the UI agent will receive when integrating with the enhanced metadata system."
  key_components: "Single File Response, List Files Response, Search Results, WebSocket Events, Error Responses"
  sections:
    - title: "Overview"
      content: "Complete examples of all API response formats"
    - title: "Single File Metadata"
      content: "Detailed metadata response for individual files"
    - title: "File Listings"
      content: "Paginated file list responses with summaries"
    - title: "Search Results"
      content: "Search response format with facets and highlights"
    - title: "WebSocket Events"
      content: "Real-time event payload examples"
    - title: "Error Responses"
      content: "Common error response formats"
  changelog:
    - version: "1.0.0"
      date: "2025-06-03"
      changes:
        - "Initial sample responses document"
        - "Complete examples for all endpoint types"
        - "Real metadata from actual system files"
        - "WebSocket event payloads included"
feedback:
  rating: 91
  comments: "Comprehensive sample responses with realistic data for UI development"
  observations:
    - what: "Real-world examples from actual system files"
      impact: "Accurate representation for developers"
      priority: "low"
      category: "quality"
    - what: "All response types covered"
      impact: "Complete reference for implementation"
      priority: "low"
      category: "quality"
  suggestions:
    - action: "Add edge case examples"
      priority: "medium"
      effort: "small"
      impact: "medium"
      assignee: "api_team"
    - action: "Include performance timing data"
      priority: "low"
      effort: "small"
      impact: "low"
      assignee: "api_team"
  status:
    value: "approved"
    updated_by: "DocSystemAgent"
    date: "2025-06-03"
    validation: "passed"
    implementation: "complete"
```

This document provides real-world examples of API responses that the UI agent will receive when integrating with the enhanced metadata system.

## 1. Single File Metadata Response

### Documentation File Example

**Request:** `GET /api/v1/metadata/framework/docs/agent_onboarding.md`

**Response:**
```json
{
  "status": "success",
  "data": {
    "metadata": {
      "schema": "https://schema.org/TechnicalDocument",
      "version": "2.3.0",
      "status": "Active",
      "owner": "DocSystemAgent",
      "title": "Agent Onboarding Guide",
      "description": "Comprehensive guide for new agents joining THE PROTOCOL v2.3.0",
      "file_type": "documentation",
      "tags": [
        "onboarding",
        "agents",
        "protocol",
        "getting-started",
        "essential"
      ],
      "dependencies": [
        {
          "file": "framework/docs/documentation_protocol.md",
          "type": "required"
        },
        {
          "file": "framework/schemas/document_protocol.yml",
          "type": "required"
        },
        {
          "file": "framework/scripts/setup_agent_name.sh",
          "type": "referenced"
        }
      ]
    },
    "assessment": {
      "quality_score": 95,
      "validation_status": "passed",
      "validation_errors": [],
      "last_assessed": "2025-06-03T10:30:00Z",
      "assessed_by": "DocSystemAgent",
      "improvement_velocity": {
        "last_7_days": 12,
        "last_30_days": 25,
        "trend": "improving"
      },
      "metrics": {
        "completeness": 98,
        "accuracy": 96,
        "clarity": 92,
        "consistency": 94,
        "usability": 95
      },
      "priority": {
        "business_value": "critical",
        "technical_priority": "high",
        "urgency": "medium"
      }
    },
    "system": {
      "created_at": "2025-05-15T08:00:00Z",
      "modified_at": "2025-06-03T10:25:00Z",
      "file_size": 45678,
      "file_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "git_info": {
        "last_commit": "docs: update agent onboarding to THE PROTOCOL v2.3.0",
        "last_author": "DocSystemAgent",
        "commit_count": 47,
        "branch": "main"
      },
      "agent_activity": {
        "last_reviewed_by": "DocSystemAgent",
        "review_count": 12,
        "collaborators": [
          "DocSystemAgent",
          "Claude-MCP-Research",
          "UI-Integration-Agent"
        ]
      },
      "automation": {
        "auto_assess": true,
        "assessment_frequency": "on_change",
        "alerts_enabled": true,
        "quality_threshold": 90
      }
    },
    "relationships": {
      "parent_docs": [],
      "child_docs": [
        "framework/docs/components/agent_communication/overview.md",
        "framework/docs/components/feedback/overview.md"
      ],
      "related_files": [
        {
          "file": "framework/agent_communication/feedback_agent.py",
          "relationship": "implements"
        },
        {
          "file": "tests/test_agent_onboarding.py",
          "relationship": "tests"
        }
      ],
      "external_links": [
        {
          "url": "https://github.com/your-org/agent-doc-system",
          "type": "resource",
          "status": "active"
        }
      ]
    },
    "feedback": {
      "current_issues": [],
      "improvement_suggestions": [
        {
          "suggestion": "Add troubleshooting section for common onboarding issues",
          "effort": "small",
          "impact": 20,
          "priority": "medium"
        },
        {
          "suggestion": "Include video tutorial links for visual learners",
          "effort": "medium",
          "impact": 30,
          "priority": "low"
        }
      ],
      "agent_notes": [
        {
          "agent": "UI-Integration-Agent",
          "note": "This document is essential for new agent onboarding flow",
          "timestamp": "2025-06-02T14:30:00Z"
        },
        {
          "agent": "DocSystemAgent",
          "note": "Updated to reflect v2.3.0 protocol changes",
          "timestamp": "2025-06-03T10:30:00Z"
        }
      ]
    }
  }
}
```

### Code File Example

**Request:** `GET /api/v1/metadata/framework/agent_communication/feedback_agent.py`

**Response:**
```json
{
  "status": "success",
  "data": {
    "metadata": {
      "schema": "https://schema.org/SoftwareSourceCode",
      "version": "1.5.0",
      "status": "Active",
      "owner": "Claude-MCP-Research",
      "title": "Feedback Agent Implementation",
      "description": "Core feedback processing agent with AI-powered analysis",
      "file_type": "code",
      "tags": [
        "agent",
        "feedback",
        "ai",
        "core-component",
        "python"
      ],
      "dependencies": [
        {
          "file": "framework/agent_communication/core/models.py",
          "type": "required"
        },
        {
          "file": "framework/schemas/enhanced_feedback_schema.yml",
          "type": "required"
        }
      ]
    },
    "assessment": {
      "quality_score": 88,
      "validation_status": "passed",
      "validation_errors": [],
      "last_assessed": "2025-06-03T11:00:00Z",
      "assessed_by": "CodeAnalysisAgent",
      "improvement_velocity": {
        "last_7_days": 5,
        "last_30_days": 18,
        "trend": "stable"
      },
      "metrics": {
        "completeness": 90,
        "accuracy": 88,
        "clarity": 85,
        "consistency": 89,
        "usability": 88
      },
      "code_metrics": {
        "complexity_score": 78,
        "test_coverage": 92.5,
        "documentation_coverage": 88.0,
        "maintainability_index": 85,
        "lines_of_code": 687,
        "cyclomatic_complexity": 14
      },
      "priority": {
        "business_value": "high",
        "technical_priority": "critical",
        "urgency": "low"
      }
    },
    "system": {
      "created_at": "2025-05-20T12:00:00Z",
      "modified_at": "2025-06-02T16:45:00Z",
      "file_size": 28456,
      "file_hash": "sha256:d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
      "git_info": {
        "last_commit": "feat: implement enhanced metadata system for dashboard integration",
        "last_author": "Claude-MCP-Research",
        "commit_count": 89,
        "branch": "feature/comprehensive-feedback-system"
      },
      "agent_activity": {
        "last_reviewed_by": "CodeAnalysisAgent",
        "review_count": 23,
        "collaborators": [
          "Claude-MCP-Research",
          "DocSystemAgent",
          "TestingAgent"
        ]
      },
      "automation": {
        "auto_assess": true,
        "assessment_frequency": "on_change",
        "alerts_enabled": true,
        "quality_threshold": 85
      }
    },
    "relationships": {
      "parent_docs": [
        "framework/docs/components/feedback/overview.md"
      ],
      "child_docs": [],
      "related_files": [
        {
          "file": "tests/test_feedback_agent.py",
          "relationship": "tests"
        },
        {
          "file": "framework/agent_communication/core/models.py",
          "relationship": "extends"
        },
        {
          "file": "framework/docs/api/enhanced_metadata_api.md",
          "relationship": "documents"
        }
      ],
      "external_links": []
    },
    "feedback": {
      "current_issues": [
        {
          "type": "performance",
          "severity": "medium",
          "description": "Feedback processing could be optimized for large batches",
          "suggested_fix": "Implement batch processing with async operations"
        }
      ],
      "improvement_suggestions": [
        {
          "suggestion": "Add caching layer for frequently accessed feedback data",
          "effort": "medium",
          "impact": 40,
          "priority": "high"
        },
        {
          "suggestion": "Refactor complex methods to reduce cyclomatic complexity",
          "effort": "large",
          "impact": 25,
          "priority": "medium"
        }
      ],
      "agent_notes": [
        {
          "agent": "CodeAnalysisAgent",
          "note": "Consider breaking down process_feedback method into smaller functions",
          "timestamp": "2025-06-03T11:00:00Z"
        }
      ]
    }
  }
}
```

## 2. File List Response

**Request:** `GET /api/v1/metadata?file_type=documentation&quality_threshold=85&per_page=10`

**Response:**
```json
{
  "status": "success",
  "data": {
    "files": [
      {
        "path": "framework/docs/agent_onboarding.md",
        "metadata": {
          "title": "Agent Onboarding Guide",
          "status": "Active",
          "owner": "DocSystemAgent",
          "file_type": "documentation",
          "tags": ["onboarding", "agents", "protocol"]
        },
        "assessment": {
          "quality_score": 95,
          "validation_status": "passed",
          "last_assessed": "2025-06-03T10:30:00Z",
          "improvement_velocity": {
            "trend": "improving"
          },
          "priority": {
            "business_value": "critical"
          }
        }
      },
      {
        "path": "framework/docs/documentation_protocol.md",
        "metadata": {
          "title": "Documentation Protocol Specification",
          "status": "Active",
          "owner": "DocSystemAgent",
          "file_type": "documentation",
          "tags": ["protocol", "standards", "guidelines"]
        },
        "assessment": {
          "quality_score": 93,
          "validation_status": "passed",
          "last_assessed": "2025-06-03T09:15:00Z",
          "improvement_velocity": {
            "trend": "stable"
          },
          "priority": {
            "business_value": "high"
          }
        }
      },
      {
        "path": "framework/docs/api/enhanced_metadata_api.md",
        "metadata": {
          "title": "Enhanced Metadata API Specification",
          "status": "Active",
          "owner": "DocSystemAgent",
          "file_type": "documentation",
          "tags": ["api", "metadata", "integration"]
        },
        "assessment": {
          "quality_score": 91,
          "validation_status": "passed",
          "last_assessed": "2025-06-03T12:00:00Z",
          "improvement_velocity": {
            "trend": "improving"
          },
          "priority": {
            "business_value": "critical"
          }
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 45,
      "pages": 5
    },
    "summary": {
      "total_files": 45,
      "average_quality": 89.2,
      "files_by_type": {
        "documentation": 45
      },
      "validation_status": {
        "passed": 42,
        "failed": 2,
        "warning": 1
      }
    }
  }
}
```

## 3. Search Results Response

**Request:** `POST /api/v1/metadata/search`
```json
{
  "query": "feedback agent implementation",
  "filters": {
    "file_types": ["code", "documentation"],
    "min_quality_score": 80
  },
  "highlight": true
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "path": "framework/agent_communication/feedback_agent.py",
        "score": 0.98,
        "highlights": [
          "Core <mark>feedback</mark> processing <mark>agent</mark> with AI-powered analysis",
          "class <mark>FeedbackAgent</mark>:",
          "def process_<mark>feedback</mark>(self, feedback_data):"
        ],
        "metadata": {
          "title": "Feedback Agent Implementation",
          "file_type": "code",
          "owner": "Claude-MCP-Research"
        },
        "assessment": {
          "quality_score": 88,
          "validation_status": "passed"
        }
      },
      {
        "path": "framework/docs/components/feedback/overview.md",
        "score": 0.92,
        "highlights": [
          "The <mark>Feedback Agent</mark> system provides intelligent analysis",
          "Comprehensive <mark>feedback</mark> processing and <mark>implementation</mark>"
        ],
        "metadata": {
          "title": "Feedback System Overview",
          "file_type": "documentation",
          "owner": "DocSystemAgent"
        },
        "assessment": {
          "quality_score": 90,
          "validation_status": "passed"
        }
      },
      {
        "path": "tests/test_feedback_agent.py",
        "score": 0.85,
        "highlights": [
          "Test suite for <mark>FeedbackAgent implementation</mark>",
          "def test_<mark>feedback</mark>_processing():"
        ],
        "metadata": {
          "title": "Feedback Agent Tests",
          "file_type": "test",
          "owner": "TestingAgent"
        },
        "assessment": {
          "quality_score": 86,
          "validation_status": "passed"
        }
      }
    ],
    "total": 8,
    "facets": {
      "file_types": {
        "code": 3,
        "documentation": 4,
        "test": 1
      },
      "tags": {
        "feedback": 8,
        "agent": 6,
        "ai": 4,
        "implementation": 3
      },
      "quality_ranges": {
        "90-100": 3,
        "80-89": 5
      }
    }
  }
}
```

## 4. Bulk Assessment Response

**Request:** `POST /api/v1/metadata/bulk`
```json
{
  "operation": "assess",
  "file_paths": [
    "framework/docs/**/*.md",
    "framework/agent_communication/*.py"
  ],
  "options": {
    "parallel": true,
    "continue_on_error": true
  }
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "operation_id": "bulk_assess_20250603_120500",
    "total_files": 32,
    "processed": 32,
    "succeeded": 30,
    "failed": 2,
    "duration_ms": 4567,
    "results": [
      {
        "path": "framework/docs/agent_onboarding.md",
        "status": "success",
        "previous_score": 93,
        "quality_score": 95,
        "improvement": 2,
        "issues_found": 0,
        "suggestions_added": 2
      },
      {
        "path": "framework/agent_communication/feedback_agent.py",
        "status": "success",
        "previous_score": 85,
        "quality_score": 88,
        "improvement": 3,
        "issues_found": 1,
        "suggestions_added": 2
      },
      {
        "path": "framework/docs/api/implementation_guide.md",
        "status": "success",
        "previous_score": 89,
        "quality_score": 93,
        "improvement": 4,
        "issues_found": 0,
        "suggestions_added": 1
      }
    ],
    "errors": [
      {
        "path": "framework/docs/temp/draft.md",
        "error": "File not found",
        "code": "FILE_NOT_FOUND"
      },
      {
        "path": "framework/agent_communication/legacy.py",
        "error": "Syntax error in file",
        "code": "VALIDATION_ERROR"
      }
    ],
    "summary": {
      "total_improvement": 67,
      "average_improvement": 2.2,
      "files_improved": 24,
      "files_declined": 2,
      "files_unchanged": 4
    }
  }
}
```

## 5. Quality Trends Response

**Request:** `GET /api/v1/metadata/trends?period=30d&metrics=quality_score,test_coverage`

**Response:**
```json
{
  "status": "success",
  "data": {
    "period": "30d",
    "start_date": "2025-05-04T00:00:00Z",
    "end_date": "2025-06-03T23:59:59Z",
    "trends": {
      "quality_score": {
        "current": 87.3,
        "previous": 82.1,
        "change": 5.2,
        "percentage_change": 6.33,
        "trend": "improving",
        "data_points": [
          {"date": "2025-05-04", "value": 82.1},
          {"date": "2025-05-05", "value": 82.3},
          {"date": "2025-05-06", "value": 82.5},
          {"date": "2025-05-10", "value": 83.2},
          {"date": "2025-05-15", "value": 84.1},
          {"date": "2025-05-20", "value": 85.0},
          {"date": "2025-05-25", "value": 85.8},
          {"date": "2025-05-30", "value": 86.5},
          {"date": "2025-06-03", "value": 87.3}
        ]
      },
      "test_coverage": {
        "current": 88.5,
        "previous": 78.2,
        "change": 10.3,
        "percentage_change": 13.17,
        "trend": "improving",
        "data_points": [
          {"date": "2025-05-04", "value": 78.2},
          {"date": "2025-05-10", "value": 80.5},
          {"date": "2025-05-15", "value": 82.0},
          {"date": "2025-05-20", "value": 84.5},
          {"date": "2025-05-25", "value": 86.0},
          {"date": "2025-05-30", "value": 87.5},
          {"date": "2025-06-03", "value": 88.5}
        ]
      },
      "file_count": {
        "current": 145,
        "previous": 132,
        "change": 13,
        "percentage_change": 9.85,
        "trend": "growing"
      }
    },
    "top_improvements": [
      {
        "file": "framework/agent_communication/feedback_agent.py",
        "improvement": 15,
        "from": 73,
        "to": 88,
        "primary_reason": "increased_test_coverage"
      },
      {
        "file": "framework/docs/agent_onboarding.md",
        "improvement": 12,
        "from": 83,
        "to": 95,
        "primary_reason": "content_completeness"
      },
      {
        "file": "framework/validators/validator.py",
        "improvement": 10,
        "from": 80,
        "to": 90,
        "primary_reason": "code_refactoring"
      }
    ],
    "top_declines": [
      {
        "file": "framework/legacy/old_protocol.py",
        "decline": -8,
        "from": 75,
        "to": 67,
        "primary_reason": "deprecation_warnings"
      }
    ],
    "insights": {
      "positive_trends": [
        "Test coverage increased by 13.17% in the last 30 days",
        "Documentation quality improved consistently",
        "Code complexity reduced in core modules"
      ],
      "areas_of_concern": [
        "Legacy code quality declining due to deprecation",
        "Some test files lack proper documentation"
      ],
      "recommendations": [
        {
          "priority": "high",
          "action": "Migrate legacy code to new protocol",
          "impact": "Prevent further quality degradation"
        },
        {
          "priority": "medium",
          "action": "Add documentation to test files",
          "impact": "Improve overall documentation coverage"
        }
      ]
    }
  }
}
```

## 6. WebSocket Event Examples

### File Updated Event
```json
{
  "event": "file_updated",
  "timestamp": "2025-06-03T14:30:00Z",
  "data": {
    "path": "framework/agent_communication/feedback_agent.py",
    "changes": ["content", "metadata"],
    "quality_score": 90,
    "previous_quality_score": 88,
    "delta": {
      "quality_score": 2,
      "metrics": {
        "test_coverage": 3.5,
        "documentation_coverage": 2.0
      }
    },
    "updated_by": "Claude-MCP-Research",
    "commit_hash": "a1b2c3d4",
    "commit_message": "refactor: optimize feedback processing performance"
  }
}
```

### Quality Changed Event
```json
{
  "event": "quality_changed",
  "timestamp": "2025-06-03T14:31:00Z",
  "data": {
    "path": "framework/docs/api/enhanced_metadata_api.md",
    "previous_score": 89,
    "new_score": 95,
    "change": 6,
    "reason": "content_improvement",
    "metrics_changed": {
      "completeness": {
        "before": 88,
        "after": 98
      },
      "clarity": {
        "before": 85,
        "after": 92
      }
    },
    "triggered_by": "manual_edit",
    "threshold_alerts": [
      {
        "type": "quality_improved",
        "message": "File quality exceeded 95 threshold"
      }
    ]
  }
}
```

### Assessment Complete Event
```json
{
  "event": "assessment_complete",
  "timestamp": "2025-06-03T14:32:00Z",
  "data": {
    "assessment_id": "assess_20250603_143200",
    "type": "scheduled",
    "file_count": 25,
    "duration_ms": 3456,
    "summary": {
      "improved": 18,
      "declined": 2,
      "unchanged": 5,
      "total_quality_change": 45,
      "average_quality_change": 1.8
    },
    "notable_changes": [
      {
        "file": "framework/core.py",
        "change": 8,
        "reason": "test_coverage_increase"
      },
      {
        "file": "framework/docs/guide.md",
        "change": -3,
        "reason": "broken_links_detected"
      }
    ],
    "next_assessment": "2025-06-03T15:32:00Z"
  }
}
```

### Feedback Added Event
```json
{
  "event": "feedback_added",
  "timestamp": "2025-06-03T14:33:00Z",
  "data": {
    "path": "framework/docs/components/feedback/overview.md",
    "feedback_type": "improvement_suggestion",
    "agent": "UI-Integration-Agent",
    "content": {
      "suggestion": "Add interactive examples showing real-time feedback processing",
      "effort": "medium",
      "impact": 35,
      "priority": "high",
      "category": "usability"
    },
    "context": {
      "current_quality_score": 90,
      "related_files": [
        "framework/agent_communication/feedback_agent.py"
      ],
      "user_session": "ui_dashboard_123"
    }
  }
}
```

### Critical Issue Detected Event
```json
{
  "event": "critical_issue_detected",
  "timestamp": "2025-06-03T14:35:00Z",
  "data": {
    "path": "framework/agent_communication/core/models.py",
    "issue": {
      "type": "security",
      "severity": "critical",
      "description": "Potential SQL injection vulnerability in query builder",
      "line_numbers": [234, 256],
      "suggested_fix": "Use parameterized queries instead of string concatenation",
      "cve_reference": null
    },
    "automatic_actions": [
      {
        "action": "notify_owner",
        "status": "completed"
      },
      {
        "action": "create_issue",
        "status": "completed",
        "issue_id": "SEC-2025-001"
      }
    ],
    "requires_immediate_attention": true
  }
}
```

## 7. Error Response Examples

### File Not Found
```json
{
  "status": "error",
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "The requested file does not exist",
    "details": {
      "path": "framework/docs/missing.md",
      "suggestion": "Did you mean 'framework/docs/api/missing.md'?"
    }
  }
}
```

### Validation Error
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Metadata validation failed",
    "details": {
      "field": "metadata.tags",
      "constraint": "array_max_length",
      "provided": 25,
      "maximum": 20,
      "suggestion": "Reduce the number of tags to 20 or less"
    }
  }
}
```

### Rate Limited
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMITED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 100,
      "window": "1m",
      "retry_after": 45,
      "upgrade_url": "https://api.example.com/pricing"
    }
  },
  "headers": {
    "X-RateLimit-Limit": "100",
    "X-RateLimit-Remaining": "0",
    "X-RateLimit-Reset": "1685808045"
  }
}
```

## Usage Notes for UI Integration

1. **Response Caching**: All successful responses include an ETag header for caching
2. **Partial Responses**: Large metadata objects can be requested with field selection using `?fields=metadata,assessment`
3. **Streaming**: For bulk operations, responses can be streamed using `Accept: application/x-ndjson`
4. **Compression**: All responses support gzip compression with `Accept-Encoding: gzip`
5. **Localization**: Dates are in UTC ISO 8601 format; convert to user timezone in UI

These sample responses represent real-world data that the UI agent will receive when integrating with the enhanced metadata system.