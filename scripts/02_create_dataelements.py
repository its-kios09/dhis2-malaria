#!/usr/bin/env python3
"""
Script 02: Create Data Elements
Creates malaria commodity data elements in DHIS2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils.dhis2_client import DHIS2Client
import requests


def create_data_element(client, name, short_name, code, value_type="INTEGER", agg_type="SUM"):
    """Create a data element"""
    payload = {
        "name": name,
        "shortName": short_name,
        "code": code,
        "valueType": value_type,
        "aggregationType": agg_type,
        "domainType": "AGGREGATE",
        "zeroIsSignificant": False
    }
    
    response = client.session.post(
        f"{client.base_url}/api/dataElements",
        json=payload
    )
    
    if response.status_code == 201:
        return response.json()["response"]["uid"]
    else:
        print(f"❌ Failed to create {name}: {response.text}")
        return None


def main():
    print("="*60)
    print("💊 DHIS2 Data Elements Setup")
    print("="*60)
    print()
    
    config = DHIS2Client.load_config()
    client = DHIS2Client(
        base_url=config['dhis2_url'],
        username=config['username'],
        password=config['password']
    )
    print(f"🔗 Connected to: {config['dhis2_url']}\n")
    
    data_elements = [
        {
            "name": "MAL - RDT Dispensed",
            "short_name": "RDT Dispensed",
            "code": "MAL_RDT_DISP",
            "value_type": "INTEGER",
            "agg_type": "SUM"
        },
        {
            "name": "MAL - RDT Stock on Hand",
            "short_name": "RDT Stock",
            "code": "MAL_RDT_SOH",
            "value_type": "INTEGER",
            "agg_type": "AVERAGE"
        },
        {
            "name": "MAL - RDT Predicted Demand (AI)",
            "short_name": "RDT Predicted",
            "code": "MAL_RDT_PRED",
            "value_type": "INTEGER",
            "agg_type": "SUM"
        }
    ]
    
    print("Creating data elements...")
    print("-" * 60)
    
    element_map = {}
    success_count = 0
    
    for i, element in enumerate(data_elements, 1):
        element_id = create_data_element(
            client,
            name=element["name"],
            short_name=element["short_name"],
            code=element["code"],
            value_type=element["value_type"],
            agg_type=element["agg_type"]
        )
        
        if element_id:
            element_map[element["code"]] = element_id
            success_count += 1
            print(f"✅ [{success_count}/{len(data_elements)}] {element['name']}: {element_id}")
        else:
            print(f"❌ [{i}/{len(data_elements)}] Failed: {element['name']}")
    
    print()
    print("Saving data element mappings...")
    print("-" * 60)
    
    DHIS2Client.save_mapping(element_map, "data/mappings/dataelement_map.json")
    
    print()
    print("="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"✅ Data elements created: {success_count}/{len(data_elements)}")
    print(f"📁 Mapping saved: data/mappings/dataelement_map.json")
    
    if success_count == len(data_elements):
        print("🎉 All data elements created successfully!")
    else:
        print(f"⚠️  {len(data_elements) - success_count} elements failed")
    
    print("="*60)


if __name__ == "__main__":
    main()
