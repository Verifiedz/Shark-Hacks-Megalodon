from nextcord.ext import commands
import json, random, datetime, asyncio
from nextcord import Embed, ButtonStyle
from nextcord.ui import Button, View
from twilio.rest import Client
import keys
import discord
from discord.ext import commands

links = json.load(open("gym.json"))
helpgui = json.load(open("help.json"))

bot = commands.Bot(command_prefix="!",intents = discord.Intents.all())
bot.remove_command("help")


def createHelpEmbed(pageNum=0, inline=False):
    pageNum = pageNum % len(list(helpgui))
    pageTitle = list(helpgui)[pageNum]
    embed=Embed(color=0x0080ff, title=pageTitle)
    for key, val in helpgui[pageTitle].items():
        embed.add_field(name=bot.command_prefix+key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpgui))}")
    return embed


@bot.command(name="help")
async def Help(ctx):
    currentPage = 0

    async def next_callback(interaction):
        nonlocal currentPage, send_msg
        currentPage += 1
        await send_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    async def prev_callback(interaction):
        nonlocal currentPage, send_msg
        currentPage -= 1
        await send_msg.edit(embed=createHelpEmbed(pageNum=currentPage), view=myview)

    nextButton = Button(label=">", style=ButtonStyle.blurple)
    nextButton.callback = next_callback
    prevButton = Button(label="<", style=ButtonStyle.blurple)
    prevButton.callback = prev_callback


    myview = View(timeout=180)
    myview.add_item(prevButton)
    myview.add_item(nextButton)
    send_msg = await ctx.send(embed=createHelpEmbed(), view=myview)

@bot.command(name="test")
async def SendMessage(ctx):
    await ctx.send('test back nig')

@bot.command(name="pushvid")
async def PushWorkoutVideo(ctx):
    await ctx.send(random.choice(links["pushworkout"]))

@bot.command(name="pullvid")
async def PullWorkoutVideo(ctx):
    await ctx.send(random.choice(links["pullworkout"]))

@bot.command(name="legsvid")
async def LegsWorkoutVideo(ctx):
    await ctx.send(random.choice(links["legsworkout"]))

@bot.command(name="homevid")
async def HomeWorkoutVideo(ctx):
    await ctx.send(random.choice(links["homeworkout"]))



async def schedule_daily_message(h, m, s, channelid):
    while True:
        now = datetime.datetime.now()
        # then = now+datetime.timedelta(days=1)
        then = now.replace(hour=h, minute=m, second=s)
        if then < now:
            then += datetime.timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = bot.get_channel(channelid)

        client = Client(keys.account_SID, keys.token)
        message = client.messages.create(
            body=random.choice(links["pullworkout"]),
            from_=keys.number,
            to="phonenumber"
            )
        await asyncio.sleep(1) 



@bot.command(name="routine")

async def daily(ctx, hour:int, minute:int, second:int):
    print(hour, minute, second)

    if not (0 <= hour < 24 and 0 <= minute <= 60 and 0 <= second < 60):
        raise commands.BadArgument()

    time = datetime.time(hour, minute, second)
    timestr = time.strftime("%I:%M:%S %p")
    await ctx.send(f"A daily message will be sent at {timestr} everyday in this channel. \nDaily message:\"\"Confirm by simply saying 'yes'")
    try:
        msg = await bot.wait_for("message", timeout=60, check=lambda message: message.author == ctx.author)
    except asyncio.TimeoutError:
        await ctx.send("Your Taking to Long")
        return
    
    if msg.content == "yes":
        await ctx.send("Daily message is now starting")
        await schedule_daily_message(hour, minute, second, ctx.channel.id)
    else:
        await ctx.send("Cancelled")
        

@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("""Use the command this way: '!routine  [hour minute second]'.""")


# Step one if user inputs M.BMI 
# it should return them the user BMI based on previous inputs 
# in order for us to do this we need to create an input "height" and "weight" for the user

@bot.command(name="BMI")    #BMI refers to Biometics of the user 
async def BMI(ctx, height:int, weight: int): # in cm & kg 
    BMI =weight/(height/100)**2
    RoundBMI= round(BMI, 2)
    embed=Embed(color=0x9FE2BF, title="BMI Calculator")
    await ctx.send(f"Your BMI is:" + str(RoundBMI))

    # Now we need the bot to return the classfication for the BMI 
    if BMI <= 18.4: 
        await ctx.send(f"Currently: UnderWeight")
    elif BMI <= 24.9: 
        await ctx.send(f"Currently: Healthy")
    elif BMI <= 29.9: 
        await ctx.send(f"Currently: overweight")
    elif BMI <= 34.9: 
        await ctx.send(f"Currently: severly over weight")
    elif BMI <= 39.9: 
        await ctx.send(f"Currently: obese")   
    else: 
        await ctx.send(f"Just give up at this point")

 #inputing Command to Bot by creating an event 
 # This command request the bot to display the BMI chart, if user is unaware of what BMI is
