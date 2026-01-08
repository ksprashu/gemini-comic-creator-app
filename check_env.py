import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("SUCCESS: GOOGLE_API_KEY found.")
    else:
        print("FAILURE: GOOGLE_API_KEY not found.")

if __name__ == "__main__":
    main()
