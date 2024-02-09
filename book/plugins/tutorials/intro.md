(start-plugin-tutorial)=
# Tutorials: Developing a QIIME 2 Plugin

```{note}
This content is adapted from some notes I (@gregcaporaso) put together as a temporary "5-minute plugin development tutorial".
This will be replaced with a much more comprehensive tutorial on this topic, but using [Diátaxis](https://diataxis.fr/) as a guide:

> It’s natural to want to complete large tranches of work before you publish them, so that you have something substantial to show each time. Avoid this temptation - every step in the right direction is worth publishing immediately. [(source)](https://diataxis.fr/foundations/)

... this is a step in that direction.
```

1. Nick Bokulich’s lab maintains a template QIIME 2 plugin that is a great start for your plugin. You can find this here:
[https://github.com/bokulich-lab/q2-plugin-template](https://github.com/bokulich-lab/q2-plugin-template). There’s a link on that page to “Use this template”. Click that, and GitHub will fork that repository and you can start working on your plugin.
2. To work on the plugin, first install a QIIME 2 development environment (see [](setup-dev-environment)).
3. Then, clone your new plugin repository and run through the steps in [the plugin template README](https://github.com/bokulich-lab/q2-plugin-template/blob/main/README.md). I created [a test plugin](https://github.com/gregcaporaso/q2-this-is-a-test) on 27 July 2023 and confirmed that it all works.
4. Next, add an action. Let's create one that that takes a `FeatureTable[Frequency]` (e.g., a biom file) as input and generates one as output. I created [an action in my test plugin](https://github.com/gregcaporaso/q2-this-is-a-test/blob/894918c4ecfcc936a83031a39404782e4a2a31e1/q2_this_is_a_test/plugin_setup.py) with this signature - all it does is return a copy of the input table. Feel free to copy this into your plugin.
5. Then, run `qiime dev refresh-cache`, and then `qiime --help`. You should see your new plugin in the list of plugins. If you call help on it, you should see your new action.

[This link](https://dev.qiime2.org/latest/actions/methods/) provides more context on adding an action to your plugin.