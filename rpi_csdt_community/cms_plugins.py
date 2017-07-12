"""Extend the CMS with menu plugin."""
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _


class MenuPlugin(CMSPluginBase):
    """Creates a plugin that purely follows the templat in menu_plugin."""

    name = _("Menu Plugin")
    render_template = "rpi_csdt_community/menu_plugin.html"


plugin_pool.register_plugin(MenuPlugin)
