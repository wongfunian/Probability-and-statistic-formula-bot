import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv

#
load_dotenv(find_dotenv())


chapterList = '''
1. Chapter 2 Descriptive Statistics
2. Chapter 3 Probability
3. Chapter 4 Probability Distribution
4. Chapter 5 Estimation and Confidence Interval
5. Chapter 6 Hypothesis Testing
6. Chapter 7 Regression and Correlation
'''

chapterTwoFormulaList = '''
1. Mode
2. Mean
3. Median
4. Sample Standard Deviation, raw data
5. Sample Standard Deviation, grouped data
6. Population Standard Deviation, raw data
7. Population Standard Deviation, grouped data
8. Lower Quartile (Q1)
9. Upper Quartile (Q3)
10. Interquartile Range
11. Quartile Deviation / Semi Quartile
'''

chapterThreeFormulaList = '''
1. Probability of an Event
2. Complement of an Event
3. Addition Rule
4. Mutually Exclusive (互不干涉)
5. Independent Event
6. Dependent Event
7. Conditional Probability
8. Multiplication Rule
9. Bayes Theorem
10. Permutation
11. Combination
'''


triggerKeyword = ["stat", "stats", "formula",
                  "cheatsheet", "statisticformula"]

formulaList = {
    "chapter 2": [
        {
            "imagePath": "chapter 2 Descriptive Statistics/mode.png",
            "description":
            "**Mode**\n- Lm = Lower class limit\n- fm = frequency\n- fa = next class frequency\n- fb = previous class frequency\n- C = class size\n\nps: If class size is not equal, frequency must be replaced by standard frequency"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/mean.png",
            "description": "**Mean**\n- ∑fx = total of the frequency × class mid point\n- ∑f = total frequency"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/median.png",
            "description": "**Median**\n- Lm = Lower class limit\n- Cm = class Size\n- fm = frequency\n- N = total frequency\n- ∑fm-1 = cumulative frequency for median's preceding/previous class"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/sampleRaw-SD.png",
            "description": "**Sample Standard Deviation, raw data**"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/sampleGroup-SD.png",
            "description": "**Sample Standard Deviation, grouped data**"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/populationRaw-SD.png",
            "description": "**Population Standard Deviation, raw data**"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/populationGroup-SD.png",
            "description": "**Population Standard Deviation, grouped data**"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/lowerQuartile.png",
            "description": "**Lower Quartile (Q1)**\n- Lq = Lower class limit\n- Cq = class Size\n- fq = frequency\n- N = total frequency\n- ∑fm-1 = cumulative frequency for Lower Quartile's preceding/previous class"
        },
        {
            "imagePath": "chapter 2 Descriptive Statistics/upperQuartile.png",
            "description": "**Upper Quartile (Q3)**\n- Lq = Lower class limit\n- Cq = class Size\n- fq = frequency\n- N = total frequency\n- ∑fm-1 = cumulative frequency for Upper Quartile's preceding/previous class"
        },
        {
            "imagePath": "",
            "description": "**Interquartile Range**\n- Upper Quartile (Q3) - Lower Quartile (Q1)"
        },
        {
            "imagePath": "",
            "description": "**Quartile Deviation / Semi Quartile**\n- (Upper Quartile (Q3) - Lower Quartile (Q1)) / 2"
        }
    ],
    "chapter 3": [
        {
            "imagePath": "chapter 3 Probability/eventProbability.png",
            "description": "**Probability of and Event**\n- n(A) = total number of outcomes belong to event A\n- n(S) = total number of outcomes for the experiment"
        },
        {
            "imagePath": "chapter 3 Probability/complementEvent.png",
            "description": "**Complement of an Event**\n- P(Ā) denotes the probability of A does not occur"
        },
        {
            "imagePath": "chapter 3 Probability/additionRule.png",
            "description": "**Addition Rule**\n- P(A ∩ B) = P(A and B)\n- P(A ∪ B) = P(A or B)"
        },
        {
            "imagePath": "",
            "description": "**Mutually Exclusive (互不干涉)**\n- Event that cannot occur together\n- P(A ∩ B) = 0, it will not have same element in event A and event B\n- P(A ∪ B) = P(A) + P(B)"
        },
        {
            "imagePath": "chapter 3 Probability/independentEvent.png",
            "description": "**Independent Event**\n- Image above is the formula to check whether is Independent Event or not\n- A does not affect the probability of the occurrence of event B"
        },
        {
            "imagePath": "chapter 3 Probability/dependentEvent.png",
            "description": "*Dependent Event**\n- Image above is the formula to check whether is Dependent Event or not\n- A does affect the probability of the occurrence of event B"
        },
        {
            "imagePath": "chapter 3 Probability/conditionalProbability.png",
            "description": "**Conditional Probability**\n- Probability an Event A will occur given that event B has already occurred\n- denoted by P(A|B)"
        },
        {
            "imagePath": "chapter 3 Probability/multiplicationRule.png",
            "description": "**Multiplication Rule**"
        },
        {
            "imagePath": "chapter 3 Probability/bayesTheorem.png",
            "description": "**Bayes Theorem**"
        },
        {
            "imagePath": "chapter 3 Probability/permutation.png",
            "description": "**Permutation**\n- attention given to order of arrangement\n- sequence is important"
        },
        {
            "imagePath": "chapter 3 Probability/combination.png",
            "description": "**Combination**\n- no attention given to order of arrangement\n- sequence is not important"
        }
    ],
    "chapter 4": [],
    "chapter 5": [],
    "chapter 6": [],
    "chapter 7": []
}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower() in triggerKeyword:
            await message.channel.send(chapterList)

            try:
                def check(m):
                    return m.channel == message.channel and ((m.content.isnumeric() and int(m.content) <= 6) or m.content in triggerKeyword) and m.author == message.author

                msg = await client.wait_for("message", timeout=20.0, check=check)
                if msg.content in triggerKeyword:
                    return
                formulaSelected = []
                # Chapter 2
                if int(msg.content) == 1:
                    formulaSelected = formulaList["chapter 2"]
                    await message.channel.send(chapterTwoFormulaList)

                elif int(msg.content) == 2:
                    formulaSelected = formulaList["chapter 3"]
                    await message.channel.send(chapterThreeFormulaList)

                elif int(msg.content) == 3:
                    formulaSelected = formulaList["chapter 4"]

                elif int(msg.content) == 4:
                    formulaSelected = formulaList["chapter 5"]

                elif int(msg.content) == 5:
                    formulaSelected = formulaList["chapter 6"]

                elif int(msg.content) == 6:
                    formulaSelected = formulaList["chapter 7"]

                try:

                    def check(m):
                        return m.channel == message.channel and ((m.content.isnumeric() and int(m.content) <= len(formulaSelected)) or m.content in triggerKeyword) and m.author == message.author
                    msg = await client.wait_for("message", timeout=20.0, check=check)
                    if msg.content in triggerKeyword:
                        return
                    if formulaSelected[int(msg.content) - 1]["imagePath"] != "":
                        await message.channel.send(file=discord.File(formulaSelected[int(msg.content) - 1]["imagePath"]))
                    if formulaSelected[int(msg.content) - 1]["description"] != "":
                        await message.channel.send(formulaSelected[int(msg.content) - 1]["description"])
                    # formulaSelected[int(msg.content) - 1]
                except asyncio.TimeoutError:
                    await message.channel.send("You have out of time :(")

            except asyncio.TimeoutError:
                await message.channel.send("You have out of time :(")


client = MyClient()
client.run(os.getenv("DISCORD_API_KEY"))
