# A bot that claims the waifus.

Commands implemented:
* ~echo `message` 
  - Echo command
* ~list 
  - Displays claim list if it exists, else generates a base list
* ~set `[list]`
  - Sets the waifulist
* ~add `waifu`
  - Add waifu to claim list
* \`remove `waifu`
  - Remove waifu from claim list
* ~react `message ID`
  - React on target message IDs


Dependencies: (will upgrade in future)
Python 3.5
- everything else in requirements.txt
- config.py with bot TOKEN in it

In linux
- sudo apt-get install
- sudo apt-get install python3.5
- sudo apt-get install python3-pip
- sudo apt-get install tmux
- pip3 install requirements.txt
- python3 -m pip3 install discord.py==0.16.12
