# Add a first Pipeline

In this chapter we'll add our first {term}`Pipeline` to our plugin.
Pipelines allow developers to define workflows composed of Methods and Visualizers that can be run as a single step.
Pipelines are a type of {term}`Action` in QIIME 2, like {term}`Methods <Method>` and {term}`Visualizers <Visualizer>`, but they differ in a few ways.

* Unlike Methods, which exclusively produce one or more {term}`Artifacts <Artifact>` as output, or Visualizers, which exclusively produce one or more {term}`Visualizations <Visualization>` as output, Pipelines create one or more Artifacts *and/or* Visualizations as output.
* To support calling other Actions from within a Pipeline, the function that is registered as a Pipeline takes `qiime2.Artifact` objects as input.
  This is different than functions registered as Methods and Visualizers which take more typical Python objects as input (e.g., `skbio.DNA` or `pandas.DataFrame`).
* Also in support of calling other Actions from within a Pipeline, functions registered as Pipelines need to interact with a {term}`deployment's <Deployment>` {term}`Plugin Manager`, while the functions registered as `Methods` and `Visualizers` never interact with a Plugin Manager directly.
 Functions registered as Pipelines do this by taking an object that enables this communication, called `ctx` (short for *context*) by convention, as their first argument.
* Pipelines provide formal support for parallel computing, unlike Methods or Visualizers which can only provide access to parallel computing support that they define (such as providing access to multi-threaded execution of external applications that they run).
 As a result, Pipelines are critical for supporting workflows that are computationally expensive in QIIME 2.

In this section, we'll develop our first simple Pipeline which will chain the `nw-align` and `summarize-alignment` {term}`Actions <Action>` that we previously wrote together in a new action that produces the alignment and the alignment summary from one command call.
This will illustrate how to use Pipelines to simplify common workflows for your users.
In subsequent sections of the tutorial, we'll explore developing Pipelines that provide parallel computing support across diverse high-performance computing resource configurations.

(add-pipeline-commit)=
```{admonition} tl;dr
:class: tip

The complete code that I developed for this section is available here: {{ dwq2_add_pipeline_commit_url }}.
```

```{note}
Starting with this section, there will be some steps that are required of you that are not described fully in the text, to provide ways to begin applying what you've learned.
These are required in that the section of the tutorial you're working on may not work entirely, or may be incomplete for another reason, until they're completed.
If you've been doing the *Optional Exercises* at the ends of the sections that have them, these should be straight-forward.
For all of these *Required Exercises*, a link that provides a possible solution will be provided so if you get stuck that doesn't prevent you from moving on with the tutorial.
```

## Update the `nw_align` action to avoid duplicating information

The first thing we're going to do in preparation for building this Pipeline is create an object to store the default parameter settings for our `nw_align` function.
While not technically required, we'll use those same default settings again in our Pipeline, so we do this to adhere to the **D**on't **R**epeat **Y**ourself (**DRY**) principle of software engineering.
This is stated in *The Pragmatic Programmer* {cite}`pragprog20` as *Every piece of knowledge must have a single, unambiguous, authoritative representation within a system*, and the authors go on to say that this is *one of the most important tools in the Pragmatic Programmer's tool box*.

A bit of the reasoning behind DRY, using our code as an example, is that if default parameter settings for our pairwise alignment functionality are defined in two different places, and we want to change those settings, it's very easy to for us (or someone else maintaining this code in the future) to erroneously make the change in only one of the two places where they are defined.
This would result in different output when calling `nw_align` directly versus through our new Pipeline, which would be unexpected behavior that most people would rightly consider to be a bug.

We'll address this by putting the default parameter settings in a `dict`.
We can then look up the values in that `dict` anywhere we need them, so they only need to be defined that one time.
To achieve this, update the `_methods.py` file, to look like the following:

