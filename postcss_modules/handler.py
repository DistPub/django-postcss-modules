import time

import os

from django.conf import settings

from postcss_modules.utils import get_composes, get_absolute_path, get_file_content


class MaxTimeout(Exception):
    pass


class Handler:
    def __init__(self, ctx, options, path, source):
        self.ctx = ctx
        self.options = options
        self.path = path
        self.source = source

    def process(self):
        self.populate_vfs(self.path, self.source)
        return self.postcss_modules_process(self.path)

    def postcss_modules_process(self, path):
        css = self.ctx.call('postcssModules', path)
        max_time = self.options['max_time'] * 10
        while css is None and max_time:
            css = self.ctx.call('getResult', path)
            if css is not None:
                break
            time.sleep(0.1)
            max_time -= 0.1

        if css is None:
            raise MaxTimeout('transpiling css timeout!')
        return css

    def write_vfs(self, path, source):
        if self.ctx.call('fs.existsSync', path):
            return

        cursor = 0
        while 1:
            try:
                index = path.index('/', cursor + 1)
            except ValueError:
                break

            cursor = index
            sub_dir = path[:index]

            if self.ctx.call('fs.existsSync', sub_dir):
                continue
            self.ctx.call('fs.mkdirSync', sub_dir)

        self.ctx.call('fs.writeFileSync', path, source)

    def populate_vfs(self, path, source):
        self.write_vfs(path, source)
        dir_path, _ = os.path.split(path)
        composes = get_composes(dir_path, source)
        for depend in composes:
            path = get_absolute_path(depend[len(settings.STATIC_URL):])
            if not path:
                continue
            self.populate_vfs(depend, get_file_content(path))
