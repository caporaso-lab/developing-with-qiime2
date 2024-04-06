(plugin-antipatterns)=
# Plugin development anti-patterns

> "An anti-pattern in software engineering, project management, and business processes is a common response to a recurring problem that is usually ineffective and risks being highly counterproductive." [Source: Wikipedia -- Anti-patterns (Accessed 11 January 2024; last edited 5 December 2023)](https://en.wikipedia.org/wiki/Anti-pattern).

This section documents common anti-patterns that we observe in plugin development.
Generally speaking, the things documented on this page lead to plugins that, for the most part, work.
So why avoid them?

The extra work of making your methods accessible through QIIME 2, including things like defining the artifact classes of your inputs and outputs, pays off in that you get things like cross-interface support and [Provenance Replay](https://doi.org/10.1371/journal.pcbi.1011676) for your methods for free.
You don't have to test these things: we promise they'll work (and if they don't there is probably a bug somewhere that is our responsibility to fix - please do let us know).
If you find yourself feeling like you need to apply one of these anti-patterns in your plugin, feel free to reach out through the {{ developer_discussion }}.
We'll help you figure out the QIIME-y way to achieve your goal.

```{warning}
If you adopt the anti-patterns described on this page, the QIIME 2 framework developers explicitly provide no guarantee that your plugins will produce useful, replayable provenance, will be fully accessible (or even minimally functional) across the different interfaces that exist (e.g., Python and R APIs, command line interfaces, and graphical interfaces), or won't fail in other weird ways. We also provide no guarantee that these anti-patterns will continue to work with future versions of the QIIME 2 framework.

If features such as access to your methods through different interfaces or their compatibility with Provenance Replay aren't a priority for your work (e.g., because you are prototyping, or because you have a provenance tracking mechanism external to QIIME 2), the extra effort required to build QIIME 2 plugins may not be worth it.
```

## Providing input or output filepaths as parameters

It's not uncommon for new plugin developers to provide paths to inputs or outputs using `parameter` arguments, rather than `input` or `output` arguments, when defining and registering `Action`. For example:

```python

...

def my_action(feature_table: pd.DataFrame,
              taxonomy: pd.DataFrame,
              an_input_filepath: str,
              an_output_filepath: str) -> pd.DataFrame:
    with open(an_input_filepath) as inf:
        ...

    with open(an_output_filepath, 'w') as outf:
        ...

    # return an empty dataframe as the dummy output
    return pd.DataFrame()

...

plugin.methods.register_function(
    function=my_action,
    inputs={'feature_table': FeatureTable[Frequency],
            'taxonomy': FeatureData[Taxonomy]},
    parameters={'an_input_filepath': Str,
                'an_output_filepath': Str},
    outputs=[('dummy_output', FeatureTable[Frequency])],
    input_descriptions={
        'feature_table': 'The input feature table.',
        'taxonomy': 'The input taxonomy.'},
    parameter_descriptions={
        'an_input_filepath': 'The input text file.',
        'an_output_filepath': 'The path where output should be written.'
        },
    output_descriptions={'dummy_output': 'Ignore me.'},
    name='My cool new action.',
    description=("Apply an operation to a feature table."),
    citations=[]
)
```

This approach circumvents the need to associate `an_input_filepath` and `an_output_filepath` with an artifact class (which may need to be defined, if it's a new type).
This is convenient for the developer, and under some circumstances QIIME 2 will appear to work ok, but it's problematic for at least a couple of reasons.

First, some QIIME 2 interfaces (e.g., web-based interfaces, such as the QIIME 2 Galaxy interface) won't work correctly.
The user would have to type the values for `an_input_filepath` and `an_output_filepath` in text fields, such as `C:\Path\to\my\input.txt` or `/path/to/my/input.txt`, not for example select paths on their system through a file upload/download dialog box, as they would most likely expect when providing files to or receiving files from a web server through their browser.
They likely won't know path to type (it would have to be a file on the web server, since the `Action` only knows that this is a string, not that handling as a filepath is needed), and even if they managed to provide the correct input path, they wouldn't have access to the output that is created through the interface that they're interacting with, because it's just being written somewhere on the web server (which probably wouldn't even be allowed).
Expecting arbitrary paths to the two Python `open` calls in this example to work on the server would be unreliable at best.
In practice, this just won't work.

Next, and more broadly problematic, the entries for `an_input_filepath` and `an_output_filepath` in QIIME 2's data provenance would simply be the paths that were provided when the action was called.
This will result in incomplete data provenance for *all* downstream `Results`.
There will be no UUID associated with `an_input_filepath` and `an_output_filepath` (so the data they contain couldn't be unambiguously identified by QIIME 2).
As a result, the entries in provenance will only be meaningful to provenance consumers (users or machines) that know how to interpret the paths (e.g., what computer the paths are relative to) and are confident that the files at those locations haven't changed since the action was run.

All data that is provided as input to or generated as output from QIIME 2 `Action(s)` should be in the form of QIIME 2 Artifacts.
This is essential for ensuring that workflows using your `Action(s)` will be fully reproducible, and that your plugin will be accessible to users with varying levels of computational expertise.
These are two of the key benefits of making your methods accessible through QIIME 2 plugins, and are expectations of QIIME 2 users.
The cost is going through the upfront work of associating inputs with artifact classes.

(antipattern-skipping-validation)=
## Skipping format validation

To save time (either during development, or at run time) plugin developers will sometimes skip implementation of format validation when they create new formats. For example:

```python
from qiime2.plugin import model

class MyNewFormat(model.TextFileFormat):
    def _validate_(self, level):
        pass
```

This can lead to arbitrary input files being loaded into artifacts, even if they contain some errors or aren't even remotely the right type of data to be associated with an artifact class.
QIIME 2 actions that use an artifact created with this format will assume that validation has already been performed to avoid costly validation processed being applied multiple times to the same data.
Sometimes this will work fine, but sometimes it will crash and burn in the hands of your users.

If a user provides invalid data that passes through one of these validators, in the best case QIIME 2 will crash, and most likely with an obscure error message since the `Action(s)` using the data aren't expecting errors in the data (since it has already gone through validation).
That frustrates users who may walk away with a negative view of your plugin, or a negative view of QIIME 2 as a whole if they are not aware of the differece between QIIME 2 plugins and QIIME 2.
That's bad for everyone.
Consider how often you go back to use software (e.g., a phone app) that you tried and decided was buggy.

It's also possible that the user won't get an error message when they provide invalid data, but instead everything will appear to work correctly but in reality generate meaningless results because the input data was invalid (i.e., garbage in → garbage out).
In this case, failure to validate could lead to your user being misinformed, which can have major repercussions downstream including retracted publications, missed opportunities for scientific discovery, or even clinical misdiagnoses. Users will likely blame you for these outcomes!

If you're skipping validation to save time during development, consider what your goals are for your plugin development effort.
If this is something you'll use only in your own work, and you know the input is going to be valid (e.g., because it's tested elsewhere first), then this may not be a big problem.
However if you're planning to distribute your plugin to users, you'll never know where their data is coming from.
Performing input validation can save you and your users lots of time and frustration.

If you're skipping validation to reduce run time, you should instead consider allowing for different levels of validation, which is built into QIIME 2's format validation process.
You can read about how to use this in [](howto-format-validation-levels).
But be aware that validation that is too minimal can lead to all of the same problems as no validation at all.