```python
from skbio.alignment import global_pairwise_align_nucleotide, TabularMSA
from skbio import DNA

_nw_align_defaults = {
    'gap_open_penalty': 5,
    'gap_extend_penalty': 2,
    'match_score': 1,
    'mismatch_score': -2
}


def nw_align(
        seq1: DNA,
        seq2: DNA,
        gap_open_penalty: float = _nw_align_defaults['gap_open_penalty'],
        gap_extend_penalty: float = _nw_align_defaults['gap_extend_penalty'],
        match_score: float = _nw_align_defaults['match_score'],
        mismatch_score: float = _nw_align_defaults['mismatch_score']) \
        -> TabularMSA:
    msa, _, _ = global_pairwise_align_nucleotide(
        seq1=seq1, seq2=seq2, gap_open_penalty=gap_open_penalty,
        gap_extend_penalty=gap_extend_penalty, match_score=match_score,
        mismatch_score=mismatch_score
    )

    return msa
```

This implementation is functionally identical to what we had before, but it now allows us to import the `_nw_align_defaults` dictionary and use it elsewhere.

## Create `_pipelines.py` and add a Pipeline

Next, let's define the function that we'll register as our Pipeline.
Start by creating a new file, `_pipelines.py` in your module's top-level directory.
For me, this file will be `q2-dwq2/q2_dwq2/_pipelines.py`.
Add the following code to that file.

```python
from ._methods import _nw_align_defaults


def align_and_summarize(
        ctx, seq1, seq2,
        gap_open_penalty=_nw_align_defaults['gap_open_penalty'],
        gap_extend_penalty=_nw_align_defaults['gap_extend_penalty'],
        match_score=_nw_align_defaults['match_score'],
        mismatch_score=_nw_align_defaults['mismatch_score']):
    nw_align_action = ctx.get_action('dwq2', 'nw_align')
    summarize_alignment_action = ctx.get_action('dwq2', 'summarize_alignment')

    msa, = nw_align_action(
                    seq1, seq2, gap_open_penalty=gap_open_penalty,
                    gap_extend_penalty=gap_extend_penalty,
                    match_score=match_score, mismatch_score=mismatch_score)
    msa_summary, = summarize_alignment_action(msa)

    return (msa, msa_summary)
```

If you compare this function signature to that of our `nw_align` function, you'll notice they look very similar.
This function, `align_and_summarize`, takes all of the same inputs and parameters as `nw_align`, which allows users the same control over how that functionality works as if they had called `nw_align` directly.
You don't need to expose these parameters - in some cases you may design a Pipeline that implies a certain parameter choice - but in our case our goal is to make this Pipeline an alternative to calling `nw_align` and `summarize_alignment` back-to-back so it makes sense to provide full access to the functionality.

Notice that `align_and_summarize` accesses the default parameter settings in the same way that `nw_align` does, using the `_nw_align_defaults` dictionary that we created above.
So, if we decide at some point that we want to update one of these defaults - maybe we want to set the default `gap_open_penalty` to `4` instead of `5`, we would update that in one place (`_nw_align_defaults`) and it will change the defaults in the two Actions that now use that information.
That's DRY in action.

The one new parameter here with respect to `nw_align` is `ctx`, which was mentioned above.
`ctx` is an instance of a `qiime2.sdk.Context` object.
As a plugin developer, you'll never create one of these objects directly, but your Pipelines may use the `get_action` and `make_artifact` APIs that they provide.
A `qiime2.sdk.Context` object will always be the first parameter that is passed to functions that are registered as `Pipelines`, and by convention this parameter is called `ctx`.

One other difference to notice here is that we are not using type hints (such as `seq1: skbio.DNA`) when we define the function that we'll register as our Pipeline.
That's because the functions that we register as Pipelines, unlike those that we register as Methods and Visualizers, take Artifacts as inputs.
This is because internally they call registered {term}`Actions <Action>`, not the functions that are registered as those Actions, and all Actions in QIIME 2 take their inputs as Artifacts.
It's not until `seq1` (for example) is passed in to the function registered as our `nw_align` Action (`q2_dwq2._methods.nw_align`) that it is transformed to the `skbio.DNA` object that that function takes as input.

