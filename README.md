# RuneScape Archaeology Artifact Calculator

The calculator takes an input of an artifact name and how many of that artifact then it returns the amount of each material, total cost of each material, total cost of materials in gp, total experience with and without full archaeology outfit, and experience of each artifact. This calculator comes in two versions: script version and discord bot command version.

This project is to help me learn Python and what a fun way to do so is to make this calculator.

## How to use:
### Script Version:
- Make sure to have Python 3 and the following python libraries installed: requests, beautifulsoup4, and tabulate.
- In the terminal, change directories to the "ScriptVersion" folder.
- Run the ArchCalcScript.py file by typing "python3 ArchCalcScript.py" without the quotations in the terminal. 

### Discord Bot Version:
- Make sure to have Python 3 and the following python libraries installed: discord, requests, and beautifulsoup4.
- Must have created/own a discord bot in a discord server.
- If already have a bot with other commands:
  1. Copy and paste the "rs_arch.py" file into your cogs folder then add 'cogs.rs_arch' into your extensions list in your main bot file.
  2. Run your bot and type the command !calc or whatever command the calculator is set to into your discord server chat.
- If only have empty bot with no commands:
  1. In the terminal, change directories to the "DiscordBotVersion" folder.
  2. Open the "ArchCalcDiscordBot.py" file without the quotations in a text editor and insert your bot login token into client.run('your token here').
  3. Run the ArchCalcDiscordBot.py file by typing "python3 ArchCalcDiscordBot.py" without the quotations in the terminal to run the bot.
  4. Once the bot is online, type the command !calc or whatever command the calculator is set to into your discord server chat.

For non-RuneScape players, RuneScape is a Massive Multiplayer Online Role Playing Game (MMORPG) created by Jagex. RuneScape has a skill called Archaeology where players excavate various hotspots to obtain damaged artifacts and materials to gain experient points. Players restore the damaged artifacts with the materials either gathered or bought from a trading post called the Grand Exchange (GE) to gain more experience points. This calculator prompts the user to enter an artifact and how many then displays the total cost of materials if the player chooses to buy the materials from the GE, total experience points gained from restoring the artifacts, and material information such as the name, amount, and price of each material. 

The U.S. spelling is "Artifact" while the U.K spelling is "Artefact". Jagex is based in the U.K, so "Artefact" is used in RuneScape.
