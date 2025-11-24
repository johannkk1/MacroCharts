import json
import os
from datetime import datetime

class TemplateManager:
    def __init__(self, filepath='templates.json'):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({}, f)

    def get_templates(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_template(self, name, config):
        templates = self.get_templates()
        templates[name] = config
        with open(self.filepath, 'w') as f:
            json.dump(templates, f, indent=4)
        return True

    def delete_template(self, name):
        templates = self.get_templates()
        if name in templates:
            del templates[name]
            with open(self.filepath, 'w') as f:
                json.dump(templates, f, indent=4)
            return True
        return False

class HistoryManager:
    def __init__(self, filepath='history.json', max_items=50):
        self.filepath = filepath
        self.max_items = max_items
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def get_history(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def add_history(self, config):
        history = self.get_history()
        
        # Create a summary for display
        summary = {
            "timestamp": datetime.now().isoformat(),
            "ticker": config.get('ticker', 'Unknown'),
            "period": config.get('period', '1y'),
            "chart_type": config.get('chart_type', 'line'),
            "config": config # Store full config for restoration
        }
        
        # Add to beginning
        history.insert(0, summary)
        
        # Limit size
        if len(history) > self.max_items:
            history = history[:self.max_items]
            
        with open(self.filepath, 'w') as f:
            json.dump(history, f, indent=4)
        return summary

    def delete_history(self, index):
        """Delete a single history item by index"""
        history = self.get_history()
        if 0 <= index < len(history):
            del history[index]
            with open(self.filepath, 'w') as f:
                json.dump(history, f, indent=4)
            return True
        return False

    def clear_all_history(self):
        """Clear all history items"""
        with open(self.filepath, 'w') as f:
            json.dump([], f)
        return True
