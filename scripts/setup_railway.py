#!/usr/bin/env python3
"""
Railway Setup Script
This script helps configure Railway deployment and environment variables.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n{step}. {description}")
    print("-" * 40)

def check_railway_cli():
    """Check if Railway CLI is installed."""
    try:
        result = subprocess.run(['railway', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
        else:
            print("❌ Railway CLI is not installed")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI is not installed")
        return False

def install_railway_cli():
    """Install Railway CLI."""
    print_step("1", "Installing Railway CLI")
    
    try:
        # Try npm first
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI installed via npm")
        return True
    except subprocess.CalledProcessError:
        try:
            # Try with sudo if needed
            subprocess.run(['sudo', 'npm', 'install', '-g', '@railway/cli'], check=True)
            print("✅ Railway CLI installed via npm (with sudo)")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Railway CLI via npm")
            print("Please install manually: https://docs.railway.app/develop/cli")
            return False

def login_railway():
    """Login to Railway."""
    print_step("2", "Logging into Railway")
    
    try:
        subprocess.run(['railway', 'login'], check=True)
        print("✅ Successfully logged into Railway")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to login to Railway")
        return False

def create_railway_project():
    """Create a new Railway project."""
    print_step("3", "Creating Railway Project")
    
    project_name = input("Enter project name (or press Enter for auto-generated): ").strip()
    
    try:
        if project_name:
            subprocess.run(['railway', 'init', '--name', project_name], check=True)
        else:
            subprocess.run(['railway', 'init'], check=True)
        print("✅ Railway project created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create Railway project")
        return False

def setup_environment_variables():
    """Set up environment variables in Railway."""
    print_step("4", "Setting up Environment Variables")
    
    # Read backend env.example
    backend_env_path = Path("backend/env.example")
    if not backend_env_path.exists():
        print("❌ backend/env.example not found")
        return False
    
    print("Reading environment variables from backend/env.example...")
    
    env_vars = {}
    with open(backend_env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Skip placeholder values
                if any(placeholder in value.lower() for placeholder in ['your-', 'placeholder', 'example']):
                    continue
                
                env_vars[key] = value
    
    print(f"Found {len(env_vars)} environment variables to set")
    
    # Ask user to confirm
    confirm = input("\nDo you want to set these variables in Railway? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Skipping environment variable setup")
        return True
    
    # Set variables in Railway
    for key, value in env_vars.items():
        try:
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ Set {key}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to set {key}")
    
    return True

def setup_database():
    """Set up PostgreSQL database in Railway."""
    print_step("5", "Setting up PostgreSQL Database")
    
    try:
        # Add PostgreSQL plugin
        subprocess.run(['railway', 'add'], check=True)
        print("✅ PostgreSQL database added to project")
        
        # Get the database URL
        result = subprocess.run(['railway', 'variables'], capture_output=True, text=True, check=True)
        if 'DATABASE_URL' in result.stdout:
            print("✅ DATABASE_URL is automatically set by Railway")
        else:
            print("⚠️  DATABASE_URL not found. Please check Railway dashboard.")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to add PostgreSQL database")
        return False

def deploy_project():
    """Deploy the project to Railway."""
    print_step("6", "Deploying to Railway")
    
    try:
        subprocess.run(['railway', 'up'], check=True)
        print("✅ Project deployed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to deploy project")
        return False

def get_project_url():
    """Get the deployed project URL."""
    print_step("7", "Getting Project URL")
    
    try:
        result = subprocess.run(['railway', 'domain'], capture_output=True, text=True, check=True)
        url = result.stdout.strip()
        if url:
            print(f"✅ Your application is available at: {url}")
            return url
        else:
            print("❌ Could not get project URL")
            return None
    except subprocess.CalledProcessError:
        print("❌ Failed to get project URL")
        return None

def update_frontend_env(backend_url):
    """Update frontend environment variables with backend URL."""
    if not backend_url:
        return False
    
    print_step("8", "Updating Frontend Environment Variables")
    
    frontend_env_path = Path("frontend/.env")
    if not frontend_env_path.exists():
        # Create from example
        example_path = Path("frontend/env.example")
        if example_path.exists():
            frontend_env_path.write_text(example_path.read_text())
    
    # Read current frontend env
    env_content = frontend_env_path.read_text()
    
    # Update URLs
    env_content = env_content.replace(
        "VITE_API_URL=http://localhost:8000",
        f"VITE_API_URL={backend_url}"
    )
    env_content = env_content.replace(
        "VITE_WS_URL=ws://localhost:8000",
        f"VITE_WS_URL={backend_url.replace('https://', 'wss://').replace('http://', 'ws://')}"
    )
    
    # Write updated content
    frontend_env_path.write_text(env_content)
    print("✅ Frontend environment variables updated")
    return True

def main():
    """Main setup function."""
    print_header("Railway Setup Script")
    print("This script will help you set up your AI Agents System on Railway.")
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Railway CLI
    if not check_railway_cli():
        if not install_railway_cli():
            sys.exit(1)
    
    # Login to Railway
    if not login_railway():
        sys.exit(1)
    
    # Create project
    if not create_railway_project():
        sys.exit(1)
    
    # Setup environment variables
    if not setup_environment_variables():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Deploy
    if not deploy_project():
        sys.exit(1)
    
    # Get URL
    backend_url = get_project_url()
    
    # Update frontend
    if backend_url:
        update_frontend_env(backend_url)
    
    print_header("Setup Complete!")
    print("Your AI Agents System has been deployed to Railway!")
    print(f"Backend URL: {backend_url}")
    print("\nNext steps:")
    print("1. Update your frontend environment variables with the backend URL")
    print("2. Deploy your frontend to Railway or another platform")
    print("3. Test all endpoints and WebSocket connections")
    print("4. Set up monitoring and alerts")

if __name__ == "__main__":
    main() 