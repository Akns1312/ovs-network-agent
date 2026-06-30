# main.py
import os
import sys
from ai_agent import run_agent


def check_api_key():
    if not os.environ.get("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable not set.")
        print("Run: export GROQ_API_KEY=your-key-here")
        sys.exit(1)


def main():
    check_api_key()

    print("╔══════════════════════════════════════╗")
    print("║      OVS Network Agent               ║")
    print("║  Powered by Gemini + Open vSwitch    ║")
    print("╚══════════════════════════════════════╝")
    print("\nType your question or command.")
    print("Examples:")
    print("  - What ports are configured?")
    print("  - Show me the flow rules on br0")
    print("  - Put eth0 on VLAN 100")
    print("  - Bring port eth1 down")
    print("\nType 'quit' to exit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not question:
            continue

        if question.lower() in ("quit", "exit", "q"):
            print("Exiting.")
            break

        answer = run_agent(question)
        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()