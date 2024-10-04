import os
import subprocess
import sys

def run_django_server(host="127.0.0.1", port="8000"):
    try:
        os.chdir("src")

        subprocess.run(['py', 'manage.py', 'runserver', f'{host}:{port}'], check=True)
    except FileNotFoundError:
        print("Error: 'manage.py' not found in 'src' directory.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print(f"\nServer stopped.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        host = sys.argv[1]
        port = sys.argv[2] if len(sys.argv) > 2 else '8000'
    else:
        host = '127.0.0.1'
        port = '8000'

    run_django_server(host, port)    

