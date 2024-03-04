# Setup Instructions
1. Create a fork to the repo in your account. Any changes should be done here and send a pull request to merge your changes.
2. Create a new virtual environment using ```python3.9 -m venv <name>```, and activate it using ```source <name>/bin/activate``` (Note that Python 3.9 is required for this to work)

(For Windows Users, activate using `.\<name>\Scripts\active`)

3. Install ```requirements.txt``` using ```pip install -r requirements.txt```
4. Create a ```.env``` file in the same directory as ```requirements.txt```. The contents of this file are in #backend channel of discord. (This file contains sensitive information, hence it is not on GitHub)
5. Run command ```pre-commit install``` in the directory where ```.git``` directory is stored. This configures the git hook. (This is for ensuring that code is well formatted before performing git commit). 
6. After commiting changes, if the code is not well formatted, it gets automatically formatted and you need to commit it once again. 
