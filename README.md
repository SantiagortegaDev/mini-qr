# Mini Qr
A simple **discord bot** and **api** to generate qr code in ascii

## Discord Bot
A simple command to generate a qr and show it in a modal

Invite Bot: https://discord.com/oauth2/authorize?client_id=1550911077712142336

- **/qr** [content] (invert)
- **/api** send the api docs

for deafult this is the qr style but if you invert it you get the classic qr code with a white background

> [!NOTE]
> The Qr has a limit of characters to not convulse and be unscaneable

![screenshot](assets/qr_repo.png)

## Api
why not made a api? it's simple just like the discord bot

**GET** 'https://miniqr.santiagortega.dev/api/v1/qr?content=hello!'

![screenshot](assets/hello_qr.png) 


- **content**: str *
- **invert**: bool = False
- **raw**: bool = False (it return the qr in a json response)
- **long**: bool = False (it bypass the discord bot character limit)

## Invert
here is a screenshot of the invert (clasical) version of the qr code

![screenshot](assets/invert_qr.png)

## IA?
only for debug, i have already work with the discord api and make a lot of discord bots (privates)