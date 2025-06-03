# Enhanced Metadata API Implementation Guide

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "1.0.0"
  status: "Active"
  owner: "DocSystemAgent"
  title: "Enhanced Metadata API Implementation Guide"
  description: "Step-by-step guide for integrating with the enhanced metadata system"
content:
  overview: "This guide provides practical implementation examples and best practices for integrating with the Enhanced Metadata API."
  key_components: "Quick Start, Authentication, Client Libraries, Code Examples, Integration Patterns"
  sections:
    - title: "Quick Start"
      content: "Get up and running with the API in minutes"
    - title: "Prerequisites"
      content: "Required tools and dependencies"
    - title: "Installation"
      content: "Installing client libraries for various platforms"
    - title: "Authentication"
      content: "Setting up API key authentication"
    - title: "Basic Usage"
      content: "Common operations and code examples"
    - title: "Advanced Features"
      content: "WebSocket integration and bulk operations"
    - title: "Dashboard Integration"
      content: "Building UI components with the API"
  changelog:
    - version: "1.0.0"
      date: "2025-06-03"
      changes:
        - "Initial implementation guide"
        - "JavaScript/TypeScript and Python examples"
        - "React component examples"
        - "WebSocket integration patterns"
feedback:
  rating: 93
  comments: "Excellent implementation guide with practical examples and clear explanations"
  observations:
    - what: "Comprehensive code examples in multiple languages"
      impact: "Reduces integration time for developers"
      priority: "low"
      category: "usability"
    - what: "React component examples included"
      impact: "Direct help for UI developers"
      priority: "low"
      category: "quality"
  suggestions:
    - action: "Add Vue.js and Angular examples"
      priority: "medium"
      effort: "medium"
      impact: "medium"
      assignee: "frontend_team"
    - action: "Include troubleshooting section"
      priority: "high"
      effort: "small"
      impact: "high"
      assignee: "documentation_team"
  status:
    value: "approved"
    updated_by: "DocSystemAgent"
    date: "2025-06-03"
    validation: "passed"
    implementation: "complete"
```

## Quick Start

This guide will help you integrate with the Enhanced Metadata API to build rich documentation dashboards and intelligent code analysis tools.

## Prerequisites

- Node.js 18+ or Python 3.9+
- API key for authentication
- WebSocket support for real-time updates

## Installation

### JavaScript/TypeScript

```bash
npm install @agent-doc-system/metadata-client
# or
yarn add @agent-doc-system/metadata-client
```

### Python

```bash
pip install agent-doc-metadata
```

## Basic Integration

### 1. Initialize the Client

#### JavaScript/TypeScript

```typescript
import { MetadataClient } from '@agent-doc-system/metadata-client';

const client = new MetadataClient({
  baseUrl: 'http://localhost:8080/api/v1',
  apiKey: 'your-api-key-here',
  timeout: 30000, // 30 seconds
  retryOptions: {
    maxRetries: 3,
    backoffMultiplier: 2
  }
});
```

#### Python

```python
from agent_doc_metadata import MetadataClient

client = MetadataClient(
    base_url='http://localhost:8080/api/v1',
    api_key='your-api-key-here',
    timeout=30,
    max_retries=3
)
```

### 2. Fetch File Metadata

#### JavaScript/TypeScript

```typescript
async function getFileMetadata(filePath: string) {
  try {
    const metadata = await client.getMetadata(filePath);
    
    console.log(`File: ${filePath}`);
    console.log(`Quality Score: ${metadata.assessment.quality_score}`);
    console.log(`Status: ${metadata.metadata.status}`);
    
    // Check if file needs attention
    if (metadata.assessment.quality_score < 70) {
      console.warn('File needs improvement!');
      metadata.feedback.improvement_suggestions.forEach(suggestion => {
        console.log(`- ${suggestion.suggestion} (Impact: ${suggestion.impact})`);
      });
    }
    
    return metadata;
  } catch (error) {
    console.error(`Failed to fetch metadata: ${error.message}`);
  }
}

// Usage
const metadata = await getFileMetadata('framework/docs/api.md');
```

#### Python

```python
async def get_file_metadata(file_path: str):
    try:
        metadata = await client.get_metadata(file_path)
        
        print(f"File: {file_path}")
        print(f"Quality Score: {metadata['assessment']['quality_score']}")
        print(f"Status: {metadata['metadata']['status']}")
        
        # Check if file needs attention
        if metadata['assessment']['quality_score'] < 70:
            print("File needs improvement!")
            for suggestion in metadata['feedback']['improvement_suggestions']:
                print(f"- {suggestion['suggestion']} (Impact: {suggestion['impact']})")
        
        return metadata
    except Exception as e:
        print(f"Failed to fetch metadata: {str(e)}")

