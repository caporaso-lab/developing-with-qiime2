# Pipeline Context Object
The context object is available to pipelines as a required first argument ``ctx``.
Plugins may use these methods to invoke other registered actions or create artifacts.


```{eval-rst}
.. automethod:: qiime2.sdk.Context.get_action
.. automethod:: qiime2.sdk.Context.make_artifact

```