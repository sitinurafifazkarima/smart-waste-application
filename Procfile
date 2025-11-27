# 🚀 PROCFILE FOR DEPLOYMENT
# ==========================
# Defines how to run the app on various platforms

# For Heroku, Render, Railway
web: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