# Usage
metadata = await get_file_metadata('framework/docs/api.md')
```

### 3. List and Filter Files

#### JavaScript/TypeScript

```typescript
interface FileFilter {
  fileType?: string[];
  minQualityScore?: number;
  status?: string[];
  modifiedAfter?: Date;
}

async function listFiles(filter: FileFilter) {
  const response = await client.listMetadata({
    file_type: filter.fileType?.join(','),
    quality_threshold: filter.minQualityScore,
    status: filter.status?.join(','),
    sort_by: 'quality_score',
    order: 'desc',
    per_page: 50
  });
  
  // Process results
  const criticalFiles = response.data.files.filter(file => 
    file.assessment.priority.business_value === 'critical'
  );
  
  console.log(`Total files: ${response.data.summary.total_files}`);
  console.log(`Average quality: ${response.data.summary.average_quality}`);
  console.log(`Critical files: ${criticalFiles.length}`);
  
  return response.data.files;
}

// Usage: Get all documentation files with quality > 80
const highQualityDocs = await listFiles({
  fileType: ['documentation'],
  minQualityScore: 80,
  status: ['Active']
});
```

#### Python

```python
from typing import List, Optional, Dict
from datetime import datetime

async def list_files(
    file_types: Optional[List[str]] = None,
    min_quality_score: Optional[int] = None,
    status: Optional[List[str]] = None,
    modified_after: Optional[datetime] = None
) -> List[Dict]:
    response = await client.list_metadata(
        file_type=','.join(file_types) if file_types else None,
        quality_threshold=min_quality_score,
        status=','.join(status) if status else None,
        sort_by='quality_score',
        order='desc',
        per_page=50
    )
    
    # Process results
    critical_files = [
        file for file in response['data']['files']
        if file['assessment']['priority']['business_value'] == 'critical'
    ]
    
    print(f"Total files: {response['data']['summary']['total_files']}")
    print(f"Average quality: {response['data']['summary']['average_quality']}")
    print(f"Critical files: {len(critical_files)}")
    
    return response['data']['files']

# Usage
high_quality_docs = await list_files(
    file_types=['documentation'],
    min_quality_score=80,
    status=['Active']
)
```

### 4. Real-time Updates with WebSocket

#### JavaScript/TypeScript

```typescript
class MetadataWebSocket {
  private ws: WebSocket;
  private reconnectAttempts = 0;
  private maxReconnects = 5;
  
  constructor(private apiKey: string) {
    this.connect();
  }
  
  private connect() {
    this.ws = new WebSocket('ws://localhost:8080/ws');
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      
      // Authenticate
      this.ws.send(JSON.stringify({
        type: 'auth',
        apiKey: this.apiKey
      }));
      
      // Subscribe to events
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        events: ['file_updated', 'quality_changed', 'assessment_complete']
      }));
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleEvent(data);
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.attemptReconnect();
    };
  }
  
  private handleEvent(event: any) {
    switch (event.event) {
      case 'file_updated':
        console.log(`File updated: ${event.data.path}`);
        console.log(`New quality score: ${event.data.quality_score}`);
        // Update UI
        this.updateFileInUI(event.data);
        break;
        
      case 'quality_changed':
        console.log(`Quality changed for ${event.data.path}`);
        console.log(`${event.data.previous_score} → ${event.data.new_score}`);
        // Show notification
        this.showQualityNotification(event.data);
        break;
        
      case 'assessment_complete':
        console.log(`Assessment complete: ${event.data.assessment_id}`);
        console.log(`Files improved: ${event.data.summary.improved}`);
        // Refresh dashboard
        this.refreshDashboard();
        break;
    }
  }
  
  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnects) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(`Reconnecting in ${delay}ms...`);
      setTimeout(() => this.connect(), delay);
    }
  }
  
  private updateFileInUI(data: any) {
    // Implement UI update logic
  }
  
  private showQualityNotification(data: any) {
    // Implement notification logic
  }
  
  private refreshDashboard() {
    // Implement dashboard refresh logic
  }
}

