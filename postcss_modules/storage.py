import os

from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage

from postcss_modules.handler import Handler
from postcss_modules.utils import get_options, get_transpiler


class PostCSSModulesStorage(StaticFilesStorage):
    """
    Transpiling static files when execute `collectstatic` command
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css_options = get_options()
        self.css_ctx = get_transpiler(self.css_options)

    def _save(self, name, content):
        origin = super()._save(name, content)
        _, file_suffix = os.path.splitext(name)

        if file_suffix not in self.css_options['extensions']:
            return origin

        file = open(self.path(name), 'r+')
        css = Handler(self.css_ctx, self.css_options, f'{settings.STATIC_URL}{name}', file.read()).process()
        file.seek(0)
        file.truncate()
        file.write(css)
        file.close()
        return origin