@bot.command(name="BMIchart")
async def Chart(ctx):
    await ctx.send("https://www.ncbi.nlm.nih.gov/books/NBK535456/bin/bmi__WHO.jpg")
# The next command is to estimate the macros for Protien, Carbs and, Fat intake
# This is based of the persons body weight 
# we can set up a def, then have an equation, for our parameters 
@bot.command(name="Mchart")
async def Chart(ctx): 
    await ctx.send("The following is a general approximation for each body goal.")
    await ctx.send("https://mealpreponfleek.com/wp-content/uploads/2017/02/Macros-diet-calculator-official2.jpg")
    # Very simple Information reminder: 
@bot.command(name="MacroInfo")
async def info(ctx): 
    await ctx.send("You want to learn about Macros? Well Macros is the proceess of tracking the amount of macronutrients you intake, primarly tracking the amount of Protein, fat, and Carbohydrates you consume")
    await ctx.send("The calculation which can be done by m.Macrocalc will assess the amount of grams of each macronutrients you need to acheive your optimal body.")
    await ctx.send("Generally you seek to recieve optimal muscle growth, which for both losing and gaining weight means a higher intake of Protein, and lower percentage of Carbs and fat(the optimal amount)")
    await ctx.send("the calculator will take in your age followed by height(cm) and weight(Ib) and gender respectivally, and will import you the amount of each macronutrients you need.")
    #Calculates the Macros based on the weight and Gender of the Individual
@bot.command(name="Macrocalc")
async def Calc(ctx, weight:int,Gender:str):
    weight =weight 
    Male= 'Male'
    Female ='Female'
    if Gender == Male: 
        await ctx.send(f"Your Macros are: " + "Protein:" +str(1*weight)+"|" +""+"Fat:"+str(0.4*weight)+ "|""Carbs:"+str(0.8*weight))
    elif Gender == Female: 
        await ctx.send(f"Your Macros are: " + "Protein:" +str(0.8*weight)+"|"+"Fat:"+str(0.3*weight)+ "|""Carbs:"+str(0.8*weight))
    else: 
        return print("wrong input:")

@bot.command(name="BMR")
async def BMR(ctx,H:int, W:int, A:int, Gen:str, AL:str):
    if Gen == "Male":
        BMR = 66.5 + (13.75*W) + (5.003*H) - (6.75*A)
    elif Gen == "Woman":
        BMR = 665.1 + (9.563*W) + (1.850*H) - (4.676*A)
    if AL == "Notactive":
        cal = 1.2*BMR
    elif AL == "lightactive":
        cal = 1.375*BMR
    elif AL == "Modactive":
        cal = 1.55*BMR
    elif AL == "Veryactive":
        cal = 1.725*BMR
    elif AL == "Extraactive":
        cal = 1.9*BMR
    
    await ctx.send("Your Basal Metabolic Rate is " +str("%.2f"%BMR) + "\n" + "Fat!!!")
    await ctx.send("You need " +str("%.2f"%cal) + " Calories")

@bot.command(name="Foods")
async def Food(ctx,W:str):

    if W == "Lose":
        await ctx.send("To lose weight, focus on eating low calorie foods. These consist of the following. In order to acheive weight loss, your calorie intake must be lower than the amount burned. ")
        await ctx.send(" Eating such low calorie, high statiating foods helps with ths as these foods keep you statiated and full throughout the day whilst mainting a caloric deficit.")
        await ctx.send("https://i.pinimg.com/736x/57/47/62/574762c326fc88825a794b9bdfc21fc2.jpg")
        await ctx.send("Some foods consist of 'Sneaky Calories' which are low statiating and are given a healthy attributes but result in increased weight gain due to high number of calories:")
        await ctx.send("Some of these foods consist of the following: ")
        await ctx.send("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXtrem3wOBG1g_vzaPyQNCNjveOTayVcQSsIMTug1GVZLgQlwPf0biMifP4T8JZruiJ0M&usqp=CAU")
    if W == "Gain":
        await ctx.send("To Gain weight, focus on eating high calorie foods. These consist of the following. For weight gain to be acheived, a person must be in a caloric surplus which means to consume more calories than beign burend")
        await ctx.send("https://healthyfamilyproject.com/wp-content/uploads/2022/05/High-Calorie-Foods-Underweight-Kids.jpg")
        await ctx.send("When gaining weight, eating low statiating, high calorie foods are helpful. This allows a person to not feel too full, whilst mainting a calorie surplus")

@bot.command(name="memes")
async def SharkMemes(ctx):
    await ctx.send(random.choice(links["SharkMemes"])) 

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # await schedule_daily_message()

if __name__ == '__main__':
    bot.run("Token")