// Usage
const metadataWS = new MetadataWebSocket('your-api-key');
```

#### Python

```python
import asyncio
import json
import websockets
from typing import Callable, Dict, Any

class MetadataWebSocket:
    def __init__(self, api_key: str, event_handlers: Dict[str, Callable]):
        self.api_key = api_key
        self.event_handlers = event_handlers
        self.reconnect_attempts = 0
        self.max_reconnects = 5
        
    async def connect(self):
        uri = "ws://localhost:8080/ws"
        
        while self.reconnect_attempts < self.max_reconnects:
            try:
                async with websockets.connect(uri) as websocket:
                    await self.authenticate(websocket)
                    await self.subscribe(websocket)
                    await self.listen(websocket)
                    
            except Exception as e:
                print(f"WebSocket error: {e}")
                self.reconnect_attempts += 1
                delay = min(2 ** self.reconnect_attempts, 30)
                print(f"Reconnecting in {delay} seconds...")
                await asyncio.sleep(delay)
    
    async def authenticate(self, websocket):
        await websocket.send(json.dumps({
            "type": "auth",
            "apiKey": self.api_key
        }))
    
    async def subscribe(self, websocket):
        await websocket.send(json.dumps({
            "type": "subscribe",
            "events": ["file_updated", "quality_changed", "assessment_complete"]
        }))
    
    async def listen(self, websocket):
        async for message in websocket:
            event = json.loads(message)
            await self.handle_event(event)
    
    async def handle_event(self, event: Dict[str, Any]):
        event_type = event.get("event")
        if event_type in self.event_handlers:
            await self.event_handlers[event_type](event["data"])

# Usage
async def on_file_updated(data):
    print(f"File updated: {data['path']}")
    print(f"New quality score: {data['quality_score']}")

async def on_quality_changed(data):
    print(f"Quality changed for {data['path']}")
    print(f"{data['previous_score']} → {data['new_score']}")

async def on_assessment_complete(data):
    print(f"Assessment complete: {data['assessment_id']}")
    print(f"Files improved: {data['summary']['improved']}")

event_handlers = {
    "file_updated": on_file_updated,
    "quality_changed": on_quality_changed,
    "assessment_complete": on_assessment_complete
}

ws_client = MetadataWebSocket("your-api-key", event_handlers)
await ws_client.connect()
```

## Advanced Features

### 1. Batch Processing

Process multiple files efficiently:

```typescript
async function assessMultipleFiles(patterns: string[]) {
  const response = await client.bulkOperation({
    operation: 'assess',
    file_paths: patterns,
    options: {
      parallel: true,
      continue_on_error: true
    }
  });
  
  console.log(`Processed ${response.data.processed} files`);
  console.log(`Success rate: ${(response.data.succeeded / response.data.total_files * 100).toFixed(1)}%`);
  
  // Handle errors
  response.data.errors.forEach(error => {
    console.error(`Failed to process ${error.path}: ${error.error}`);
  });
  
  return response.data.results;
}

// Assess all documentation and code files
const results = await assessMultipleFiles([
  'framework/docs/**/*.md',
  'framework/**/*.py'
]);
```

### 2. Quality Trends Analysis

Track quality improvements over time:

```typescript
async function analyzeQualityTrends(period: string = '30d') {
  const trends = await client.getQualityTrends({
    period,
    metrics: ['quality_score', 'test_coverage', 'documentation_coverage']
  });
  
  // Calculate improvement rate
  const qualityTrend = trends.data.trends.quality_score;
  const improvementRate = 
    ((qualityTrend.current - qualityTrend.previous) / qualityTrend.previous) * 100;
  
  console.log(`Quality improvement: ${improvementRate.toFixed(1)}%`);
  
  // Find files with biggest improvements
  trends.data.top_improvements.forEach(file => {
    console.log(`${file.file}: +${file.improvement} points`);
  });
  
  return trends.data;
}
```

### 3. Custom Assessment Rules

Add custom validation rules:

```typescript
interface CustomRule {
  name: string;
  description: string;
  check: (metadata: any) => boolean;
  severity: 'error' | 'warning' | 'info';
  impact: number;
}

