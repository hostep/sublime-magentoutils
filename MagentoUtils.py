# WARNING: this code is probably terrible (I'm a Python illiterate), but it seems to work, and that's what matters :)

import sublime
import sublime_plugin
import re
import os
import shutil


class MagentoUtilsCopyToOtherDirectoryCommand(sublime_plugin.WindowCommand):
    default_copy_paths = {
        'app/code/core/': 'app/code/local/',
        'app/code/community/': 'app/code/local/',
    }
    default_copy_paths_with_guessing = {
        'base/default': '!GUESS_CUSTOM_PACKAGE!/default',
        'default/default': '!GUESS_CUSTOM_PACKAGE!/default',
        'base/default': '!GUESS_CUSTOM_PACKAGE!/default',
        'default/default': '!GUESS_CUSTOM_PACKAGE!/default'
    }

    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)

    def run(self, paths=[]):
        for path in paths:
            to_path = MagentoUtilsCopyToOtherDirectoryCommand.__validateAndGetToPath(path)

            if to_path is not None and not os.path.exists(to_path):
                if os.path.isdir(path):
                    shutil.copytree(path, to_path)
                elif os.path.isfile(path):
                    to_path_dir = os.path.dirname(to_path)
                    if not os.path.exists(to_path_dir):
                        os.makedirs(to_path_dir)
                    shutil.copy(path, to_path)
                    sublime.active_window().open_file(to_path)

                sublime.status_message("[MagentoUtils] Copied ...%s to ...%s" % (path[-50:], to_path[-50:]))

    def is_visible(self, paths=[]):
        for path in paths:
            to_path = MagentoUtilsCopyToOtherDirectoryCommand.__validateAndGetToPath(path)

            if to_path is None or os.path.exists(to_path):
                return False

        return True

    @staticmethod
    def __getCopyPaths():
        if sublime.active_window() and sublime.active_window().active_view() and sublime.active_window().active_view().settings():  # sometimes this isn't working, I don't know why ...
            project_specific_packages = sublime.active_window().active_view().settings().get('magento_utils_packages_to_copy_between', MagentoUtilsCopyToOtherDirectoryCommand.default_copy_paths_with_guessing)
        else:
            project_specific_packages = MagentoUtilsCopyToOtherDirectoryCommand.default_copy_paths_with_guessing

        project_specific_packages_with_prefixes = {}

        for from_path, to_path in project_specific_packages.items():
            # trim slashes on both sides of paths, otherwise there could be trouble further down the line!
            from_path = from_path.strip('/')
            to_path = to_path.strip('/')

            project_specific_packages_with_prefixes["app/design/frontend/%s/" % from_path] = "app/design/frontend/%s/" % to_path
            project_specific_packages_with_prefixes["skin/frontend/%s/" % from_path] = "skin/frontend/%s/" % to_path

        copyPaths = MagentoUtilsCopyToOtherDirectoryCommand.default_copy_paths.copy()
        copyPaths.update(project_specific_packages_with_prefixes)
        return copyPaths

    @staticmethod
    def __validateAndGetToPath(path):
        result = MagentoUtilsCopyToOtherDirectoryCommand.__validMagentoPaths(path)
        if result is None:
            return None

        from_path_rel = result.get('from')
        to_path_rel = result.get('to')

        result = MagentoUtilsCopyToOtherDirectoryCommand.__getBasePathAndRelPath(path, from_path_rel)
        if result is None:
            return None

        base_path = result.get('base')
        path_rel = result.get('rel_path')

        return MagentoUtilsCopyToOtherDirectoryCommand.__getToPath(base_path, to_path_rel, path_rel)

    @staticmethod
    def __getToPath(base_path, to_path_rel, path_rel):
        to_path = os.path.join(base_path, to_path_rel, path_rel)
        if '!GUESS_CUSTOM_PACKAGE!' in to_path:
            custom_package = MagentoUtilsCopyToOtherDirectoryCommand.__guessCustomPackage(base_path)
            to_path = to_path.replace('!GUESS_CUSTOM_PACKAGE!', custom_package)

        return to_path

    @staticmethod
    def __validMagentoPaths(path):
        for from_path, to_path in MagentoUtilsCopyToOtherDirectoryCommand.__getCopyPaths().items():
            if from_path in path:
                return {'from': from_path, 'to': to_path}

        return None

    @staticmethod
    def __guessCustomPackage(base_path):
        base_path = os.path.join(base_path, 'app/design/frontend')
        if os.path.isdir(base_path):
            for f in os.listdir(base_path):
                if os.path.isdir(os.path.join(base_path, f)):
                    if f != 'base' and f != 'default' and f != 'enterprise':
                        return f

        return None

    @staticmethod
    def __getBasePathAndRelPath(path, from_path_rel):
        matches = re.search('(.+)%s(.+)' % from_path_rel, path)
        if matches is not None:
            return {'base': matches.group(1), 'rel_path': matches.group(2)}

        return None
