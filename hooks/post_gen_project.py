def main():
    print("Cookiecutter done. Setup git and push to github:")
    print("\n")
    print(f"git -C {{ cookiecutter.project_slug }} init")
    print(f"git -C {{ cookiecutter.project_slug }} checkout -b main")
    print(f"git -C {{ cookiecutter.project_slug }} add .")
    print(f"git -C {{ cookiecutter.project_slug }} commit -m 'cookiecutter pudding - initial commit'")
    print(f"git -C {{ cookiecutter.project_slug }} remote add origin git@github.com:{{ cookiecutter.full_name }}/{{ cookiecutter.project_slug }}.git")
    print(f"git -C {{ cookiecutter.project_slug }} push -u origin main")

if __name__ == "__main__":
    main()