def main():
    print("Cookiecutter done. Setup git and push to github:")
    print("\n")
    print(f"cd {{ cookiecutter.project_slug }}")
    print(f"git init")
    print(f"git checkout -b main")
    print(f"git remote add origin git@github.com:{{ cookiecutter.full_name }}/{{ cookiecutter.project_slug }}.git")
    print("git add .")
    print("git commit -m 'init repo'")
    print("git push -u origin main")

if __name__ == "__main__":
    main()