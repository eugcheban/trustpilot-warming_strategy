import sys
import os
import django

sys.path.append('/home/user/Documents/vs-projects/trustpilot-warming_strategy/trustpilot') 
os.environ['DJANGO_SETTINGS_MODULE'] = 'parser_app.settings'
django.setup()