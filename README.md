# 📒 Project Logger  

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-orange.svg)](https://github.com/Vedhija/Project-Logger/issues)  



## 🛠️ Requirements

<p style="font-size:16px; color:darkslategray;">
Before getting started, make sure you have the following:
</p>

- ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
- <span style="color:green;">Git Installed ✅</span>
- <span style="color:orange;">VS Code Recommended 💻</span>


## 📥 Installation

```bash
# Clone this repository
git clone https://github.com/Vedhija/Project-Logger.git
cd Project-Logger

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt


#📜 License & Contributions
I would ❤️ contributions! Feel free to open issues and pull requests. 

#✨ Example Usage
from logger import Logger

log = Logger("app.log")
log.info("Application started")
log.error("Something went wrong!")
