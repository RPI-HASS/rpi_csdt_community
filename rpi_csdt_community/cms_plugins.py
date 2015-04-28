from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from djangocms_picture.cms_plugins import PicturePlugin
from django.utils.translation import ugettext_lazy as _

class MenuPlugin(CMSPluginBase):
    name = _("Menu Plugin")
    render_template = "rpi_csdt_community/menu_plugin.html"


plugin_pool.register_plugin(MenuPlugin)
