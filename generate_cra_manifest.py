import json
import hashlib
import time

# 1. Sole Proprietorship Identity Root
identity = {
    "cra_business_number_root": "735350936",
    "gst_hst_account": "735350936RT0001",
    "payroll_account": "735350936RP0001",
    "operating_name": "JS INNOVATION8390-1 INC",
    "authorized_owner": "Jujita Stairs",
    "registered_address": "9827 159 ST NW, EDMONTON AB T5P2Z6, CANADA"
}

# 2. Intellectual Property Assets
ip_assets = [
    {
        "title": "Octopus Payment Architecture",
        "repository": "Octopus2.0",
        "version": "2.1",
        "jurisdiction": "CA / US / Global"
    },
    {
        "title": "Regulators Companion Compliance Engine",
        "repository": "Regulators-Companion",
        "version": "1.0",
        "jurisdiction": "CA / US / Global"
    }
]

# 3. CRA Form T1135 Overseas Real Estate & Holdings
cra_t1135_holdings = {
    "reporting_threshold": "Specified Foreign Property (Income Tax Act s. 233.3)",
    "primary_filer_bn": "735350936",
    "overseas_real_estate": [
        {
            "asset_description": "Overseas Real Property / Foreign Holdings",
            "country_code": "PH", # Philippines or specified country jurisdiction
            "beneficial_entity": "JS INNOVATION8390-1 INC",
            "legal_controller": "Jujita Stairs",
            "cra_declaration_status": "Anchored to BN 735350936 for T1135 Compliance"
        }
    ]
}

# Unified Master Manifest
master_manifest = {
    "manifest_version": "3.0.0",
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "frameworks": [
        "CRA Form T1135 (Foreign Income Verification)",
        "WIPO ST.96 / ST.3",
        "CIPO e-Filing",
        "LAC Legal Deposit",
        "USPTO 37 CFR 1.98 / 2.11"
    ],
    "applicant_entity": identity,
    "intellectual_property": ip_assets,
    "foreign_property_declarations": cra_t1135_holdings
}

# Canonicalize JSON
canonical_json = json.dumps(master_manifest, sort_keys=True, indent=2)

# Write to disk
with open("canada_cra_master_manifest.json", "w") as f:
    f.write(canonical_json)

# Calculate SHA-256 Digest
digest = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

print("=" * 68)
print("CANADA CRA & GLOBAL PROVENANCE MANIFEST GENERATED")
print("=" * 68)
print(f"CANADIAN PROVENANCE SHA-256 DIGEST:")
print(f"0x{digest}")
print("=" * 68)
