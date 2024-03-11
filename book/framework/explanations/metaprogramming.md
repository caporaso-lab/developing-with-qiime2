(metaprogramming-explanation)=
# Metaprogramming

The framework uses a significant amount of runtime metaprogramming in which properties and methods are swapped out or constructed at the last minute based on plugin information.
This list shows some of the aspects of the Python language that are used to achieve this:

- decorators (used everywhere, `qiime2.sdk.action:Action` is really just a decorator-object)
- descriptor protocol (used in `qiime2.core.util:LateBindingAttribute`)
- import hooks (used by Artifact API)
- metaclasses (used by `qiime2.plugin.model.directory_format`)
- eval (`qiime2.skd.util:parse_type` and `decorator` package for signature rewriting)
