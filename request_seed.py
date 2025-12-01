import requests
import json
import os
import re

# --- Configuration (UPDATE THESE VALUES CAREFULLY!) ---
# Use the exact URL from your assignment:
INSTRUCTOR_API_URL = "https://eqjeyq4z3qjojrqpovj2rnthdg0vjqf.lambda-url.ap-south-1.on.aws"
STUDENT_ID = "23A91A0502" 
GITHUB_REPO_URL = "https://github.com/23A91A0502/partnr-task2" 
# ----------------------------------------------------

PUBLIC_KEY_FILE = "student_public.pem" 
OUTPUT_FILE = "encrypted_seed.txt"


# NOTE: This function is now commented out as we are using the hardcoded key below.
# def format_public_key_for_api(key_path):
#     """Formats the public key into the single-line string required for the JSON payload."""
#     try:
#         with open(key_path, 'r') as f:
#             public_key_pem = f.read()
#         # Replaces all literal newlines with the escaped string "\n"
#         formatted_key = public_key_pem.strip().replace('\n', '\\n')
#         return formatted_key
# 
#     except FileNotFoundError:
#         print(f"❌ Error: Public key file '{key_path}' not found.")
#         return None


def request_encrypted_seed():
    """Sends a POST request to the instructor API to get the encrypted seed."""
    
    print("1. Using hardcoded student public key...")
    # NOTE: The public key string must use double backslashes (\\n) for the API
    formatted_public_key = "-----BEGIN PUBLIC KEY-----\\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr7TNAcOBI3AmTMIMzdOD\\ntptSH+XrQ0pFWhy6K+B8lbyo56sujBdbcWSzyNBSGb9ENgdfMDjFhVTStqriqmUB\\nvjaMPQHlcTBS6xOYXTcFDtX77L13bDExAJSwojokoEDAVYu4EeTqkg/x0NxjfSsc\\nOld3/unoLyQoMzt4qd+X8YnfLY5q8RrtGOGhOEeCsQOI/cRe6k44cRBQ8V1Zygqx\\nA30VqXJ5rnmZIKnEIdB4SYFSgE8Cs58+Pa0i1ZGFsdAMTHuSUc1zG64xWNMc+dDe\\nk9nG1PsJ3TPMiW2qcrICuzOUKAxteU8fJVEbDPc7Eq2ZUCGv8ejZOtvQz+zju9Ay\\nfH+2OeJ4oCbk8NZLpiT+u84pAjWLvEX24pykJRuXULWYZYBVSQbyVkd2P1GQQm5I\\nkasED96Y7eXTrAdkcnLhiDEsH1/aVpjkxSdj9A8wXOTJIHtR3OXyhQMxYK1QuY5h\\n8IYjBeOwHLIzDGpIJ7erGRZv+yBrehNFI3JE0IYW8HudzyvdaqafCsi330sfuv11\\noUhWSIzV1ZsxJNUcjQkJQQxU8VvH2dtbI3lq7NW06KpfCrffjlgEFUJ7ru59RJic\\nPb8Y6zlBv2F1J6+BQ0dxay8m3c+hb+TqvTGrLqLmzjui1antJI376MivMzXqBJVZ\\nishD2Vz6TI+Gxx/gB3pCQe0CAwEAAQ==\\n-----END PUBLIC KEY-----" 

    # 2. Prepare HTTP POST request payload (JSON body)
    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": formatted_public_key
    }
    
    # Headers specifying we are sending JSON data
    headers = {'Content-Type': 'application/json'}
    
    print(f"2. Sending POST request to API...")
    
    try:
        # 3. Send POST request to Instructor API with timeout
        response = requests.post(INSTRUCTOR_API_URL, headers=headers, data=json.dumps(payload), timeout=15)
        response.raise_for_status() # Check for HTTP error codes

        # 4. Parse JSON response & Extract 'encrypted_seed'
        response_data = response.json()
        encrypted_seed = response_data.get("encrypted_seed")
        status = response_data.get("status")

        if status == "success" and encrypted_seed:
            print("\n✅ SUCCESS! Encrypted seed received.")
            
            # 5. Save encrypted seed to file
            with open(OUTPUT_FILE, "w") as seed_file:
                seed_file.write(encrypted_seed)
            print(f"💾 Encrypted seed saved to '{OUTPUT_FILE}'.")
            
        else:
            print("❌ API failed or returned an unexpected response.")
            print("Response:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ A network or request error occurred: {e}")
            
if __name__ == "__main__":
    request_encrypted_seed()