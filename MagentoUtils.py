import sublime_plugin
import re
import os
import shutil


class MagentoUtilsCopyToPackageCommand(sublime_plugin.WindowCommand):
    copy_paths = {
                    'app/code/core/': 'app/code/local/',
                    'app/code/community/': 'app/code/local/',
                    'app/design/adminhtml/default/default/': 'app/design/adminhtml/default/!CUSTOM_PACKAGE!/',
                    'app/design/frontend/base/': 'app/design/frontend/!CUSTOM_PACKAGE!/',
                    'app/design/frontend/default/': 'app/design/frontend/!CUSTOM_PACKAGE!/',
                    'skin/adminhtml/default/default/': 'skin/adminhtml/default/!CUSTOM_PACKAGE!/',
                    'skin/frontend/base/': 'skin/frontend/!CUSTOM_PACKAGE!/',
                    'skin/frontend/default/': 'skin/frontend/!CUSTOM_PACKAGE!/'
                 }

    def run(self, paths=[]):
        for path in paths:
            to_path = MagentoUtilsCopyToPackageCommand.__validateAndGetToPath(path)

            if to_path is not None and not os.path.exists(to_path):
                if os.path.isdir(path):
                    shutil.copytree(path, to_path)
                elif os.path.isfile(path):
                    to_path_dir = os.path.dirname(to_path)
                    if not os.path.exists(to_path_dir):
                        os.makedirs(to_path_dir)
                    shutil.copy(path, to_path)

                print "copied from: " + path + " to: " + to_path

    def is_visible(self, paths=[]):
        for path in paths:
            to_path = MagentoUtilsCopyToPackageCommand.__validateAndGetToPath(path)

            if to_path is None or os.path.exists(to_path):
                return False

        return True

    @staticmethod
    def __validateAndGetToPath(path):
        result = MagentoUtilsCopyToPackageCommand.__validMagentoPaths(path)
        if result is None:
            return None

        from_path_rel = result.get('from')
        to_path_rel = result.get('to')

        result = MagentoUtilsCopyToPackageCommand.__getBasePathAndRelPath(path, from_path_rel)
        if result is None:
            return None

        base_path = result.get('base')
        path_rel = result.get('rel_path')

        return MagentoUtilsCopyToPackageCommand.__getToPath(base_path, to_path_rel, path_rel)

    @staticmethod
    def __getToPath(base_path, to_path_rel, path_rel):
        to_path = os.path.join(base_path, to_path_rel, path_rel)
        if '!CUSTOM_PACKAGE!' in to_path:
            custom_package = MagentoUtilsCopyToPackageCommand.__figureOutCustomPackage(base_path)
            to_path = to_path.replace('!CUSTOM_PACKAGE!', custom_package)

        return to_path

    @staticmethod
    def __validMagentoPaths(path):
        for from_path, to_path in MagentoUtilsCopyToPackageCommand.copy_paths.items():
            if from_path in path:
                return {'from': from_path, 'to': to_path}

        return None

    @staticmethod
    def __figureOutCustomPackage(base_path):
        base_path = os.path.join(base_path, 'app/design/frontend')
        if os.path.isdir(base_path):
            for f in os.listdir(base_path):
                if os.path.isdir(os.path.join(base_path, f)):
                    if f != 'base' and f != 'default':
                        return f

        return None

    @staticmethod
    def __getBasePathAndRelPath(path, from_path_rel):
        matches = re.search('(.+)%s(.+)' % from_path_rel, path)
        if matches is not None:
            return {'base': matches.group(1), 'rel_path': matches.group(2)}

        return None
