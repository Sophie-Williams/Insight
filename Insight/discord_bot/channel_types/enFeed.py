from . import nofeed_text as noCh
from .base_object import *


class enFeed(noCh.discord_text_nofeed_exist):
    def load_table(self):
        super(enFeed, self).load_table()
        self.cached_feed_specific = self.cached_feed_table.object_enFeed

    @classmethod
    def linked_table(cls):
        return dbRow.tb_enfeed

    def linked_visual_base(self):
        return visual_enfeed

    def __str__(self):
        return "Entity Feed"

    @classmethod
    async def create_new(cls,message_object:discord.Message, service_module, discord_client):
        """Entity Feed  - Displays PvP activity for a set of tracked entities. Entities are characters, corporations, or alliances. This feed type is ideal for personal, corporate, alliance, or coalition killboard streaming. """
        await super().create_new(message_object,service_module,discord_client)

    def get_linked_options(self):
        return Linked_Options.opt_enfeed(self)

    @classmethod
    def is_loadable_feed(cls):
        return True

    @classmethod
    def feed_category(cls):
        return 1


from . import Linked_Options