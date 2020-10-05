import discord
from discord.ext import commands, menus
from referral_cog import Confirm
import dbobj,os
from util_classes import database

class debug(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.is_owner()
  @commands.command(name="clear-referral",aliases=['cr'],help="Usable only by bot owner for debug purposes.")
  async def clear_referral_cmd(self,ctx,user:discord.User=None):
    if(user == None):
      await ctx.send("You must tag a user!")
      return
    existing_user = database.select_one(dbobj.user_link, source=user.id)
    if(existing_user != None and existing_user != []):
      existing_user = existing_user[1]
      user_obj = self.bot.get_user(existing_user)
      confirm = await Confirm("Are you sure you want to clear the record for **" + user.name + "#" + user.discriminator + "** who declared themselves as referred by **" + user_obj.name + "#" + user_obj.discriminator + "**?  (this will lower the referrer's score)").prompt(ctx)
      if confirm:
        statement = "DELETE FROM user_link WHERE source = %s"
        data = (user.id,)
        decreasing_score = database.select_one(dbobj.scores, user_id=user_obj.id)[1]
        data_2 = (decreasing_score-1,user_obj.id)
        #database.delete_data(statement,data)
        database.test_delete(dbobj.user_link,source=user.id)
        database.update_data(dbobj.scores,data_2)
      else:
        await ctx.send("Process canceled.")
        return
    else:
      await ctx.send("That user has not declared anyone as their referrer yet!")

  @commands.is_owner()
  @commands.command(name="webhook-test",aliases=['wt'],help="Send a webhook message in this channel if such a webhook exists.")
  async def webhook_test_cmd(self,ctx,*,msg):
    wh = await ctx.channel.webhooks()
    if wh == []:
      await ctx.send("No webhooks in this channel!")
    else:
      await ctx.message.delete()
      await wh[0].send(msg)
