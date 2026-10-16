import os
import sys

def main_menu():
    while True:
        print("\n=== OCTOPUS 2.0 APPLICATION ===")
        print(" [1] Run Regulators' Companion Audit")
        print(" [2] Run Settlement Cycle")
        print(" [3] Exit")
        choice = input("Select option: ").strip()
        if choice == '1':
            os.system("python regulators_companion_wrapper.py")
        elif choice == '2':
            os.system("python octopus_daemon.py")
        elif choice == '3':
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
