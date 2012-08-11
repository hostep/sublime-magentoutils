import sublime, sublime_plugin
import re, os, shutil

class MagentoUtilsCopyToPackageCommand(sublime_plugin.WindowCommand):
    def run(self, paths = []):
        mage_path = MagentoUtilsCopyToPackageCommand.__validMagentoPaths(paths)
        if mage_path is None:
            return False

        for path in paths:
            to_path = MagentoUtilsCopyToPackageCommand.__getToPath(path, mage_path)
            if to_path is not None and not os.path.exists(to_path):
                if os.path.isdir(path):
                    shutil.copytree(path, to_path)
                elif os.path.isfile(path):
                    to_path_dir = os.path.dirname(to_path)
                    if not os.path.exists(to_path_dir):
                        os.makedirs(to_path_dir)
                    shutil.copy(path, to_path)

                print "copied from: " + path + " to: " + to_path

    def is_visible(self, paths = []):
        mage_path = MagentoUtilsCopyToPackageCommand.__validMagentoPaths(paths)
        if mage_path is None:
            return False

        for path in paths:
            to_path = MagentoUtilsCopyToPackageCommand.__getToPath(path, mage_path)

            if to_path is None or os.path.exists(to_path):
                return False

        return True

    @staticmethod
    def __getToPath(path, mage_path):
        package = MagentoUtilsCopyToPackageCommand.__getMagentoPackageFromPath(path, mage_path)
        theme = MagentoUtilsCopyToPackageCommand.__getMagentoThemeFromPath(path, mage_path)

        if package is None or theme is None:
            return None

        custom_package = MagentoUtilsCopyToPackageCommand.__figureOutCustomPackage(path, mage_path)
        custom_theme = 'default' # assume custom theme is always 'default'

        if custom_package is None or custom_theme is None:
            return None

        base_path = MagentoUtilsCopyToPackageCommand.__getBasePath(path, mage_path)
        rel_from_path = MagentoUtilsCopyToPackageCommand.__getRelFromPath(path, mage_path, package, theme)

        if base_path is None or rel_from_path is None:
            return None

        to_path = os.path.join(base_path, mage_path, custom_package, custom_theme, rel_from_path)
        return to_path

    @staticmethod
    def __validMagentoPaths(paths):
        for path in paths:
            if "app/design/frontend/" in path:
                return "app/design/frontend/"
            elif "skin/frontend/" in path:
                return "skin/frontend/"

        return None

    @staticmethod
    def __getMagentoPackageFromPath(path, mage_path):
        matches = re.search('%s([^/]+)/' % mage_path, path)
        if matches is not None:
            return matches.group(1)

        return None

    @staticmethod
    def __getMagentoThemeFromPath(path, mage_path):
        matches = re.search('%s[^/]+/([^/]+)' % mage_path, path)
        if matches is not None:
            return matches.group(1)

        return None

    @staticmethod
    def __figureOutCustomPackage(path, mage_path):
        matches = re.search('(^.+%s).+' % mage_path, path)
        if matches is not None:
            packages_path = matches.group(1)
            if os.path.isdir(packages_path):
                for f in os.listdir(packages_path):
                    if os.path.isdir(os.path.join(packages_path, f)):
                        if f != "base" and f != "default":
                            return f

        return None

    @staticmethod
    def __getBasePath(path, mage_path):
        matches = re.search('(.+)%s' % mage_path, path)
        if matches is not None:
            return matches.group(1)

        return None

    @staticmethod
    def __getRelFromPath(path, mage_path, package, theme):
        package_theme_path = os.path.join(mage_path, package, theme)
        matches = re.search('.+%s/(.+)$' % package_theme_path, path)
        if matches is not None:
            return matches.group(1)

        return None

