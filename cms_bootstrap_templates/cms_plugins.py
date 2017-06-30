from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from djangocms_picture.cms_plugins import PicturePlugin
from django.utils.translation import ugettext_lazy as _

class JumbotronPlugin(TextPlugin):
    name = _("Bootstrap Jumbotron")
    render_template = "cms_bootstrap_templates/jumbotron.html"

class PageheaderPlugin(TextPlugin):
    name = _("Bootstrap Page Header")
    render_template = "cms_bootstrap_templates/pageheader.html"

class AlertPlugin(TextPlugin):
    """TODO: This should be made to provide an option of several alerts
    """
    name = _("Bootstrap Alert")
    render_template = "cms_bootstrap_templates/alert.html"

class PanelPlugin(TextPlugin):
    name = _("Bootstrap Panel")
    render_template = "cms_bootstrap_templates/panel.html"

class WellPlugin(TextPlugin):
    name = _("Bootstrap Well")
    render_template = "cms_bootstrap_templates/well.html"

class ImagePlugin(PicturePlugin):
    name = _("Bootstrap Image")
    render_template = "cms_bootstrap_templates/image.html"

plugin_pool.register_plugin(JumbotronPlugin)
plugin_pool.register_plugin(PageheaderPlugin)
plugin_pool.register_plugin(AlertPlugin)
plugin_pool.register_plugin(PanelPlugin)
plugin_pool.register_plugin(WellPlugin)
plugin_pool.register_plugin(ImagePlugin)
