from .visual_capradar import *


class VisualCapRadarCompact(visual_capradar):
    def make_text_heading(self):
        self.message_txt = "{}".format(self.mention_method())

    def make_header(self):
        if self.km.str_location_name(name_only=True):
            loc_str = " near **[{}]({}).**".format(self.km.str_location_name(name_only=True),
                                                   self.baseSystem.str_jmp_titan(self.system))
        else:
            loc_str = " in **[{}]({}).**".format(self.system.str_system_name(),
                                                 self.baseSystem.str_jmp_titan(self.system))
        autHead = "{tC} of {tI} in tracked ships".format(tC=str(len(self.tracked_hostiles)),
                                                         tI=self.km.str_total_involved())
        self.embed.set_author(name=autHead, url=self.km.str_zk_link(), icon_url=self.hv.str_highest_image(64))
        e_desc = '**[{haP}]({haP_l})({haAfi})** in a **{haS}**{loc}'.format(haP=self.hv.str_pilot_name(),
                                                                            haP_l=self.hv.str_pilot_zk(),
                                                                            haAfi=self.hv.str_highest_name(),
                                                                            haS=self.hv.str_ship_name(), loc=loc_str)
        self.embed.description = e_desc
        self.embed.title = "{haS} destroyed a {viS} in {sysReg}".format(haS=self.hv.str_ship_name(),
                                                                        viS=self.vi.str_ship_name(),
                                                                        sysReg=str(self.system))
        self.embed.set_thumbnail(url=self.hv.str_ship_image(64))

    def make_body(self):
        pass

    @classmethod
    def appearance_id(cls):
        return 3

    @classmethod
    def get_desc(cls):
        return "Compact - Highest valued attacker ship/affiliation, system/location details, and supercarrier/titan" \
               " generated Dotlan route from base system. Size: Small"
