# GitHub Free Achievements 🚀

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/GitHub-API-black.svg" alt="GitHub API">
  <img src="https://img.shields.io/badge/Automation-Achievements-success.svg" alt="Automation">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
  <img src="https://img.shields.io/badge/Maintained-Yes-success.svg" alt="Maintained">
  <img src="https://img.shields.io/badge/Contributions-Welcome-orange.svg" alt="Contributions Welcome">
  <a href="https://github.com/stein-exe/github-free-achievements/stargazers">
    <img src="https://img.shields.io/github/stars/stein-exe/github-free-achievements?style=social" alt="GitHub stars">
  </a>
</p>

Automate common GitHub actions that can help trigger profile achievements using ready-to-run Python scripts.

Repository: **[stein-exe/github-free-achievements](https://github.com/stein-exe/github-free-achievements)**  
Profile: **[github.com/stein-exe](https://github.com/stein-exe)**

⭐ If this project helps you, please **star the repository**:  
➡️ **[Star github-free-achievements](https://github.com/stein-exe/github-free-achievements)**

---

## ✨ What’s Inside

This repo includes:

- `farm_achievements.py` → full automated run for multiple GitHub achievement-related actions
- `prefered.py` → alternate/preferred workflow script for achievement automation

Simple goal: run the script, authenticate with your token, and let it perform configured GitHub actions.

---

## ✅ Requirements

- Python 3.9+ (recommended)
- Internet connection
- GitHub account
- GitHub Personal Access Token (PAT)

Install dependency:

```bash
pip install requests
```

---

## 🔐 Create a GitHub Token (PAT)

1. Open: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token** (classic) or fine-grained token.
3. Add required permissions.

Recommended minimum scopes (classic PAT):
- `repo`
- `read:user`
- `write:discussion` (if discussion actions are used)
- `workflow` (only if your flow needs it)

4. Copy token and keep it safe.

> Never hardcode your token in public files.  
> Revoke token immediately if leaked.

---

## ⚙️ Setup & Run

Clone repository:

```bash
git clone https://github.com/stein-exe/github-free-achievements.git
cd github-free-achievements
```

Run main script:

```bash
python farm_achievements.py
```

Or run alternate script:

```bash
python prefered.py
```

During runtime, script may ask for:
- GitHub token
- Repository name (if needed)

Then it will automatically continue with configured achievement-related actions.

---

## 🧠 How These Files Work (Simple)

### `farm_achievements.py`
- Main automation script.
- Authenticates your GitHub account.
- Uses GitHub REST/GraphQL APIs.
- Creates/updates repository activity (issues, PR flow, merges, reactions, discussions, etc.) based on configured steps.

### `prefered.py`
- Alternative script flow.
- Same core purpose: automate selected GitHub actions for achievements with a different preferred execution style.

---

## 🛡️ Safety Notes

- GitHub API rate limits apply.
- Run responsibly to avoid abuse flags.
- Some achievements can require time and GitHub-side processing delay.
- Use only on accounts and repositories you control.
- Revoke and rotate tokens regularly.

---

## 👨‍💻 Author

**By [STEIN](https://t.me/rejerk)**

- GitHub Profile: [https://github.com/stein-exe](https://github.com/stein-exe)
- GitHub Repo: [https://github.com/stein-exe/github-free-achievements](https://github.com/stein-exe/github-free-achievements)

---

## ⭐ Support

If you like this project, please give it a star and share it with others:

👉 **[Star this repository](https://github.com/stein-exe/github-free-achievements)**
