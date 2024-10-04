import os
import subprocess
import sys

def run_django_command(command):
    os.chdir('src')
    subprocess.run(['py', 'manage.py'] + command.split(), check=True)

def load_available_commands(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def print_available_commands(commands):
    print("Available subcommands:")
    for command in commands:
        print(f"    {command}")

def main():
    available_commands = load_available_commands('commands.txt')

    if len(sys.argv) < 2:
        print('')
        print("Usage: python script.py [subcommand]")
        print_available_commands(available_commands)
        return
    
    subcommand = sys.argv[1]
    
    if subcommand in available_commands:
        try:
            run_django_command(subcommand)
        except FileNotFoundError:
            print("Error: 'manage.py' not found in the 'src' directory.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nServer stopped.\n")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print(f"Unknown subcommand: {subcommand}")
        print_available_commands(available_commands)

if __name__ == '__main__':
    main()
