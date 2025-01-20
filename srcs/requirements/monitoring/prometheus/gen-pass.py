import sys
import bcrypt

try:
    if len(sys.argv) != 2:
        print("Error: Please provide exactly one password argument", file=sys.stderr)
        sys.exit(1)
    
    password = sys.argv[1]
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(hashed_password.decode('utf-8'))

except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
