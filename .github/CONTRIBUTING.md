# 🛠️ Contributing to MeowMusic

Thank you for your interest in contributing to **MeowMusic**! Here are the simple guidelines to help you get started.

---

## 🚀 How to Contribute

1. **Fork the Repository**:
   Click the "Fork" button on the top right of the [MeowMusic repository](https://github.com/Kanha-Team/MeowMusic).

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/<your-username>/MeowMusic.git
   cd MeowMusic
   ```

3. **Install Dependencies using uv or pip**:
   ```bash
   pip install uv
   uv sync
   ```

4. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

5. **Code Style & Formatting**:
   We use `black`, `isort`, and `ruff` to keep code clean and formatted:
   ```bash
   uv run black .
   uv run isort .
   uv run ruff check . --fix
   ```

6. **Commit & Push**:
   ```bash
   git commit -m "feat: add amazing new feature"
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**:
   Go to your fork on GitHub and click **"Compare & pull request"**. Describe your changes clearly!

---

## 💬 Community & Help
Need help with development? Join our support group on Telegram: [@MeowClone](https://t.me/MeowClone).
