from flask import Flask
import configparser
import logging
import datetime

logging.basicConfig(filename='elefant.log', level=logging.DEBUG)

config = configparser.ConfigParser(interpolation=None)
config.read("conf/app.conf")

app = Flask(__name__,
            static_url_path='')
app.config['SECRET_KEY'] = config['cryptography']['SecretKey']
app.config['BASIC_AUTH_USERNAME'] = config['auth']['User']
app.config['BASIC_AUTH_PASSWORD'] = config['auth']['Password']


def timeago(timestamp_str):
    """Convert ISO timestamp to relative time string like '2 hours ago'"""
    try:
        if not timestamp_str:
            return ""
        
        # Parse ISO timestamp
        timestamp = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.datetime.utcnow()
        
        # Calculate time difference
        diff = now - timestamp
        
        # Convert to total seconds
        total_seconds = int(diff.total_seconds())
        
        if total_seconds < 60:
            return "just now"
        elif total_seconds < 3600:  # Less than 1 hour
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif total_seconds < 86400:  # Less than 1 day
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif total_seconds < 172800:  # Less than 2 days
            return "yesterday"
        elif total_seconds < 604800:  # Less than 1 week
            days = total_seconds // 86400
            return f"{days} days ago"
        elif total_seconds < 2629746:  # Less than 1 month (30.44 days)
            weeks = total_seconds // 604800
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif total_seconds < 31556952:  # Less than 1 year
            months = total_seconds // 2629746
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            # For very old dates, show the actual date
            return timestamp.strftime("%b %d, %Y")
            
    except Exception:
        # Fallback to original timestamp if parsing fails
        return timestamp_str


# Register the template filter
app.jinja_env.filters['timeago'] = timeago

from app import routes
