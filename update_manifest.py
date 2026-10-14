import json
import hashlib
import time

# 1. Unified Identity Anchor (CRA Business Number Root)
identity = {
    "cra_business_number": "735350936",
    "gst_hst_account": "735350936RT0001",
    "operating_name": "JS INNOVATION8390-1 INC",
    "authorized_owner": "Jujita Stairs",
    "registered_address": "9827 159 ST NW, EDMONTON AB T5P2Z6, CANADA"
}

# 2. Comprehensive Asset Registry (Software IP + Overseas Real Estate)
all_assets = {
    "intellectual_property": [
        {
            "title": "Octopus Payment Architecture",
            "version": "2.1",
            "repository": "Octopus2.0",
            "jurisdiction": "Global / CA / US"
        },
        {
            "title": "Regulators Companion Compliance Engine",
            "version": "1.0",
            "repository": "Regulators-Companion",
            "jurisdiction": "Global / CA / US"
        }
    ],
    "real_estate_and_physical_holdings": [
        {
            "asset_class": "Overseas Real Estate Holding",
            "beneficial_owner": "JS INNOVATION8390-1 INC",
            "legal_controller": "Jujita Stairs",
            "status": "Cryptographically Re-anchored to BN 735350936"
        }
    ]
}

# Construct Unified Master Manifest
master_manifest = {
    "manifest_version": "2.0.0",
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "primary_entity": identity,
    "consolidated_assets": all_assets
}

# Canonicalize JSON (sorted keys, compact indent)
canonical_json = json.dumps(master_manifest, sort_keys=True, indent=2)

# Save to disk
filename = "master_asset_provenance_manifest.json"
with open(filename, "w") as f:
    f.write(canonical_json)

# Compute Master SHA-256 Digest
master_digest = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

print("=" * 68)
print(f"MASTER MANIFEST UPDATED: {filename}")
print("=" * 68)
print(f"NEW MASTER SHA-256 PROVENANCE ANCHOR:")
print(f"0x{master_digest}")
print("=" * 68)
