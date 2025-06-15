# main.py
import os
from dotenv import load_dotenv
from assistant import CareerAssistant

def main():
    load_dotenv()
    
    try:
        assistant = CareerAssistant()
        print("Career Assistant Bot initialized successfully!")
        print("\nWelcome to the Career Path Assistant!")
        print("Type 'quit' to exit\n")
        
        while True:
            user_input = input("Tell me about your interests: ")
            
            if user_input.lower() == 'quit':
                print("\nThank you for using Career Path Assistant!")
                break
                
            response = assistant.process(user_input)
            print("\nCareer Suggestions:")
            print(response)
            print("\n" + "-"*50 + "\n")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return

if __name__ == "__main__":
    main() 