const customRules: CustomRule[] = [
  {
    name: 'require-examples',
    description: 'Documentation must include code examples',
    check: (metadata) => {
      if (metadata.metadata.file_type !== 'documentation') return true;
      const content = metadata._content || '';
      return content.includes('```') || content.includes('Example:');
    },
    severity: 'warning',
    impact: 10
  },
  {
    name: 'max-complexity',
    description: 'Code complexity must be below threshold',
    check: (metadata) => {
      if (!metadata.assessment.code_metrics) return true;
      return metadata.assessment.code_metrics.cyclomatic_complexity < 15;
    },
    severity: 'error',
    impact: 20
  }
];

async function assessWithCustomRules(filePath: string) {
  const response = await client.assessFile(filePath, {
    assessment_type: 'full',
    custom_rules: customRules
  });
  
  return response.data;
}
```

### 4. Dashboard Integration

Build a comprehensive dashboard:

```typescript
class MetadataDashboard {
  private updateInterval: number = 60000; // 1 minute
  private updateTimer: NodeJS.Timer;
  
  constructor(private client: MetadataClient) {
    this.startAutoUpdate();
  }
  
  async getDashboardData() {
    const [files, trends, recentActivity] = await Promise.all([
      this.client.listMetadata({ per_page: 100 }),
      this.client.getQualityTrends({ period: '7d' }),
      this.client.getRecentActivity({ limit: 20 })
    ]);
    
    return {
      summary: {
        totalFiles: files.data.summary.total_files,
        averageQuality: files.data.summary.average_quality,
        filesNeedingAttention: files.data.files.filter(f => 
          f.assessment.quality_score < 70
        ).length,
        trend: trends.data.trends.quality_score.trend
      },
      filesByType: files.data.summary.files_by_type,
      validationStatus: files.data.summary.validation_status,
      recentChanges: recentActivity.data.activities,
      topIssues: this.extractTopIssues(files.data.files),
      improvementVelocity: this.calculateVelocity(files.data.files)
    };
  }
  
  private extractTopIssues(files: any[]) {
    const issues = [];
    
    files.forEach(file => {
      file.feedback.current_issues.forEach(issue => {
        issues.push({
          file: file.path,
          ...issue
        });
      });
    });
    
    return issues
      .sort((a, b) => {
        const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return severityOrder[a.severity] - severityOrder[b.severity];
      })
      .slice(0, 10);
  }
  
  private calculateVelocity(files: any[]) {
    const velocities = files
      .filter(f => f.assessment.improvement_velocity)
      .map(f => f.assessment.improvement_velocity.last_7_days);
    
    return velocities.length > 0
      ? velocities.reduce((a, b) => a + b, 0) / velocities.length
      : 0;
  }
  
  private startAutoUpdate() {
    this.updateTimer = setInterval(async () => {
      const data = await this.getDashboardData();
      this.updateUI(data);
    }, this.updateInterval);
  }
  
  private updateUI(data: any) {
    // Implement UI update logic
    console.log('Dashboard updated:', data);
  }
  
  destroy() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
    }
  }
}

// Usage
const dashboard = new MetadataDashboard(client);
const dashboardData = await dashboard.getDashboardData();
```

## Error Handling Best Practices

### 1. Comprehensive Error Handling

```typescript
class MetadataError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = 'MetadataError';
  }
}

async function safeMetadataOperation<T>(
  operation: () => Promise<T>,
  fallback?: T
): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    if (error instanceof MetadataError) {
      switch (error.code) {
        case 'FILE_NOT_FOUND':
          console.warn(`File not found: ${error.details?.path}`);
          break;
        case 'RATE_LIMITED':
          console.warn('Rate limited, waiting before retry...');
          await new Promise(resolve => setTimeout(resolve, 5000));
          return safeMetadataOperation(operation, fallback);
        case 'VALIDATION_ERROR':
          console.error('Validation failed:', error.details);
          break;
        default:
          console.error(`API Error: ${error.message}`);
      }
    } else {
      console.error('Unexpected error:', error);
    }
    
    if (fallback !== undefined) {
      return fallback;
    }
    throw error;
  }
}

// Usage
const metadata = await safeMetadataOperation(
  () => client.getMetadata('framework/docs/api.md'),
  { /* default metadata object */ }
);
```

### 2. Retry with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      if (attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Retry attempt ${attempt + 1} after ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
}

// Usage
const result = await retryWithBackoff(() => 
  client.assessFile('framework/core.py')
);
```

## Performance Optimization

### 1. Response Caching

