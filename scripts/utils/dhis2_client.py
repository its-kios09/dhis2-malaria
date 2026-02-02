"""
DHIS2 API Client
Reusable utilities for interacting with DHIS2 REST API
"""

import requests
import json
from typing import Dict, List, Optional


class DHIS2Client:
    """Client for DHIS2 API operations"""
    
    def __init__(self, base_url: str, username: str, password: str):
        """Initialize DHIS2 client"""
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({"Content-Type": "application/json"})
    
    def create_org_unit(self, name: str, short_name: str, 
                       opening_date: str, parent_id: Optional[str] = None) -> Optional[str]:
        """Create organization unit and return its ID"""
        payload = {
            "name": name,
            "shortName": short_name,
            "openingDate": opening_date
        }
        
        if parent_id:
            payload["parent"] = {"id": parent_id}
        
        response = self.session.post(
            f"{self.base_url}/api/organisationUnits",
            json=payload
        )
        
        if response.status_code == 201:
            return response.json()["response"]["uid"]
        else:
            print(f"❌ Failed to create {name}: {response.text}")
            return None
    
    @staticmethod
    def load_config(config_path: str = "config/config.json") -> Dict:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_mapping(mapping: Dict, filepath: str):
        """Save ID mapping to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(mapping, f, indent=2)
        print(f"💾 Saved to: {filepath}")
