# Enhanced Metadata API Specification

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "DocSystemAgent"
  title: "Enhanced Metadata API Specification"
  description: "Complete API specification for integrating with the enhanced metadata system"
content:
  overview: "The Enhanced Metadata API provides comprehensive document and code analysis with real-time updates, quality scoring, and intelligent feedback integration."
  key_components: "REST Endpoints, WebSocket Events, Bulk Operations, Quality Tracking"
  sections:
    - title: "Overview"
      content: "API designed to power modern documentation dashboards with rich insights"
    - title: "Core Endpoints"
      content: "File metadata retrieval, search, updates, and assessments"
    - title: "WebSocket Events"
      content: "Real-time updates for file changes and quality metrics"
    - title: "Error Handling"
      content: "Consistent error responses and rate limiting"
    - title: "Best Practices"
      content: "Caching, pagination, and batch operations"
  changelog:
    - version: "1.0.0"
      date: "2025-06-03"
      changes:
        - "Initial release with enhanced metadata support"
        - "Complete REST API with 7 core endpoints"
        - "WebSocket support for real-time updates"
        - "Comprehensive error handling and rate limiting"
feedback:
  rating: 95
  comments: "Comprehensive API specification with excellent examples and clear documentation"
  observations:
    - what: "Complete endpoint documentation with request/response examples"
      impact: "Easy integration for UI developers"
      priority: "low"
      category: "quality"
    - what: "WebSocket event specifications included"
      impact: "Enables real-time dashboard updates"
      priority: "low"
      category: "quality"
  suggestions:
    - action: "Add SDK examples in multiple languages"
      priority: "medium"
      effort: "medium"
      impact: "high"
      assignee: "api_team"
    - action: "Include postman collection for testing"
      priority: "low"
      effort: "small"
      impact: "medium"
      assignee: "documentation_team"
  status:
    value: "approved"
    updated_by: "DocSystemAgent"
    date: "2025-06-03"
    validation: "passed"
    implementation: "complete"