```typescript
class CachedMetadataClient {
  private cache = new Map<string, { data: any; etag: string; expires: number }>();
  private cacheTime = 300000; // 5 minutes
  
  constructor(private client: MetadataClient) {}
  
  async getMetadata(filePath: string, forceRefresh = false) {
    const cached = this.cache.get(filePath);
    
    if (!forceRefresh && cached && cached.expires > Date.now()) {
      return cached.data;
    }
    
    const response = await this.client.getMetadataWithHeaders(filePath, {
      'If-None-Match': cached?.etag
    });
    
    if (response.status === 304 && cached) {
      // Not modified, extend cache
      cached.expires = Date.now() + this.cacheTime;
      return cached.data;
    }
    
    // Update cache
    this.cache.set(filePath, {
      data: response.data,
      etag: response.headers.etag,
      expires: Date.now() + this.cacheTime
    });
    
    return response.data;
  }
  
  clearCache(filePath?: string) {
    if (filePath) {
      this.cache.delete(filePath);
    } else {
      this.cache.clear();
    }
  }
}
```

### 2. Batch Requests

```typescript
class BatchedMetadataClient {
  private batchQueue: Map<string, Promise<any>> = new Map();
  private batchTimer: NodeJS.Timer;
  private batchDelay = 50; // ms
  
  constructor(private client: MetadataClient) {}
  
  async getMetadata(filePath: string): Promise<any> {
    // Check if already in batch
    const existing = this.batchQueue.get(filePath);
    if (existing) return existing;
    
    // Create promise for this request
    const promise = new Promise((resolve, reject) => {
      // Add to batch
      this.addToBatch(filePath, resolve, reject);
    });
    
    this.batchQueue.set(filePath, promise);
    return promise;
  }
  
  private addToBatch(filePath: string, resolve: Function, reject: Function) {
    if (!this.batchTimer) {
      this.batchTimer = setTimeout(() => this.processBatch(), this.batchDelay);
    }
  }
  
  private async processBatch() {
    const paths = Array.from(this.batchQueue.keys());
    this.batchQueue.clear();
    this.batchTimer = null;
    
    try {
      // Fetch all at once
      const results = await this.client.bulkGetMetadata(paths);
      
      // Resolve individual promises
      results.forEach(result => {
        const promise = this.batchQueue.get(result.path);
        if (promise) {
          promise.resolve(result.metadata);
        }
      });
    } catch (error) {
      // Reject all promises
      this.batchQueue.forEach(promise => {
        promise.reject(error);
      });
    }
  }
}
```

## Security Considerations

### 1. API Key Management

```typescript
// Never hardcode API keys
const apiKey = process.env.METADATA_API_KEY;

if (!apiKey) {
  throw new Error('METADATA_API_KEY environment variable is required');
}

// Rotate keys periodically
class SecureMetadataClient {
  private keyRotationInterval = 86400000; // 24 hours
  
  constructor(private getApiKey: () => Promise<string>) {
    this.scheduleKeyRotation();
  }
  
  private async scheduleKeyRotation() {
    setInterval(async () => {
      const newKey = await this.getApiKey();
      this.client.updateApiKey(newKey);
    }, this.keyRotationInterval);
  }
}
```

### 2. Input Validation

```typescript
function validateFilePath(path: string): string {
  // Prevent directory traversal
  if (path.includes('..') || path.includes('~')) {
    throw new Error('Invalid file path');
  }
  
  // Ensure path is within allowed directories
  const allowedPrefixes = ['framework/', 'docs/', 'src/'];
  if (!allowedPrefixes.some(prefix => path.startsWith(prefix))) {
    throw new Error('Access denied to this path');
  }
  
  return path.normalize();
}
```

## Troubleshooting

### Common Issues and Solutions

1. **Connection Timeouts**
   - Increase client timeout setting
   - Check network connectivity
   - Verify API endpoint is accessible

2. **Rate Limiting**
   - Implement request queuing
   - Use batch operations
   - Cache responses appropriately

3. **WebSocket Disconnections**
   - Implement automatic reconnection
   - Handle connection state properly
   - Use heartbeat/ping messages

4. **Large Response Handling**
   - Use pagination for list operations
   - Implement streaming for large files
   - Compress responses when possible

## Next Steps

1. Explore the [API Reference](./enhanced_metadata_api.md) for detailed endpoint documentation
2. Review [Sample Responses](./sample_responses.md) for real-world examples
3. Check [WebSocket Events](./websocket_events.md) for real-time integration
4. Join our developer community for support and updates

Remember to always handle errors gracefully and implement proper logging for debugging purposes.