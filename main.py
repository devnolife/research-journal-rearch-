#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Research Journal Search System
Multi-Platform Journal Search with Content-Based Filtering

Usage:
    python main.py [--host HOST] [--port PORT] [--debug]
    
Examples:
    python main.py                    # Run with defaults (localhost:5000)
    python main.py --port 8080        # Run on port 8080
    python main.py --host 0.0.0.0     # Allow external access
    python main.py --debug            # Enable debug mode
"""

import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_nltk():
    """Download required NLTK data if not present"""
    import nltk
    required_packages = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
    
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}' if package == 'punkt' else f'corpora/{package}')
        except LookupError:
            print(f"📥 Downloading NLTK package: {package}")
            nltk.download(package, quiet=True)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Research Journal Search System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    Run with default settings
  python main.py --port 8080        Run on port 8080
  python main.py --host 0.0.0.0     Allow external connections
  python main.py --debug            Enable debug mode
        """
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host to run the server on (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run the server on (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Banner
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   📚 Research Journal Search System                         ║
║   Multi-Platform Search with Content-Based Filtering        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Setup NLTK
    print("🔧 Checking NLTK packages...")
    setup_nltk()
    print("✅ NLTK packages ready")
    
    # Create uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("📁 Created uploads directory")
    
    # Import and run Flask app
    print(f"\n🚀 Starting server on http://{args.host}:{args.port}")
    print("   Press Ctrl+C to stop\n")
    
    from app import app
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

if __name__ == '__main__':
    main()
