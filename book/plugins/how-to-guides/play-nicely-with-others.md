(how-to-play-nicely)=
# How to play nicely with other plugins

There are several namespace considerations to keep in mind when developing
QIIME 2 {term}`plugins <Plugin>` or {term}`actions <Action>`.

- {term}`Plugin` names are unique, and collisions are not tolerated by the framework.
  This means if you want to name your plugin ``dada2``, users will not be able to have your plugin **and** the [DADA2](https://github.com/qiime2/q2-dada2) plugin installed in the same {term}`deployment` at the same time.
- {term}`Action` names are **not** globally unique, but rather are namespaced within a plugin's domain.
- {term}`Semantic Types <Semantic Type>`, {term}`Formats <Format>`, and {term}`Transformers <Transformer>` are registered globally, like plugins, again, if you choose to use an existing name, this will prevent users from deploying both offending plugins concurrently.

There are a few strategies the QIIME 2 developers have employed to work within
these limits:

- Most {term}`types <Type>`, {term}`formats <Format>`, and {term}`transformers <Transformer>` are registered in a single {term}`plugin`: [q2-types](https://github.com/qiime2/q2-types).
  This prevents circular imports.
  For many 3rd-party plugin developers, this means most typical types and formats are available within a single import.
  If you're creating new types in your plugins, avoid re-using type names.
  Generally types are well established before being added to q2-types, since we commit to backward compability of q2-types (so it's hard to make changes to type names, for example).
- Plugin naming takes one of two approaches, typically:
   - The name matches the source tool being wrapped (e.g. `cutadapt`).
   - The name is some generic descriptor, like `diversity` or `taxa`.
- Action naming typically takes one of two approaches:
   - The name matches a subcommand or method on the source tool being wrapped.
   - The name is a generic descriptor, and typically is written as a verb (but not exclusively).
