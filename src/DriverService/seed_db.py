import json
import urllib.request
import urllib.error
import sys
import time

# Configuration
API_BASE_URL = "http://localhost:6001/api"
DRIVERS_FILE = "sample_driver_records.json"
FORMS_FILE = "sample_form_records.json"

def get_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"❌ Error connecting to {url}: {e}")
        sys.exit(1)
    return []

def post_json(url, data):
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            return response.status in (200, 201)
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to add record: {e.code} - {e.read().decode()}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e}")
        return False

def seed_drivers():
    print("🚗 Seeding Drivers...")
    
    # Load sample data
    try:
        with open(DRIVERS_FILE, 'r') as f:
            drivers_to_seed = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {DRIVERS_FILE}")
        return

    # Get existing drivers
    existing_drivers = get_json(f"{API_BASE_URL}/drivers/list")
    existing_licenses = {d.get('licenseNumber') for d in existing_drivers}
    
    count = 0
    for driver in drivers_to_seed:
        if driver.get('licenseNumber') in existing_licenses:
            print(f"   ⚠️  Skipping {driver.get('fullName')} (License: {driver.get('licenseNumber')}) - Already exists")
        else:
            if post_json(f"{API_BASE_URL}/drivers", driver):
                print(f"   ✅ Added {driver.get('fullName')}")
                count += 1
            else:
                print(f"   ❌ Failed to add {driver.get('fullName')}")
    
    print(f"🏁 Driver seeding complete. Added {count} new drivers.\n")

def seed_forms():
    print("📝 Seeding Forms...")
    
    # Load sample data
    try:
        with open(FORMS_FILE, 'r') as f:
            forms_to_seed = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {FORMS_FILE}")
        return

    # Get existing forms to check for duplicates (simplified check)
    # Since forms don't have unique keys in the JSON, we'll check loosely based on driverId and vehicleId
    existing_forms = get_json(f"{API_BASE_URL}/forms/list")
    
    # Create a set of existing (driverId, vehicleId) tuples for quick lookup
    # Note: This assumes we only want one form per driver-vehicle pair for seeding purposes.
    # Adjust logic if multiple forms per pair are allowed.
    existing_pairs = {(f.get('driverId'), f.get('vehicleId')) for f in existing_forms}

    count = 0
    for form in forms_to_seed:
        driver_id = form.get('driverId')
        vehicle_id = form.get('vehicleId')
        
        # Basic check: if we already have a form for this driver+vehicle, skip
        # This prevents duplicate seeding on multiple runs
        if (driver_id, vehicle_id) in existing_pairs:
             print(f"   ⚠️  Skipping Form (Driver: {driver_id}, Vehicle: {vehicle_id}) - Already exists")
        else:
            if post_json(f"{API_BASE_URL}/forms", form):
                print(f"   ✅ Added Form (Driver: {driver_id}, Vehicle: {vehicle_id})")
                count += 1
            else:
                print(f"   ❌ Failed to add Form")

    print(f"🏁 Form seeding complete. Added {count} new forms.\n")

def main():
    print("🌱 Starting Database Seeder...\n")
    
    # Check if service is reachable
    try:
        urllib.request.urlopen(f"{API_BASE_URL}/drivers/list")
    except Exception:
        print("❌ Driver Service is not reachable at http://localhost:6001")
        print("   Please make sure the service is running (use ./setup-and-run.sh)")
        sys.exit(1)

    seed_drivers()
    seed_forms()
    print("✨ Seeding process finished!")

if __name__ == "__main__":
    main()

