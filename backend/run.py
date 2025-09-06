#!/usr/bin/env python3
"""
Entry point for the Flask application
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production with gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
