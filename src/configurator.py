# -*- coding: cp1252 -*-

import sys

import src.app.configurator_modules.change_password as password_manager
import src.app.configurator_modules.errorfix as error_fixer
import src.app.configurator_modules.change_settings as settings_manager

def main_menu():
    print("\nBitte waehlen Sie eine Aktion zum Ausfuehren:")
    print("1. Passwort aendern")
    print("2. Einstellungen")
    print("3. Fehlersuche")
    print("4. App zuruecksetzen")
    print("5. Beenden")
        
    choice = input("Geben Sie Ihre Wahl ein (1-5): ").strip()
        
    if choice == "1":
        password_manager.change_password() 
    elif choice == "2":
        settings_manager.change_settings()
        pass
    elif choice == "3":
        error_fixer.fix()
    elif choice == "4":
        error_fixer.hard_reset()
    elif choice == "5":
        print("Programm wird beendet.")
        sys.exit(0)
    else:
        print("Ungueltige Wahl. Bitte erneut versuchen.")

main_menu()