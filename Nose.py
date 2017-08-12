import sublime
import sublime_plugin
import re


class NoseRunCommand(sublime_plugin.TextCommand):

    @classmethod
    def log(cls, msg, *args):
        if cls.get_cfg('debug', False):
            print("Noseblime: " + (msg % args))

    @classmethod
    def get_cfg(cls, name, default=None):
        config = sublime.load_settings('Noseblime.sublime-settings')
        return config.get(name, default)

    def _get_region_context(self, region):
        def find_above_selector_text(selector, ref_row):
            regions = self.view.find_by_selector(selector)
            for iregion in reversed(regions):
                row, _ = self.view.rowcol(iregion.begin())
                if row <= ref_row:
                    return self.view.substr(iregion)
            return ""

        caret_row, _ = self.view.rowcol(region.begin())
        class_name = find_above_selector_text('entity.name.class.python', caret_row)
        method_name = find_above_selector_text('entity.name.function.python', caret_row)

        if class_name and method_name:
            return "%s:%s.%s" % (self.view.file_name(), class_name, method_name)
        if class_name:
            return "%s:%s" % (self.view.file_name(), class_name)
        return str(self.view.file_name())

    def _get_view_context(self):
        paths = [self._get_region_context(region) for region in self.view.sel()]
        # Remove duplicates
        return list(set(paths))

    def run(self, edit, files=None, dirs=None, force_file=False):
        paths = (files or []) + (dirs or [])
        if not paths:
            # command run from view
            paths = [self.view.file_name()] if force_file else self._get_view_context()

        program = self.get_cfg('program')
        args = self.get_cfg('args') or []
        self.view.window().run_command('exec', {
                'cmd': [program] + args + paths,
                'file_regex': self.get_cfg('result_file_regex'),
                # multiline is not working: 'file_regex': r"(?s)^\s*File \"(.+)\", line ([0-9]+),.*^(\S+:.*)$^",
            })

    def _isTestDirectory(self, path):
        return bool(re.search(self.get_cfg('test_dir_regex'), path))

    def _isTestFile(self, path):
        return bool(re.search(self.get_cfg('test_file_regex'), path))

    def is_visible(self, files=None, dirs=None, **kwargs):
        self.log("is_visible '%s' / '%s' / '%s'", files, dirs, kwargs)
        if not(files or dirs) and self.view.file_name():
            # command run from view
            files = [self.view.file_name()]

        for file in files or []:
            if self._isTestFile(file):
                return True

        for adir in dirs or []:
            if self._isTestDirectory(adir):
                return True

        return False
