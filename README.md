# LWG / Anarking Lobby bot
It's a bot that constantly checks LWG website for lobbies(specific or not), and then post them in either in anarking or LWG discord.

## On Start/Join
- [x] On joining guild
  - [x] add server settings if its not in the settings.json file
  - [x] add roles that are in settings.json file and not in the server (aka “ranked”)

## Commands
### Utils
- [x] !hi: [Member] says hi :D
- [x] !purge: delete a channel messages, going back to 2 weeks
- [x] !notifToggle :toggle notifications. Meaning the bot stops or starts giving notifications for maps (for times that some people just want to spam discord with pings, using lwg)
- [x] !roles: displays all roles related with lwg and this bot
- [x] !reset: resets all settings

### Lobby [Admin]
- [x] !lob: [Member] display current active lobbies
- [x] !lob_role: displays roles
- [x] !lob_report: continuously reports Active lobbies 
- [x] !lob_stop: stops !lob_all & !lob_report

### Map Filter [Admin]
- [x] !mapf_view: view all maps you filtered
- [x] !mapf_add: filter a new map
- [x] !mapf_remove: remove a map filter
  - [x] Add role creating / destruction to these commands
- [x] !mapf_att: add thumbnail image and stripe color in the same command
- [x] !mapf_img: edit/add thumbnail image to filter
- [x] !mapf_colour: edit/add stripe color of this filter’s embed
- [x] !mapf_emoji: edit the emoji related with the role
- [x] !mapf_ranked: toggle ranked role existing or not


### Dev [Developer]
- [x] !dev_shutdown: shuts the bot down
- [x] !dev_restart: restarts the bot
- [x] !dev_reload: Reloads cogs and commands for updates 
- [x] !dev_add_server: in case the bot didn't automatically add your server to it’s settings db
- [x] !dev_show_settings: shows the settings of the server


### Test [Admin]
- [x] !gen_lobby: generates a list of lobbies based on input maps
- [x] !gen_ranked: toggles ranked search
