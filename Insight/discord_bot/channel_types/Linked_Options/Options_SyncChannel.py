from . import options_base
from .. import capRadar, direct_message
import discord
from functools import partial
from sqlalchemy.orm import Session
import asyncio
import InsightExc


class Options_Sync(options_base.Options_Base):
    def __init__(self, insight_channel):
        assert isinstance(insight_channel, capRadar.capRadar)
        super().__init__(insight_channel)
        self.previous_sync_print = ""

    async def InsightOption_addToken(self, message_object: discord.Message):
        """Add new token - Adds a new token for syncing contact information related to pilots, corporations, or alliances."""
        user_channel: direct_message.direct_message = await self.cfeed.channel_manager.get_user_dm(message_object)

        def write_token(token_row):
            db: Session = self.cfeed.service.get_session()
            try:
                __row = tb_discord_tokens(channel_id=self.cfeed.channel_id, token=token_row.token_id)
                db.merge(__row)
                db.commit()
            except Exception as ex:
                print(ex)
                raise InsightExc.Db.DatabaseError
            finally:
                db.close()

        if isinstance(user_channel, direct_message.direct_message):
            await message_object.channel.send(
                "{}\nI opened a direct message with you. Please read it.".format(message_object.author.mention))
            try:
                __token = await user_channel.linked_options.InsightOptionAbstract_addchannel()
                await self.cfeed.discord_client.loop.run_in_executor(None, partial(write_token, __token))
                await self.InsightOption_syncnow(message_object)
            except:
                await message_object.channel.send("No changes were made to the token configuration for this channel")

    async def InsightOption_removeToken(self, message_object: discord.Message):
        """Remove token - Removes a token from the channel along with any synced contacts associated with it."""
        def get_options():
            _options = dOpt.mapper_index_withAdditional(self.cfeed.discord_client, message_object)
            _options.set_main_header(
                "Delete a token from this channel, removing all associated contacts in the blacklist.")
            db: Session = self.cfeed.service.get_session()
            try:
                for token in db.query(tb_discord_tokens).filter(
                        tb_discord_tokens.channel_id == self.cfeed.channel_id).all():
                    _options.add_option(dOpt.option_returns_object(name=str(token), return_object=token))
            except Exception as ex:
                print(ex)
            finally:
                db.close()
            return _options

        __options = await self.cfeed.discord_client.loop.run_in_executor(None, get_options)
        selected_row = await __options()
        await self.delete_row(selected_row)
        await self.InsightOption_syncnow(message_object)

    async def InsightOption_syncnow(self, message_object: discord.Message = None):
        """Force sync - Updates the channel's allies list if you have SSO tokens assigned to it."""

        def sync_contacts(check_modify=False):
            db: Session = self.cfeed.service.get_session()
            return_str = ""
            try:
                __row = db.query(tb_channels).filter(tb_channels.channel_id == self.cfeed.channel_id).one()
                __row.sync_api_contacts(self.cfeed.service)
                db.commit()
                return_str = __row.str_tokens()
                if check_modify:
                    if return_str == self.previous_sync_print:
                        return None
                return return_str
            except Exception as ex:
                print(ex)
                raise InsightExc.Db.DatabaseError
            finally:
                db.close()
                self.previous_sync_print = return_str

        if message_object is not None:
            await self.cfeed.channel_discord_object.send("Syncing ignored ally capRadar contact lists now")
            __resp = await self.cfeed.discord_client.loop.run_in_executor(None, sync_contacts)
        else:
            __resp = await self.cfeed.discord_client.loop.run_in_executor(None, partial(sync_contacts, True))
        if __resp is not None:
            await self.cfeed.channel_discord_object.send(__resp)
        await self.reload(message_object)


from discord_bot import discord_options as dOpt
from database.db_tables import *