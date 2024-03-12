(garbage-collection-explanation)=
# Garbage Collection

This page does not offer any particularly deep or useful answers, but seeks to serve as a warning that this part of QIIME 2 is *difficult* to understand.
If you think you have a better or more robust way to manage resource allocation, we would love to hear from you!

Because QIIME 2 {term}`Artifacts<Artifact>` are really directory structures, synchronizing filesystem state with memory can be difficult.
It is further excacerbated by the lifetimes of the objects being unkown.
For example viewing an artifact can produce anything from a in-memory object to an entirely new directory structure.

Currently, QIIME 2 chooses to tie the filesystem state directly with an objects lifetime in memory.
This means that instead of allocating a location and automatically destroying it with a static lifetime (e.g. RAII/context manager) it is handled dynamically.
It is up to the Python garbage collector to invoke a destructor that cleans the filesystem when appropriate.
This pushes the issue off from managing lifetimes, to ensuring that destruction occurs and that the data *should* be destroyed (e.g. it is not user-input).

The objects responsible for managing filesystem paths (and destroying them) are located in `qiime2.core.path`.

Additionally it is not always the case that the garbage collecter *will* call a destructor. 
For example in a multiprocessing context, `sys._exit` is called instead of `sys.exit`, meaning that any filesystem objects created in the child-process will not be cleaned up.
Exceptions are another way in which normal cleanup can become confounded.
Fortunately there is an additional object `qiime2.sdk.context:Context` which can be used to juggle this information and can provide a context-manager for when a static lifetime is known.
