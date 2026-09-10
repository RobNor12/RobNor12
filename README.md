# Credential Generator & Lifecycle Manager

### 📖 Overview
The **Credential Generator** is a secure, command-line administrative utility designed to reduce the manual labor and human error involved in producing and decommissioning standardized credentials for an organization. It enforces strict naming conventions, validates administrative permissions, and manages credential persistence cleanly through local data structures.

---

### 🛠 Technology Used
* **Python** (Core scripting, input validation, and logic flow)
* **Pandas** (Data manipulation and clean CSV persistence)
* **OS / Sys / Random** (File safety checks, system exit handling, and secure ID generation)

---

### 🚀 Key Features
* **Secure Authentication (`auth`)**: Validates administrative access against a localized credential tracking file and implements a compromise-detection check if multiple unexpected password entries are found.
* **Standardized Generation (`gen_credentials`)**: Prompts administrators for names, enforces strict character limits (3–15 characters), extracts initials, and appends a cryptographically randomized 9-digit suffix separated by an underscore (e.g., `rlm_123456789`).
* **Interactive Decommissioning (`remove_credentials`)**: Allows administrators to review existing credentials individually, decide whether to purge or keep them, and gracefully exit or save changes at any point.
* **Robust Input Validation**: Implements strict validation loops on all user prompts to catch unexpected inputs and guide administrators safely.

---

### ⚙️ How to Use

* **Setup:**
  * Install requirements.txt to ensure you have the proper libraries needed to run the program
  * Ensure your "password_file" and "credential_file" are located securely in the programs directory
  
* **Run the Script:**

      Bash
      python cred_generator.py
**Follow the Prompts:** Authenticate with your administrator password, choose whether to generate new credentials, review/manage existing ones, and exit safely. 

---

### MIT License
Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

### Return page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
