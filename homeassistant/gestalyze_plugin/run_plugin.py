#!/usr/bin/env python3
import sys
import os
import logging

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ha_gestalyze_plugin import GestalyzePlugin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Run the Home Assistant plugin independently."""
    try:
        # Initialize and start the plugin
        plugin = GestalyzePlugin()
        plugin.start()
        
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping Home Assistant plugin...")
        plugin.stop()
    except Exception as e:
        print(f"Error running plugin: {e}")
        plugin.stop()

if __name__ == "__main__":
    main()
