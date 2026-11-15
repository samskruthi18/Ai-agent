
from crew import generate_workspace

def main():

    print("\n===================================")
    print("      AI WORKSPACE GENERATOR")
    print("===================================\n")

    requirement = input("Describe your company and requirements:\n\n")

    if not requirement.strip():
        print("Please enter your requirements.")
        return

    print("\nGenerating your workspace blueprint...\n")

    try:
        result = generate_workspace(requirement)

        print("\n===================================")
        print("       WORKSPACE BLUEPRINT")
        print("===================================\n")

        print(result)

        with open("workspace_blueprint.txt", "w", encoding="utf-8") as file:
            file.write(str(result))

        print("\nBlueprint saved to workspace_blueprint.txt")

    except Exception as error:
        print("\nError generating workspace:")
        print(error)


if __name__ == "__main__":
    main()
