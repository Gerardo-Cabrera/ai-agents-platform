# AI API Examples - Practical Usage Guide

This file contains practical examples for using the AI API endpoints with DeepSeek/Ollama integration.

## Quick Start

### 1. Get Access Token
```bash
# Login to get your access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

### 2. Set Environment Variable
```bash
# Set your token as environment variable
export ACCESS_TOKEN="your_access_token_here"
```

## Basic Examples

### Check AI Health
```bash
curl -X GET "http://localhost:8000/api/v1/ai/health" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### List Available Models
```bash
curl -X GET "http://localhost:8000/api/v1/ai/models" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Generate Simple Response
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, how are you?",
    "model": "deepseek-coder:6.7b"
  }'
```

## Code Generation Examples

### Python Function
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function that takes a list of numbers and returns the sum of all even numbers",
    "model": "deepseek-coder:6.7b"
  }'
```

### JavaScript Function
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a JavaScript function that validates an email address using regex",
    "model": "deepseek-coder:6.7b"
  }'
```

### SQL Query
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a SQL query to find all users who registered in the last 30 days and have made at least one purchase",
    "model": "deepseek-coder:6.7b"
  }'
```

## Code Review Examples

### Review Python Code
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this Python code and suggest improvements:\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
    "model": "deepseek-coder:6.7b"
  }'
```

### Review JavaScript Code
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this JavaScript code and suggest improvements:\n\nfunction fetchUserData(userId) {\n    fetch(`/api/users/${userId}`)\n        .then(response => response.json())\n        .then(data => console.log(data))\n        .catch(error => console.error(error));\n}",
    "model": "deepseek-coder:6.7b"
  }'
```

## Documentation Examples

### API Documentation
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate OpenAPI documentation for a REST API with these endpoints:\n- GET /users - List all users\n- POST /users - Create a new user\n- GET /users/{id} - Get user by ID\n- PUT /users/{id} - Update user\n- DELETE /users/{id} - Delete user",
    "model": "deepseek-coder:6.7b"
  }'
```

### README Generation
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a README.md file for a Python FastAPI project that includes user authentication, database integration, and API documentation",
    "model": "deepseek-coder:6.7b"
  }'
```

## Configuration Examples

### Dockerfile
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a multi-stage Dockerfile for a Python FastAPI application with the following requirements:\n- Python 3.11\n- PostgreSQL client\n- Redis client\n- Production-ready with nginx",
    "model": "deepseek-coder:6.7b"
  }'
```

### Docker Compose
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a docker-compose.yml file for a web application with:\n- FastAPI backend\n- React frontend\n- PostgreSQL database\n- Redis cache\n- Nginx reverse proxy",
    "model": "deepseek-coder:6.7b"
  }'
```

## Testing Examples

### Unit Test
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write unit tests for this Python function:\n\ndef calculate_discount(price, discount_percent):\n    if discount_percent < 0 or discount_percent > 100:\n        raise ValueError(\"Discount must be between 0 and 100\")\n    return price * (1 - discount_percent / 100)",
    "model": "deepseek-coder:6.7b"
  }'
```

### Integration Test
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create integration tests for a user authentication API with endpoints for login, register, and logout",
    "model": "deepseek-coder:6.7b"
  }'
```

## Chat Examples

### Technical Discussion
```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain the differences between REST and GraphQL APIs, and when to use each one",
    "model": "deepseek-coder:6.7b"
  }'
```

### Problem Solving
```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I have a performance issue with my database queries. The application is slow when fetching large datasets. What are the best practices to optimize this?",
    "model": "deepseek-coder:6.7b"
  }'
```

## Model Management

### Download New Model
```bash
curl -X POST "http://localhost:8000/api/v1/ai/pull-model" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "llama2:7b"
  }'
```

### Download Code-Specific Model
```bash
curl -X POST "http://localhost:8000/api/v1/ai/pull-model" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "codellama:7b"
  }'
```

## Python Script Examples

### Complete Python Script
```python
#!/usr/bin/env python3
"""
AI API Client Example
"""
import requests
import json
import os
from typing import Optional, Dict, Any

