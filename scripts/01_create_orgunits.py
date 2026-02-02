#!/usr/bin/env python3
"""
Script 01: Create Organization Units
Creates Kenya root and all 47 counties in DHIS2
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils.dhis2_client import DHIS2Client

COUNTIES = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo Marakwet",
    "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado",
    "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga",
    "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia",
    "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit",
    "Meru", "Migori", "Mombasa", "Muranga", "Nairobi",
    "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua",
    "Nyeri", "Samburu", "Siaya", "Taita Taveta", "Tana River",
    "Tharaka Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu",
    "Vihiga", "Wajir", "West Pokot"
]

def main():
    print("="*60)
    print("🇰🇪 DHIS2 Organization Units Setup")
    print("="*60)
    print()
    
    config = DHIS2Client.load_config()
    client = DHIS2Client(
        base_url=config['dhis2_url'],
        username=config['username'],
        password=config['password']
    )
    print(f"🔗 Connected to: {config['dhis2_url']}\n")
    
    print("Step 1: Creating Kenya (root organization unit)...")
    print("-" * 60)
    
    kenya_id = client.create_org_unit(
        name="Kenya",
        short_name="KE",
        opening_date="2018-01-01"
    )
    
    if not kenya_id:
        print("Failed to create Kenya. Exiting.")
        sys.exit(1)
    
    print(f"Created Kenya: {kenya_id}\n")
    
    print("Step 2: Creating 47 counties...")
    print("-" * 60)
    
    county_map = {}
    success_count = 0
    
    for i, county_name in enumerate(COUNTIES, 1):
        full_name = f"{county_name} County"
        
        county_id = client.create_org_unit(
            name=full_name,
            short_name=county_name[:50],
            opening_date="2018-01-01",
            parent_id=kenya_id
        )
        
        if county_id:
            county_map[full_name] = county_id
            success_count += 1
            print(f"[{success_count:2d}/47] {county_name} County: {county_id}")
        else:
            print(f"[{i:2d}/47] Failed: {county_name} County")
    
    print()
    print("Step 3: Saving county ID mappings...")
    print("-" * 60)
    
    DHIS2Client.save_mapping(county_map, "data/mappings/county_id_map.json")
    
    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Counties created: {success_count}/47")
    print(f"Kenya ID: {kenya_id}")
    print(f"Mapping saved: data/mappings/county_id_map.json")
    
    if success_count == 47:
        print("All counties created successfully!")
    else:
        print(f"{47 - success_count} counties failed")
    
    print("="*60)

if __name__ == "__main__":
    main()