The first thing we're doing in our `align_and_summarize` function is getting those actions that we'll use.
These are retrieved using `ctx.get_action`, which takes a plugin name and an action name as input and returns the Action as a function that we can call.
I'm assigning these to variables that end in `_action` to indicate that these are registered QIIME 2 Actions, not the underlying functions that are registered as those Actions.
The plugin referred to in a call to `ctx.get_action` can either be the plugin you're working on (as in our case here), or any other plugin that your plugin has as a dependency.
The action name can be any Method or Visualizer in that plugin.
Here we're retrieving the two actions that we want to run in our Pipeline, `nw_align` and `summarize_alignment`, and assigning those to the variables `nw_align_action` and `summarize_alignment_action`.

We then call each of these functions, providing the output of `nw_align_action` (an {term}`artifact of class <Artifact Class>` `FeatureData[AlignedSequence]`) as the input to `summarize_alignment_action`.
`summarize_alignment_action` then returns a {term}`Visualization` as output.
Each of our `*_action` functions return a tuple of its {term}`Results <Result>`, and in our case each returns only a single Result, which is why the variables that we assign the Results to are followed by commas (as in `msa, = nw_align_action`).
That's a shortcut that would be equivalent to `msa = nw_align_action(...)[0]`.

Finally, we return our Pipeline's Results, an Artifact and a Visualization, in a tuple.

## Register the Pipeline

Pipeline registration is similar to Methods or Visualizer registration, except that the method used for registration is `plugin.pipelines.register_function`.
Because our Pipeline shares many of its inputs with our `nw_align` Method, when we register the `Pipeline` there is another opportunity for duplicated information to make its way into our plugin and violate {term}`DRY`.

Here's the final Pipeline registration code that I ended up with in my `plugin_setup.py` file, after defining some new variables in that file:

```python
plugin.pipelines.register_function(
    function=align_and_summarize,
    inputs=_nw_align_inputs,
    parameters=_nw_align_parameters,
    outputs=_align_and_summarize_outputs,
    input_descriptions=_nw_align_input_descriptions,
    parameter_descriptions=_nw_align_parameter_descriptions,
    output_descriptions=_align_and_summarize_output_descriptions,
    name="Pairwise global alignment and summarization.",
    description=("Perform global pairwise sequence alignment using a slow "
                 "Needleman-Wunsch (NW) implementation, and generate a "
                 "visual summary of the alignment."),
    # Only citations new to this Pipeline need to be defined. Citations for
    # the Actions called from the Pipeline are automatically included.
    citations=[],
    examples={}
)
```

As a **required exercise** after adding this code to your `plugin_setup.py` file, define the variables used in this code block in such a way that it avoids the DRY violation mentioned above.
If you get stuck, refer to [the code that I added for this section](add-pipeline-commit).

After you're done, you should be able to refresh your cache (`qiime dev refresh-cache`), and then call `--help` on your plugin to see your new `Pipeline` in the list.
Try it out using the `SingleDNASequence` Artifacts that you previously passed to the `nw_align` action.

## Add tests and documentation

We're of course not done with our new action until we write its tests and documentation.
In both cases, this builds off work that we previously did when we defined our Method and Visualizer.

As another **required exercise**, add a unit test and a usage example for this Pipeline.
Refer to [the code that I added for this section](add-pipeline-commit) if you need a hint.

When you're done, you should be able to run `make test` and see output like the following:

```shell
$ make test
...
===== 18 passed, 29 warnings in 4.66s =====
```

## An optional exercise

In an earlier optional exercise, you may have added a Method for Smith-Waterman alignment, built on the `skbio.alignment.local_pairwise_align_nucleotide`.
Adapt your new Pipeline so that it gives the user the option of running global (Needleman-Wunsch) or local (Smith-Waterman) alignment.

```{admonition} Hint
:class: tip
You'll likely define a new parameter in your action that toggles whether global or local pairwise alignment is used.
The {term}`Primitive Type` associated with that parameter during your Pipeline registration can be `Str % Choices`, where `Str` and `Choices` are imported from `qiime2.plugin`.
You can find examples of how this is used in the `plugin_setup.py` file of the [`q2-diversity`](https://github.com/qiime2/q2-diversity) plugin.
Use this as an opportunity to refer to other plugins as learning examples.
```
