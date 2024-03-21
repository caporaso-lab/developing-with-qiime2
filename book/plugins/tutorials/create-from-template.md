(plugin-from-template)=
# Creating your plugin from an existing template

```{note}
This content is adapted from notes I (@gregcaporaso) put together as a temporary “5-minute plugin development tutorial”.
This section will be adapted to build from a [cookiecutter project template](https://cookiecutter.readthedocs.io/en/stable/), replacing many of the manual steps required here.
```

1. Nick Bokulich’s lab maintains a template QIIME 2 plugin that is a great start for your plugin. You can find this here:
[https://github.com/bokulich-lab/q2-plugin-template](https://github.com/bokulich-lab/q2-plugin-template). There’s a link on that page to “Use this template”. Click that, and GitHub will fork that repository and you can start working on your plugin.
1. To work on the plugin, first install a QIIME 2 development environment (see [](setup-dev-environment)).
1. Activate your development environment.
1. Then, clone your new plugin repository and run through the steps in [the plugin template README](https://github.com/bokulich-lab/q2-plugin-template/blob/main/README.md). I created [a test plugin](https://github.com/caporaso-lab/q2-dwq2) on 22 February 2024 and confirmed that it all works. [Here are the changes I made](https://github.com/caporaso-lab/q2-dwq2/pull/1/files) when I did this step (and the [second set of changes I made, when I realized I missed some occurences](https://github.com/caporaso-lab/q2-dwq2/pull/2/files)).
    * Tip: Rename the `q2_plugin_name` directory using `git mv q2_plugin_name <new plugin name>`.
    * Tip: It's easiest to replace `q2-plugin-name`, `q2_plugin_name`, `plugin_name`, and `plugin-name` in the files using a global search/replace - there are many occurences.
1. From the top-level directiory of your plugin repository, install your plugin in developer mode by running `pip install -e .`.
1. To confirm that your plugin is now available, run `qiime info`. You should see your new plugin in the list of available plugins. (If you get an error that says something like `ModuleNotFoundError: No module named 'q2_plugin_name'`, you didn't replace all instances of `q2_plugin_name` in the template repository.)
1. Next, add an action. Let's create one that that takes a `FeatureTable[Frequency]` (i.e., a feature table with count data) as input and generates one as output. I created [an action in my test plugin](https://github.com/caporaso-lab/q2-dwq2/blob/e8fe1e5b32bfc2a331d48611b3a70b0fa5b19165/q2_dwq2/plugin_setup.py) with this signature - all it does is return a copy of the input table. Copy this into your plugin.
1. Then, run `qiime dev refresh-cache`, and then `qiime --help`. You should see your new plugin in the list of plugins. If you call help on it, you should see your new action. You should be able to run the `duplicate-table` action in your plugin as you can for any other QIIME 2 plugin.

Next, we'll [add a first (real) action to our plugin](add-nw-align-method).