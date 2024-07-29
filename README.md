# Obscura - Python Code Obfuscation Tool

**Obscura** is a Python code obfuscation tool designed to protect your source code from reverse engineering and tampering. This is a learning project for me, and while it includes a variety of obfuscation techniques, please note that it may not be as robust as other well-known public methods. Some features are theoretical and may not work as expected.

---

## 🌟 Key Features

### 🛡️ Code Obfuscation Techniques

- **Inline Code Obfuscation**: Replaces inline code with obfuscated code.
- **Control Flow Obfuscation**: Obfuscates the control flow to make it harder to understand the code logic.
- **Control Flow Flattening**: Flattens the control flow to add complexity to the code structure.
- **Function Mirroring**: Creates mirrored functions to add redundancy and confusion.
- **Obfuscate Identifiers**: Obfuscates function, class, and variable names.
- **Obfuscate Constants**: Changes constants to obfuscated forms.
- **Number to Hex Conversion**: Converts numbers to hexadecimal format.
- **Opaque Predicates**: Inserts opaque predicates to make the code harder to analyze.
- **Insert Dummy Variables & Args**: Adds dummy variables and arguments to functions.

### 🔒 Encryption

- **Code Encryption**: Encrypts code with various methods such as AES, Base64, Hybrid (Anti-V), and Hybrid Hash (Custom Method).
- **Inject Anti-Debug**: Adds anti-debugging mechanisms to the encrypted code.
- **Re-Obfuscate Decryption Stub**: Re-obfuscates the decryption stub for added security.

### 📉 Compression

- **Compress Code**: Compresses the obfuscated code to reduce its size and add another layer of obfuscation.
- **Compression Repeats**: Allows multiple compression iterations for increased complexity.

### 🛠️ Project Obfuscation (To be implemented)

- **Folder Obfuscation**: Will allow obfuscation of all .py files in a folder, handling cross-references and dependencies.

---

## 🖼️ Screenshots

<table>
  <tr>
    <td><img src="https://i.imgur.com/KP1vyeN.png" alt="Screenshot1"></td>
    <td><img src="https://i.imgur.com/u4SkNyy.png" alt="Screenshot2"></td>
  </tr>
</table>

---

## Getting Started

1. Clone or download the Obscura repository to your local machine.
2. Ensure you have Python and the required dependencies installed.
3. Run the `main.py` file to launch the obfuscation tool.
4. Use the application to obfuscate your Python files by selecting the desired options.

For detailed usage instructions and troubleshooting, please refer to the repository's documentation.

---

## 🚧 Disclaimer

This project is a work in progress and is intended for learning purposes only. Some features may not work as expected, and the obfuscation techniques may not provide the same level of protection as other well-known methods. Use it at your own risk and do not rely on it for critical security purposes.

---
