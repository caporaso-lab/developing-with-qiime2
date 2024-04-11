(add-nw-align-usage)=
# Add usage examples

If you want others to use your new functionality, it isn't *really* done until you document how to use it.
Let's do that now.
This will ensure that users know how to use your code, and it will give them something to try after they install your plugin to convince them that it's working.
I generally find that I'm the first person to benefit from my documentation, and in some cases I'm also the person who most frequently benefits from my documentation (e.g., if it's code that I write for my own purposes, rather than something I intend to broadly disseminate).

QIIME 2 provides a framework for defining *usage examples* for plugins.
Usage examples are defined abstractly, rather than based on a specific QIIME 2 interface, and QIIME 2 interfaces can define *usage drivers* that know how to translate those abstract definitions into instructions for their application through a specific interface.
For example, the framework contains a usage driver for the {term}`Python 3 API`, and therefore can turn abstract usage examples into a series of Python 3 commands.
{term}`q2cli` contains a usage driver that translates abstract usage examples into a series of shell commands.
And [q2galaxy](https://github.com/qiime2/q2galaxy) contains a usage driver that turns examples into text-based instructions for running them through {term}`Galaxy`.
So, by writing a single usage example, your documentatation is targeted toward users with different levels of computational expertise, and as new interfaces become available you don't need to update your usage examples for users to be able to work with your examples through them.
This is one way the framework supports our goal of meeting users where they are in terms of their computational experience, and it's one of the big benefits that you as a plugin developer gets by developing with QIIME 2.

In this section of the tutorial, we'll define a usage example for our `nw-align` action.

(add-usage-example-commit)=
```{admonition} tl;dr
:class: tip
The full code that I developed for this section can be viewed [here](https://github.com/caporaso-lab/q2-dwq2/commit/790c73536a7d0cbf6c4a3f07630c65a79c5d6077).
```

## Defining a usage example for `nw-align`

Usage examples work on actual data that you define when you create the usage example.
This allows users to run your usage examples, explore the input and output, and confirm that things work as expected before they try your plugin on their own data.
This also allows you to have your usage examples automatically tested every time your run your test code, which lets you make and honor a commitment to your users that the documentation you provide will work, because you can automatically run all of the usage examples you define with a single command after every change you make so you'll be the first to know if anything is broken.

So let's start by defining data for use by our `nw-align` usage example.
This is done by creating a function that returns a QIIME 2 artifact that is used as an input in the example.

### Define input data for your usage example

Start by creating a top-level file in your module called `_examples.py`.
Mine will be called `q2-dwq2/q2_dwq2/_examples.py`.
Add the following code, and then we'll work through it.

```python
import tempfile

import skbio

import qiime2

from q2_dwq2 import SingleRecordDNAFASTAFormat


def seq1_factory():
    seq = skbio.DNA("AACCGGTTGGCCAA", metadata={"id": "seq1"})
    return _create_seq_artifact(seq)


def seq2_factory():
    seq = skbio.DNA("AACCGCTGGCGAA", metadata={"id": "seq2"})
    return _create_seq_artifact(seq)


def _create_seq_artifact(seq: skbio.DNA):
    ff = SingleRecordDNAFASTAFormat()
    seq.write(str(ff.path))
    return qiime2.Artifact.import_data("SingleDNASequence", ff)
```

Our goal here is to define two "factory" functions - one for each of `nw-align`'s `SingleDNASequence` inputs - that each return an {term}`artifact of class <artifact class>` `SingleDNASequence`.
These functions will be used when we define our usage example, and because of how usage example definitions work, these functions can't take any parameters as input.
Because both of these functions will do similar work under the hood, I am also creating a helper function that creates a `SingleDNASequence` artifact from an `skbio.DNA` object.
That lets me avoid duplicating code.

The factory functions I defined here are `seq1_factory` and `seq2_factory`.
Each creates an `skbio.DNA` object, and then passes that to my helper function, `_create_seq_artifact`.

````{margin}
```{tip}
The type hint in the `_create_seq_artifact` function definition isn't required, but I like to include it to remind myself how this function works when I come back to it in the future.
It makes my code more self-documenting.
```
````

`_create_seq_artifact` takes an `skbio.DNA` sequence object as input.
Internally, it creates a `SingleRecordDNAFASTAFormat` object which is assigned to the variable `ff` (for *file format*).
Our sequence is written to `ff.path` (i.e., the file format's `path` object, which we cast to a string) using `seq.write`.
In the final step, we use `qiime2.Artifact.import_data`, which allows us to import data in a similar way as if we were calling `qiime tools import` through q2cli (incidentally, `qiime tools import` calls `qiime2.Artifact.import_data`, under the hood).
We provide the artifact class that we want to import into, and the file format (`ff`) that we want to import from, and we get a QIIME 2 artifact back.
That artifact is returned by the helper function, and in turn is returned by the factory function that called it. 🛠️

This may feel like a lot of work to define data to use in an example, but it provides a lot of flexibility in how the usage example you define can ultimately be used.
For example, it allows some *usage drivers* to actually create these inputs (for example, a usage driver that is going to be used to [test the examples](test-usage-examples)), while another usage driver can just act as if they were created but not bother taking the time to actually create them (for example, usage drivers that are [displaying examples in command line help](display-usage-example) text but not executing them).

### Defining the usage example

Next, we define a usage example as a function that takes a `UsageDriver` subclass as input.
We often call the input `use`, by convention, but you can call it anything.
This function starts by instantiating two sequence artifacts using the factory functions that we just defined.
It then defines the relevant action call, which in our case will be to the `dwq2` plugin's `nw_align` action.
It also assigns the inputs, and provides a name for the output.

This usage example is using default parameter values, but you could addionally pass parameters to the action in this usage example, or add a second usage example that does that which you also associate with this action.

The following code in my `q2-dwq2/q2_dwq2/_examples.py` file defines the usage example:

```python
def nw_align_example_1(use):
    seq1 = use.init_artifact('seq1', seq1_factory)
    seq2 = use.init_artifact('seq2', seq2_factory)

    msa, = use.action(
        use.UsageAction(plugin_id='dwq2',
                        action_id='nw_align'),
        use.UsageInputs(seq1=seq1, seq2=seq2),
        use.UsageOutputNames(aligned_sequences='msa'),
    )
```

### Registering the usage example

Finally, we're ready to register the usage example.
For this, we'll go back to the `plugin_setup.py` file.

You should first import the new usage example function by adding the following line to your imports at the top of the file:

```python
from q2_dwq2._examples import nw_align_example_1
```

Then, in the call to `plugin.methods.register_function`, you should add an `examples` parameter, to which you can provide a dictionary mapping example names to usage example functions.
These names (i.e., dictionary keys) will be displayed with the usage example in some interfaces.
To do this, adapt your call to `plugin.methods.register_function` as follows.

```python
plugin.methods.register_function(
    function=nw_align,
    ...
    citations=[citations['Needleman1970']],
    examples={'Align two DNA sequences.': nw_align_example_1}
)
```

That completes the definition and registration of our `nw-align` usage example.

(display-usage-example)=
## Displaying usage examples

In this section we'll work through some user-facing commands that allow you or your users to view your usage examples.
First, and most straight-forward, is to do this through q2cli.
If you call your action with the `--help` parameter, you will now see the usage example at the bottom of the resulting help text.

### Command line interface

```shell
$ qiime dwq2 nw-align --help
Usage: qiime dwq2 nw-align [OPTIONS]

...

Examples:
  # ### example: Align two DNA sequences.
  qiime dwq2 nw-align \
    --i-seq1 seq1.qza \
    --i-seq2 seq2.qza \
    --o-aligned-sequences msa.qza
```

You can test this command by having QIIME 2 write the example data we defined to file using the following q2cli command:

```shell
$ qiime dwq2 nw-align --example-data usage-example-data/
```

After generating the example data, run the usage example as described in the help text providing the example data as input and confirm that it works as expected.

### Python 3 API

As mentioned above, the abstract nature of our usage example definition enables it to be interpreted by different usage drivers, enabling the same example to be presented as it would be used through different interfaces.
Open an `ipython` shell in your development environment, and try the following:

```python
from qiime2.plugins import dwq2, ArtifactAPIUsage

examples = dwq2.actions.nw_align.examples

for example in examples.values():
    use = ArtifactAPIUsage()
    example(use)
    print(use.render())
```

This should display how to run this example through the Python 3 API.
Try it out with the same example data that you generated above (you can use `qiime2.Artifact.load` to load the example files into QIIME 2 artifacts to be provided as input to this call to `nw_align`).

```python
import qiime2.plugins.dwq2.actions as dwq2_actions

msa, = dwq2_actions.nw_align(
    seq1=seq1,
    seq2=seq2,
)
```

(test-usage-examples)=
## Automated testing of usage examples

Finally, it's a good idea to have your usage examples run as part of your test suite, as a way to assess if any future changes you make to your code break the usage examples you defined.
To do this, create a new test file in your `tests` directory.
Mine is called `q2-dwq2/tests/test_examples.py`.
Add the following code to that file:

```python
from qiime2.plugin.testing import TestPluginBase


class UsageExampleTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_examples(self):
        self.execute_examples()
```

Save the file, and run `make test`.
That will now run this additional test, which uses `TestPluginBase.execute_examples` to discover and run all of the usage examples defined in the plugin.
You should see output like the following:

```shell
$ make test

...

===== 15 passed, 25 warnings in 15.06s ======
```

This code tests that the usage examples ran successfully, but importantly it does not test that any output they produce aligns with expected output.
It is possible to additionally check the output of these examples, but that doesn't replace the need for unit tests.
Unit tests tend to be more expressive and useful for testing your plugin's functionality, while automated usage example testing is a good way to assess the validity of your documentation.
If you'd like to learn more about testing specific output that you get from running your usage examples, refer to the [](how-to-write-usage-examples) *How to* guide.

## Writing tutorials

Usage examples provide users with guidelines on the specific commands they can run to use your plugin, but they don't provide a lot of context.
It's a good idea to also write tutorials that describe what your plugin is intended to do, how and why to use it, and how to interpret the results.
Ideally the tutorial also provides a small data set that can be analysed quickly on a modestly powered laptop computer.
I credit a lot of the popularity of QIIME 1 and QIIME 2 to its tutorials and to our support forums.

Writing tutorials is out of scope of this document for now, though we may add a *How to* article in the future that discusses writing and automating testing of tutorials.
As a general recommendation though, I highly recommend writing your tutorials using [Jupyter Book](https://jupyterbook.org), which is what *Developing with QIIME 2* is written with.
It's very feature rich, easily deployed with GitHub Actions, and it makes it straight-forward to create nice looking documentation.
[Diataxis](https://diataxis.fr/) is also great reading material on how your tutorials can be structured, and if you get excited about writing documentation (it's fun!) the [Write the Docs community](https://www.writethedocs.org/) is a group of like-minded folks.

Happy documenting! 📝

## Optional exercise

Add a usage example for your `summarize` visualizer.

```{dropdown} Need some hints?
For your example data, you can use the output generated by the `nw-align` usage example that we created here.
If you export that artifact, you can find the data in the format you'll need to create it in your factory function.
You can also find the artifact class that you'll need to use in your `qiime2.Artifact.import_data` call using the `qiime tools peek` command.
```