class AIClient:
    def __init__(self, base_url: str = "http://localhost:8000", token: Optional[str] = None):
        self.base_url = base_url
        self.token = token or os.getenv("ACCESS_TOKEN")
        if not self.token:
            raise ValueError("Access token required. Set ACCESS_TOKEN environment variable or pass token parameter.")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def check_health(self) -> Dict[str, Any]:
        """Check AI service health"""
        response = requests.get(f"{self.base_url}/api/v1/ai/health", headers=self.headers)
        return response.json()
    
    def list_models(self) -> Dict[str, Any]:
        """List available models"""
        response = requests.get(f"{self.base_url}/api/v1/ai/models", headers=self.headers)
        return response.json()
    
    def generate(self, prompt: str, model: str = "deepseek-coder:6.7b") -> Dict[str, Any]:
        """Generate response"""
        data = {"prompt": prompt, "model": model}
        response = requests.post(f"{self.base_url}/api/v1/ai/generate", 
                               headers=self.headers, json=data)
        return response.json()
    
    def chat(self, prompt: str, model: str = "deepseek-coder:6.7b") -> Dict[str, Any]:
        """Chat with AI"""
        data = {"prompt": prompt, "model": model}
        response = requests.post(f"{self.base_url}/api/v1/ai/chat", 
                               headers=self.headers, json=data)
        return response.json()
    
    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Download new model"""
        data = {"model_name": model_name}
        response = requests.post(f"{self.base_url}/api/v1/ai/pull-model", 
                               headers=self.headers, json=data)
        return response.json()

def main():
    """Example usage"""
    try:
        # Initialize client
        client = AIClient()
        
        # Check health
        health = client.check_health()
        print(f"AI Service Health: {health['status']}")
        print(f"Available Models: {health['models']}")
        
        # Generate code
        result = client.generate("Write a Python function to calculate factorial")
        print(f"\nGenerated Code:\n{result['response']}")
        
        # Chat
        chat_result = client.chat("Explain what is recursion in programming")
        print(f"\nChat Response:\n{chat_result['response']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### Usage Script
```python
#!/usr/bin/env python3
"""
Quick AI API Usage Script
"""
import requests
import json

def quick_ai_request(prompt: str, model: str = "deepseek-coder:6.7b"):
    """Quick function to make AI requests"""
    url = "http://localhost:8000/api/v1/ai/generate"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN_HERE",
        "Content-Type": "application/json"
    }
    data = {"prompt": prompt, "model": model}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Replace with your actual access token
    prompt = "Write a simple Python function to reverse a string"
    result = quick_ai_request(prompt)
    print(json.dumps(result, indent=2))
```

## JavaScript/Node.js Examples

### Node.js Client
```javascript
const axios = require('axios');

class AIClient {
    constructor(baseUrl = 'http://localhost:8000', token) {
        this.baseUrl = baseUrl;
        this.token = token || process.env.ACCESS_TOKEN;
        
        if (!this.token) {
            throw new Error('Access token required. Set ACCESS_TOKEN environment variable or pass token parameter.');
        }
        
        this.client = axios.create({
            baseURL: this.baseUrl,
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        });
    }
    
    async checkHealth() {
        const response = await this.client.get('/api/v1/ai/health');
        return response.data;
    }
    
    async listModels() {
        const response = await this.client.get('/api/v1/ai/models');
        return response.data;
    }
    
    async generate(prompt, model = 'deepseek-coder:6.7b') {
        const response = await this.client.post('/api/v1/ai/generate', {
            prompt,
            model
        });
        return response.data;
    }
    
    async chat(prompt, model = 'deepseek-coder:6.7b') {
        const response = await this.client.post('/api/v1/ai/chat', {
            prompt,
            model
        });
        return response.data;
    }
    
    async pullModel(modelName) {
        const response = await this.client.post('/api/v1/ai/pull-model', {
            model_name: modelName
        });
        return response.data;
    }
}

// Example usage
async function main() {
    try {
        const client = new AIClient();
        
        // Check health
        const health = await client.checkHealth();
        console.log('AI Service Health:', health.status);
        console.log('Available Models:', health.models);
        
        // Generate code
        const result = await client.generate('Write a JavaScript function to validate email');
        console.log('\nGenerated Code:', result.response);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

## Troubleshooting

### Common Issues

1. **Authentication Error (401)**
   - Make sure you have a valid access token
   - Check if the token has expired
   - Verify the Authorization header format

2. **Connection Error**
   - Ensure the backend service is running
   - Check if Ollama is accessible from the backend
   - Verify the OLLAMA_BASE_URL configuration

3. **Model Not Found**
   - Check available models with `/api/v1/ai/models`
   - Download the required model with `/api/v1/ai/pull-model`
   - Verify the model name is correct

4. **Timeout Errors**
   - Some operations (like pulling models) may take time
   - Increase timeout settings in your client
   - Check network connectivity

### Debug Commands

```bash
# Check if backend is running
curl -s http://localhost:8000/health

# Check AI health (no auth required)
curl -s http://localhost:8000/api/v1/ai/health

# Check Ollama directly
curl -s http://localhost:11434/api/tags

# Test with verbose output
curl -v -X POST "http://localhost:8000/api/v1/ai/generate" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "model": "deepseek-coder:6.7b"}'
```

## Best Practices

1. **Always handle errors** in your client code
2. **Use appropriate timeouts** for long-running operations
3. **Cache responses** when appropriate to reduce API calls
4. **Validate inputs** before sending to the API
5. **Use retry logic** for transient failures
6. **Monitor API usage** and implement rate limiting if needed
7. **Keep your access tokens secure** and rotate them regularly
8. **Use specific prompts** for better results
9. **Test with different models** to find the best fit for your use case
10. **Document your prompts** for consistency and reproducibility 