# Magento Utils plugin for Sublime Text 2

## Provides copying specific files from one directory to another

When right clicking on a file or directory in the sidebar, you will have the option to copy it from one directory to another.
The plugin will first look if you already have a copy at the destination and if it finds one, it won't allow you to copy it anymore as it already exists.

The following directories are considered:

* Files from `app/code/core/...` or `app/code/community/...` to `app/code/local/...`
* Files from `app/design/frontend/{package}/{theme}` to another package/theme combination
* Files from `skin/frontend/{package}/{theme}` to another package/theme combination

You can define the package/theme copying on a per-project base by defining this setting in your .sublime-project file:

```
"settings":
{
    "magento_utils_packages_to_copy_between":
    {
        "base/default": "custom/default",
        "default/default": "custom/default",
        "parent/default": "custom/default"     # Usefull for Magento CE >= 1.9 parent/child theme support
    }
}
```
If there isn't a project setting, the plugin will try to guess your custom package, by looking at the available packages and taking the first one which isn't 'base', 'default' or 'enterprise'.



## Roadmap

I'm considering of adding a feature where you can copy a template from the same source to multiple destinations, and giving you the option to choose which one out of those destinations you want to use, this will allow you to do something like this:

```
"settings":
{
    "magento_utils_packages_to_copy_between":
    {
        "base/default": "custom/default",
        "default/default": "custom/default",
        "base/default": "custom/christmas",
        "default/default": "custom/christmas",
        "custom/default": "custom/christmas"
    }
}
```

## Issues

I noticed a certain issue when sometimes the menu item isn't showing when it should, you can get around by right clicking the file a second time, then it will appear again.  
(For future notice: it has something to do with the fact that the plugin can't get access to the project settings for some strange reason...)
