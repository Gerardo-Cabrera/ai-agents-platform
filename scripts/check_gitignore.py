#!/usr/bin/env python3
"""
GitIgnore Checker Script
This script checks if .gitignore files are working correctly and identifies files that should be ignored.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Set

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n{step}. {description}")
    print("-" * 40)

def get_git_status():
    """Get the current git status."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        print("❌ Error running git status")
        return []

def get_untracked_files():
    """Get untracked files from git."""
    try:
        result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        print("❌ Error getting untracked files")
        return []

def check_environment_files():
    """Check for environment files that should be ignored."""
    print_step("1", "Checking Environment Files")
    
    env_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.startswith('.env'):
                env_files.append(os.path.join(root, file))
    
    if env_files:
        print("⚠️  Found environment files that should be ignored:")
        for file in env_files:
            print(f"   - {file}")
        print("\n   These files contain sensitive information and should not be committed!")
    else:
        print("✅ No environment files found (good!)")

def check_secret_files():
    """Check for secret files that should be ignored."""
    print_step("2", "Checking Secret Files")
    
    secret_extensions = ['.key', '.pem', '.p12', '.pfx', '.crt', '.csr']
    secret_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in secret_extensions):
                secret_files.append(os.path.join(root, file))
    
    if secret_files:
        print("⚠️  Found secret files that should be ignored:")
        for file in secret_files:
            print(f"   - {file}")
        print("\n   These files contain sensitive information and should not be committed!")
    else:
        print("✅ No secret files found (good!)")

def check_cache_directories():
    """Check for cache directories that should be ignored."""
    print_step("3", "Checking Cache Directories")
    
    cache_dirs = [
        '__pycache__',
        'node_modules',
        '.cache',
        'cache',
        '.temp',
        'temp',
        'tmp',
        'logs',
        'uploads',
        'data',
        'chroma_db'
    ]
    
    found_cache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root:
            continue
            
        for dir_name in dirs:
            if dir_name in cache_dirs:
                full_path = os.path.join(root, dir_name)
                found_cache_dirs.append(full_path)
    
    if found_cache_dirs:
        print("⚠️  Found cache directories that should be ignored:")
        for dir_path in found_cache_dirs:
            print(f"   - {dir_path}")
    else:
        print("✅ No cache directories found (good!)")

def check_large_files():
    """Check for large files that might need to be ignored."""
    print_step("4", "Checking Large Files")
    
    large_files = []
    max_size = 10 * 1024 * 1024  # 10MB
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) > max_size:
                    large_files.append(file_path)
            except (OSError, FileNotFoundError):
                continue
    
    if large_files:
        print("⚠️  Found large files (>10MB) that might need to be ignored:")
        for file_path in large_files:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"   - {file_path} ({size_mb:.1f}MB)")
        print("\n   Consider adding these to .gitignore if they're not needed in the repo")
    else:
        print("✅ No large files found (good!)")

def check_git_status():
    """Check what git sees as untracked or modified."""
    print_step("5", "Checking Git Status")
    
    untracked_files = get_untracked_files()
    status_files = get_git_status()
    
    if untracked_files:
        print("📋 Untracked files (not in git):")
        for file in untracked_files:
            print(f"   - {file}")
    else:
        print("✅ No untracked files")
    
    if status_files:
        print("\n📋 Modified/staged files:")
        for file in status_files:
            print(f"   - {file}")
    else:
        print("✅ No modified files")

def suggest_gitignore_additions():
    """Suggest additions to .gitignore files."""
    print_step("6", "Suggesting .gitignore Additions")
    
    suggestions = []
    
    # Check for common patterns that might be missing
    patterns_to_check = [
        '*.log',
        '*.tmp',
        '*.temp',
        '*.bak',
        '*.backup',
        '*.old',
        '*.orig',
        '*.db',
        '*.sqlite',
        '*.sqlite3',
        'logs/',
        'temp/',
        'tmp/',
        'cache/',
        '.cache/',
        'uploads/',
        'data/',
        'node_modules/',
        '__pycache__/',
        '.env',
        '.env.local',
        '.env.development',
        '.env.production',
        '*.key',
        '*.pem',
        '*.crt',
        'secrets/',
        '.secrets/',
        '.vscode/',
        '.idea/',
        '.DS_Store',
        'Thumbs.db',
        'coverage/',
        '.coverage',
        'htmlcov/',
        '.nyc_output/',
        'dist/',
        'build/',
        '.next/',
        '.nuxt/',
        'out/',
        'chroma_db/',
        '*.chroma',
        '*.pkl',
        '*.joblib',
        '*.h5',
        '*.onnx'
    ]
    
    print("💡 Common patterns to consider adding to .gitignore:")
    for pattern in patterns_to_check:
        print(f"   - {pattern}")

def check_specific_project_files():
    """Check for project-specific files that should be ignored."""
    print_step("7", "Checking Project-Specific Files")
    
    project_specific_patterns = [
        'debug_env.py',
        'debug_*.py',
        'system_optimizer/',
        'utils/system_optimizer.py',
        'agents/',
        'agent_cache/',
        'agent_logs/',
        'grafana/',
        'grafana-v*/',
        'prometheus/',
        'prometheus.yml',
        'metrics/',
        'monitoring/',
        '.railway/',
        'railway.json.local',
        'docker-compose.override.yml',
        'docker-compose.local.yml'
    ]
    
    found_files = []
    for pattern in project_specific_patterns:
        if '*' in pattern:
            # Handle wildcard patterns
            base_pattern = pattern.replace('*', '')
            for root, dirs, files in os.walk('.'):
                if '.git' in root:
                    continue
                    
                for file in files:
                    if base_pattern in file or file.startswith(base_pattern):
                        found_files.append(os.path.join(root, file))
        else:
            # Handle exact patterns
            if os.path.exists(pattern):
                found_files.append(pattern)
    
    if found_files:
        print("📋 Project-specific files found:")
        for file in found_files:
            print(f"   - {file}")
    else:
        print("✅ No project-specific files found")

def main():
    """Main function."""
    print_header("GitIgnore Checker")
    print("This script checks if your .gitignore files are working correctly.")
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository. Please run this script from the project root.")
        sys.exit(1)
    
    # Run all checks
    check_environment_files()
    check_secret_files()
    check_cache_directories()
    check_large_files()
    check_git_status()
    suggest_gitignore_additions()
    check_specific_project_files()
    
    print_header("Summary")
    print("✅ GitIgnore check completed!")
    print("\nNext steps:")
    print("1. Review any warnings above")
    print("2. Add missing patterns to appropriate .gitignore files")
    print("3. Remove any sensitive files that were accidentally committed")
    print("4. Run 'git add .' and 'git commit' to commit your changes")

if __name__ == "__main__":
    main() 