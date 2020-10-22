from db.models import Reminder


async def addReminder(parameters, channel):
    date = parameters[0]
    name = parameters[1]
    Reminder.objects.create(name=name)
    print("Event : date {} \n name {}\n".format(date, name))


async def delReminder(parameters, channel):
    print("delete event")


async def modReminder(parameters, channel):
    print("modifying event")


async def morsty(parameters, channel):
    await channel.send("""```
               ___
            .-9 9 `\\     Is it
          =(:(::)=  ;       Binary ?
   Who      ||||     \\
     am     ||||      `-.
    I ?    ,\\|\\|         `,
          /                \\    What's life ?
         ;                  `'---.,
         |                         `\\
         ;                     /     |
 Is it   \\                    |      /
 morse ?  )           \\  __,.--\\    /
       .-' \\,..._\\     \\`   .-'  .-'
      `-=``      `:    |   /-/-/`
                   `.__/
```""")


commands = {
    'addreminder': addReminder,
    'delreminder': delReminder,
    'modreminder': modReminder,
    'morsty': morsty,
}


async def execCommand(line, channel):
    parameters = line.split(" ")
    if parameters[0] not in commands.keys():
        await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
        return
    else:
        await commands[parameters[0]](parameters[1:], channel)
