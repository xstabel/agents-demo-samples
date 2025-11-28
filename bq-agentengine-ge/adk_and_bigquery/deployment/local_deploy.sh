#!/bin/bash

# --- Variables ---
GOOGLE_CLOUD_PROJECT=yogaproject-1508
BIGQUERY_RUN_PROJECT_ID=yogaproject-1508
BIGQUERY_DATA_PROJECT_ID=yogaproject-1508-multimodal
STAGING_BUCKET=your-staging-bucket
export AUTH_ID="bigquery-agent-auth"
AGENT_DISPLAY_NAME="BigQuery Agent"
URL_MCP_TOOLSET="https://toolbox-93433691361.us-central1.run.app"

PROJECT_ID="yogaproject-1508" # Your Google Cloud Project ID
AUTHORIZATION_ID="bigquery-agent-auth" # A unique ID for the authorization, e.g., "gcal-agent-auth"
CLIENT_ID="93433691361-kts401qg0n6n2pk015l0cnjqmucvde1l.apps.googleusercontent.com"
CLIENT_SECRET="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" # The OAuth 2.0 Client Secret from your Google Cloud project
SCOPES="https://www.googleapis.com/auth/bigquery" # A space-separated list of OAuth scopes, e.g., "https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/userinfo.email"
DISCOVERY_ENGINE_API_BASE_URL="https://discoveryengine.googleapis.com/v1alpha"


# --- Script Body ---
AUTH_TOKEN=$(gcloud auth print-access-token)
echo "Please set it using: export PROJECT_ID=your-project-id"