```

## Overview

The Enhanced Metadata API provides comprehensive document and code analysis with real-time updates, quality scoring, and intelligent feedback integration. This API is designed to power modern documentation dashboards with rich insights and actionable intelligence.

## Base URL

```
http://localhost:8080/api/v1
```

## Authentication

All API requests require an API key in the header:

```http
X-API-Key: your-api-key-here
```

## Core Endpoints

### 1. Get File Metadata

Retrieve enhanced metadata for a specific file.

**Endpoint:** `GET /metadata/{file_path}`

**Parameters:**
- `file_path` (string, required): Relative path to the file

**Response:**
```json
{
  "status": "success",
  "data": {
    "metadata": {
      "schema": "https://schema.org/TechnicalDocument",
      "version": "1.2.3",
      "status": "Active",
      "owner": "DocSystemAgent",
      "title": "Enhanced Agent Communication Protocol",
      "description": "Comprehensive documentation system with AI feedback integration",
      "file_type": "documentation",
      "tags": ["protocol", "agent-communication", "ai-feedback"],
      "dependencies": [
        {
          "file": "framework/schemas/document_protocol.yml",
          "type": "required"
        }
      ]
    },
    "assessment": {
      "quality_score": 92,
      "validation_status": "passed",
      "validation_errors": [],
      "last_assessed": "2025-06-03T01:15:30Z",
      "assessed_by": "DocSystemAgent",
      "improvement_velocity": {
        "last_7_days": 8,
        "last_30_days": 15,
        "trend": "improving"
      },
      "metrics": {
        "completeness": 95,
        "accuracy": 90,
        "clarity": 88,
        "consistency": 94,
        "usability": 89
      },
      "code_metrics": {
        "complexity_score": 75,
        "test_coverage": 88.5,
        "documentation_coverage": 92.0,
        "maintainability_index": 82,
        "lines_of_code": 450,
        "cyclomatic_complexity": 12
      },
      "priority": {
        "business_value": "critical",
        "technical_priority": "high",
        "urgency": "medium"
      }
    },
    "system": {
      "created_at": "2025-06-01T10:30:00Z",
      "modified_at": "2025-06-03T01:10:00Z",
      "file_size": 15672,
      "file_hash": "sha256:a1b2c3d4e5f6...",
      "git_info": {
        "last_commit": "feat: add enhanced metadata schema",
        "last_author": "DocSystemAgent",
        "commit_count": 23,
        "branch": "feature/enhanced-metadata"
      },
      "agent_activity": {
        "last_reviewed_by": "DocSystemAgent",
        "review_count": 5,
        "collaborators": ["DocSystemAgent", "Claude-MCP-Research"]
      },
      "automation": {
        "auto_assess": true,
        "assessment_frequency": "on_change",
        "alerts_enabled": true,
        "quality_threshold": 85
      }
    },
    "relationships": {
      "parent_docs": ["framework/docs/agent_onboarding.md"],
      "child_docs": [],
      "related_files": [
        {
          "file": "framework/agent_communication/feedback_agent.py",
          "relationship": "implements"
        }
      ],
      "external_links": [
        {
          "url": "https://schema.org/TechnicalDocument",
          "type": "api",
          "status": "active"
        }
      ]
    },
    "feedback": {
      "current_issues": [],
      "improvement_suggestions": [
        {
          "suggestion": "Add more code examples for API integration",
          "effort": "small",
          "impact": 15,
          "priority": "medium"
        }
      ],
      "agent_notes": [
        {
          "agent": "DocSystemAgent",
          "note": "Comprehensive protocol documentation with excellent validation",
          "timestamp": "2025-06-03T01:15:30Z"
        }
      ]
    }
  }
}
```

### 2. List All Files with Metadata

Get a paginated list of all files with their metadata.

**Endpoint:** `GET /metadata`

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 20, max: 100)
- `file_type` (string, optional): Filter by file type
- `quality_threshold` (integer, optional): Minimum quality score
- `status` (string, optional): Filter by status
- `sort_by` (string, optional): Sort field (quality_score, modified_at, file_size)
- `order` (string, optional): Sort order (asc, desc)

**Response:**
```json
{
  "status": "success",
  "data": {
    "files": [
      {
        "path": "framework/docs/agent_onboarding.md",
        "metadata": { /* Full metadata object */ },
        "assessment": { /* Full assessment object */ }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 145,
      "pages": 8
    },
    "summary": {
      "total_files": 145,
      "average_quality": 87.3,
      "files_by_type": {
        "documentation": 45,
        "code": 78,
        "config": 12,
        "test": 10
      },
      "validation_status": {
        "passed": 132,
        "failed": 8,
        "warning": 5
      }
    }
  }
}
```

### 3. Search Files

Search for files using various criteria.

**Endpoint:** `POST /metadata/search`

**Request Body:**
```json
{
  "query": "agent communication",
  "filters": {
    "file_types": ["documentation", "code"],
    "min_quality_score": 80,
    "status": ["Active", "Draft"],
    "tags": ["protocol"],
    "modified_after": "2025-06-01T00:00:00Z"
  },
  "include_content": false,
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
        "path": "framework/agent_communication/core.py",
        "score": 0.95,
        "highlights": [
          "Enhanced <mark>agent communication</mark> protocol"
        ],
        "metadata": { /* Metadata object */ }
      }
    ],
    "total": 12,
    "facets": {
      "file_types": {
        "documentation": 5,
        "code": 7
      },
      "tags": {
        "protocol": 8,
        "agent-communication": 12
      }
    }
  }
}
```

### 4. Update File Metadata

Update metadata for a specific file.

**Endpoint:** `PATCH /metadata/{file_path}`

**Request Body:**
```json
{
  "metadata": {
    "tags": ["updated", "reviewed"],
    "owner": "NewOwner"
  },
  "feedback": {
    "agent_notes": [
      {
        "agent": "UIAgent",
        "note": "Updated based on user feedback",
        "timestamp": "2025-06-03T14:00:00Z"
      }
    ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "path": "framework/docs/api.md",
    "updated_fields": ["metadata.tags", "metadata.owner", "feedback.agent_notes"],
    "new_quality_score": 94,
    "validation_status": "passed"
  }
}
```

### 5. Trigger Assessment

Manually trigger a quality assessment for a file.

**Endpoint:** `POST /metadata/{file_path}/assess`

**Request Body:**
```json
{
  "assessment_type": "full",
  "include_dependencies": true,
  "custom_rules": []
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "assessment_id": "assess_12345",
    "status": "completed",
    "duration_ms": 245,
    "previous_score": 88,
    "new_score": 92,
    "improvements": [
      {
        "metric": "completeness",
        "before": 85,
        "after": 95,
        "change": 10
      }
    ],
    "recommendations": [
      {
        "type": "documentation",
        "priority": "medium",
        "suggestion": "Add usage examples for complex functions"
      }
    ]
  }
}
```

### 6. Bulk Operations

Perform operations on multiple files.

**Endpoint:** `POST /metadata/bulk`

**Request Body:**
```json
{
  "operation": "assess",
  "file_paths": [
    "framework/docs/*.md",
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
    "operation_id": "bulk_67890",
    "total_files": 25,
    "processed": 25,
    "succeeded": 23,
    "failed": 2,
    "results": [
      {
        "path": "framework/docs/api.md",
        "status": "success",
        "quality_score": 94
      }
    ],
    "errors": [
      {
        "path": "framework/docs/broken.md",
        "error": "File not found"
      }
    ]
  }
}
```

### 7. Get Quality Trends

Retrieve quality trends over time.

**Endpoint:** `GET /metadata/trends`

**Query Parameters:**
- `period` (string): Time period (7d, 30d, 90d, 1y)
- `file_type` (string, optional): Filter by file type
- `metrics` (array, optional): Specific metrics to include

**Response:**
```json
{
  "status": "success",
  "data": {
    "period": "30d",
    "trends": {
      "quality_score": {
        "current": 87.3,
        "previous": 82.1,
        "change": 5.2,
        "trend": "improving",
        "data_points": [
          {
            "date": "2025-05-04",
            "value": 82.1
          }
        ]
      },
      "file_count": {
        "current": 145,
        "previous": 132,
        "change": 13,
        "trend": "growing"
      },
      "coverage": {
        "test_coverage": 88.5,
        "documentation_coverage": 92.0
      }
    },
    "top_improvements": [
      {
        "file": "framework/core.py",
        "improvement": 15,
        "from": 75,
        "to": 90
      }
    ]
  }
}
```

## WebSocket Events

Connect to receive real-time updates.

**WebSocket URL:** `ws://localhost:8080/ws`

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = () => {
  // Subscribe to events
  ws.send(JSON.stringify({
    type: 'subscribe',
    events: ['file_updated', 'quality_changed', 'assessment_complete']
  }));
};
```

### Event Types

#### 1. File Updated
```json
{
  "event": "file_updated",
  "timestamp": "2025-06-03T14:30:00Z",
  "data": {
    "path": "framework/docs/api.md",
    "changes": ["content", "metadata"],
    "quality_score": 94,
    "delta": {
      "quality_score": 2,
      "metrics": {
        "completeness": 5
      }
    }
  }
}
```

#### 2. Quality Changed
```json
{
  "event": "quality_changed",
  "timestamp": "2025-06-03T14:31:00Z",
  "data": {
    "path": "framework/core.py",
    "previous_score": 85,
    "new_score": 92,
    "reason": "test_coverage_improved",
    "metrics_changed": {
      "test_coverage": {
        "before": 75.0,
        "after": 88.5
      }
    }
  }
}
```

#### 3. Assessment Complete
```json
{
  "event": "assessment_complete",
  "timestamp": "2025-06-03T14:32:00Z",
  "data": {
    "assessment_id": "assess_12345",
    "file_count": 10,
    "duration_ms": 1234,
    "summary": {
      "improved": 7,
      "declined": 1,
      "unchanged": 2
    }
  }
}
```

#### 4. Feedback Added
```json
{
  "event": "feedback_added",
  "timestamp": "2025-06-03T14:33:00Z",
  "data": {
    "path": "framework/docs/guide.md",
    "feedback_type": "improvement_suggestion",
    "agent": "UIAgent",
    "content": {
      "suggestion": "Add interactive examples",
      "priority": "high",
      "impact": 25
    }
  }
}
```

## Error Handling

All endpoints follow consistent error response format:

```json
{
  "status": "error",
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "The requested file does not exist",
    "details": {
      "path": "framework/missing.md"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `FILE_NOT_FOUND` | 404 | Requested file doesn't exist |
| `INVALID_REQUEST` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `RATE_LIMITED` | 429 | Too many requests |
| `ASSESSMENT_FAILED` | 500 | Assessment process failed |
| `VALIDATION_ERROR` | 422 | Metadata validation failed |

## Rate Limiting

- **Default limit:** 100 requests per minute
- **Burst limit:** 20 requests per second
- **WebSocket connections:** 5 concurrent per API key

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1685808000
```

## Best Practices

1. **Caching**: Cache metadata responses with ETags
2. **Pagination**: Use pagination for large file lists
3. **WebSocket**: Use WebSocket for real-time updates instead of polling
4. **Batch Operations**: Use bulk endpoints for multiple files
5. **Error Handling**: Implement exponential backoff for retries

## Version History

- **v1.0.0** (2025-06-03): Initial release with enhanced metadata support