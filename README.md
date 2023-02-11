# Password Tool

![Product Name Screen Shot][screenshot]

Ever wanted to try a CLI base tool for generating and storing passwords?
<br>
Well now you can!
<br>
With the CLI tool you can manage your passwords offline in a terminal.
<br>
Or... you could play around and break the code

<br>

## Why Should You Bother At All?
The passwords, both user password and saved passwords are being encrypted, so there is no way one could just take them and use them


## Getting Started

Let's see what should you need for the project up and running on your local machine.

### Prerequisites

* Python 3.10 or newer
* Pip installed for package management

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/YaroslavMiloslavsky/python_password_management.git
   ```
2. (Optional) Create a virtual python environment
   ```sh
   python -m venv path-to-venv
   ```
3. If you have your venv, activate it
   ```sh
   venv\Scripts\activate
   ```
4. Install requirements from the `requirements.txt`
   ```sh
   pip install -r requirements.txt
   ```
5. Run the tool
   ```sh
   python main.py
   ```
6. If you wish to test the code, from the rood directory run
   ```commandline
   python -m unittest discover -s .\test\ -p 'test_*.py'
   ```


## Usage

You should use it to store passwords...
<br>
Or any information you wish to encrypt


## Roadmap

- Add roadmap
- Add open issues 
- Design a better README file
- Add much more features (in the roadmap)

See the [open issues](https://github.com/YaroslavMiloslavsky/python_password_management/issues) for a full list of proposed features (and known issues).

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

[screenshot]: images/screenshot.png
