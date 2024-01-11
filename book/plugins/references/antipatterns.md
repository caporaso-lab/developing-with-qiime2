# Plugin development anti-patterns

> "An anti-pattern in software engineering, project management, and business processes is a common response to a recurring problem that is usually ineffective and risks being highly counterproductive." [Source: Wikipedia: Anti-patterns (Accessed 11 January 2024; last edited 5 December 2023](https://en.wikipedia.org/wiki/Anti-pattern).

This section documents common anti-patterns that we observe in plugin development.
If you find yourself feeling like you need to apply one of these patterns in your plugin, feel free to reach out in the {{ developer_discussion }}.
We'll help you figure out the right way to achieve your goal.

## Providing input filepaths as parameters

It's not uncommon for new plugin developers to provide paths to inputs using parameter arguments (such as `--p-path-to-my-input`) when defining an `Action`.
This circumvents the need to associate that input with a semantic type and format, which is convenient for the developer, and under some circumstances QIIME 2 will appear to work ok.
This is a bad idea for at least a couple of reasons however.

First, some interfaces (e.g., the QIIME 2 Galaxy interface) won't work correctly.
The user would have to type the path to their input in a text field, rather than being presented with the compatible input artifacts on the Galaxy server or being presented with a file upload box, and they likely won't know what that path is (because it'll be a file stored on the Galaxy server).
Even if the user did know the path, expecting a Python `open` call to work on that path on the web server would be unreliable (e.g., the user that the server is executing jobs as might not have permission to access that path).

Next, and more broadly problematic, the entry for this input in QIIME 2's data provenance would simply be the path that was provided when the action was called.
Unless the plugin is only used in a very controlled environment (and is not intended to be distributed to users who will use it in all kinds of environments), this will result in incomplete data provenance.
There will be no UUID associated with the input (so it couldn't be unambiguously identified), and the entry in provenance will only be meaningful if someone knows how to interpret that path (e.g., what computer the path is relative to) and knows that the file at that location hasn't changed since the action was run.

All data that is provided as input to QIIME 2 `Action(s)` should be in the form of QIIME 2 Artifacts.
This is essential for ensuring that your `Action(s)` will be fully reproducible, and accessible to users with varying levels of computational expertise, which QIIME 2 users have come to expect.
These are two of the key benefits that making your methods accessible through QIIME 2 plugins provides, but the cost is going through the upfront work of associating inputs with semantic types and formats.

## Skipping format validation

To save time (either during development, or at run time) plugin developers will sometimes skip implementation of format validation when they create new formats. For example:

```python
from qiime2.plugin import model

class MyNewFormat(model.TextFileFormat):
    def _validate_(self, level):
        pass
```

This can lead to arbitrary input files being loaded into artifacts, even if they contain some errors or aren't even remotely the right type of data to be associated with a semantic type.
QIIME 2 actions that use an artifact created with this format will assume that validation has already been performed to avoid costly validation processed being applied multiple times to the same data.
Sometimes this will work fine, but sometimes it will crash and burn in the hands of your users.

If a user provides invalid data that passes through one of these validators, in the best case QIIME 2 will crash, and most likely with an obscure error message since the `Action(s)` using the data aren't expecting errors in the data (since it has already gone through validation).
That frustrates users who may walk away with a negative view of your plugin, or a negative view of QIIME 2 as a whole if they are not aware of the differece between QIIME 2 plugins and QIIME 2.
That's bad for everyone.
Consider how often you go back to use software (e.g., a phone app) that you tried and decided was buggy.

It's also possible that the user won't get an error message when they provide invalid data, but instead everything will appear to work correctly but in reality generate meaningless results because the input data was invalid (i.e., garbage in → garbage out).
In this case, failure to validate could lead your user being misled, which can have major repercussions downstream including retracted publications, missed opportunities for scientific discovery, or even clinical misdiagnoses. Users will likely blame you for these outcomes!

If you're skipping validation to save time during development, consider what your goals are for your plugin development effort.
If this is something you'll use only in your own work, and you know the input is going to be valid (e.g., because it's tested elsewhere first), then this may not be a big problem.
However if you're planning to distribute your plugin to users, you'll never know where their data is coming from.
Performing input validation can save you and your users lots of time and frustration.

If you're skipping validation to reduce run time, you should instead consider allowing for different levels of validation, which is built into QIIME 2's format validation process.
You can read about how to use this in [](howto-format-validation-levels).
But be aware that validation that is too minimal can lead to all of the same problems as no validation at all.


