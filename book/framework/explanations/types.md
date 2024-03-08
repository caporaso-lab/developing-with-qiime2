(types-explanation)=
# Semantic and Primitive Types

```{eval-rst}

QIIME 2 uses a combination of types and formats to represent: what data *means* and how to *use* it, respectively.
This document will attempt to motivate why typing may be useful and outline how QIIME 2 implements types and what they can be used for.

An Analogy
----------
Suppose we were interested in modeling a system in which there were *hands*,
*utensils* and *tasks*. We are trying to determine which *utensils* can be used
to complete which *tasks*. Here *utensils* are like QIIME 2 :term:`artifacts<Artifact>` and *tasks* are QIIME 2 :term:`actions<Action>`.
Imagine then, that this hand (unlike yours or mine) is not intelligent and will grasp anything to carry out its work without further consideration.
The *hand* then, represents the computer.

To make this example more concrete, let's suppose we wanted to write a note.
We provide to the hand a fork, and ask it to return to us a note.
Accepting the fork, the hand blithely tears the paper into shreds and hands you what remains, considering its mission to be complete.

This is not ideal.

Instead, lets give the hand some rules it can follow to determine if it should perform a task with a utensil.
For example, we would have prefered it use a pencil when writing a note instead of a fork.
To describe this more formally, we might say that a task "write note" requires
a pencil and returns a note::

  write note : pencil -> note

Repeating the above situation, we provide a fork to the hand and ask it to write a note.
The hand observes that a fork cannot be used to make a note as it is not a pencil, and our paper remains unshredded (though still blank).

However, if we were to write a note with a pen, according to the above rules,
we would also be refused, as only pencils are allowed to write notes.
Instead of helping us, the type annotation above seems to be in the way.

Finding a way to fix this mismatch while still constraining inputs is the
fundamental goal of a type system and is where a lot of complexity arises.
There is also a lot of freedom in implementation, some type systems are as
strict as the above, and provide little *expressive power*, others provide a
great deal (becoming Turing-complete in the process) at the cost of complexity.

Ultimately it is important to remember what the purpose is.
A type system should abstract away details that the computer *needs* but which impede a person's comprehension of a system.
A good type system should be a compromise between the fuzzy (and indistinct) world of language that people understand, and robust formal systems that computers can use.

Defining a Type
---------------
In QIIME 2 there are 3 *kinds* of types, all of which use the same underlying grammar.
Only one of these kinds can be extended, the :term:`Semantic Type`.
The other two, :term:`Primitive Type` and :term:`Visualization`, are built into the framework.

Semantic types are the only kind that can be extended, so let's start there with our example from before.

To create a type, we use the :func:`SemanticType <qiime2.plugin.SemanticType>` factory:

.. testsetup:: utensils

   from qiime2.plugin import SemanticType, Plugin, Properties
   plugin = Plugin('name', 'version', 'website', '__main__')
   other_plugin = Plugin('name', 'version', 'website', '__main__')

.. testcode:: utensils

   Pencil = SemanticType('Pencil')

That's it! Let's define some more:

.. testcode:: utensils

   Pen = SemanticType('Pen')
   Fork = SemanticType('Fork')
   Spoon = SemanticType('Spoon')
   Chalk = SemanticType('Chalk')

To let QIIME 2 know that these new types exist, we'll need to register them on
our :class:`plugin object <qiime2.plugin.Plugin>` with :func:`register_semantic_types<qiime2.plugin.Plugin.register_semantic_types>`:

.. testcode:: utensils

   plugin.register_semantic_types(Pencil, Pen, Fork, Spoon, Chalk)

Now QIIME 2 is aware of these types and we can use them.

There are only 5 types right now, but imagine we had dozens, it might get a bit
hard to keep them all straight. To make it easier for us to talk about them, we
can try to group similar types together. Looking at our type, we seem to have
two broad categories so far, writing and dining utensils. Let's define some
*composite types* to group them:

.. testcode:: utensils

   Dining = SemanticType('Dining', field_names=['utensil'],
                         field_members={ 'utensil': (Fork, Spoon) })

   Writing = SemanticType('Writing', field_names=['implement'],
                          field_members={ 'implement': (Pen, Pencil, Chalk) })

And of course we should register these as well:

.. testcode:: utensils

   plugin.register_semantic_types(Dining, Writing)

Before explaining what the new parameters are, let's use these and circle back:

.. testcode:: utensils

   Writing[Pen]
   Writing[Pencil]
   Writing[Chalk]

   Dining[Spoon]
   Dining[Fork]

Since we don't have many types, this may look a little silly,
but now we can talk about dining and writing utensils as broad groups.
What happens if we try to mix these? Let's make some *dining chalk* (gross!):

.. testcode:: utensils

   Dining[Chalk]

It produces the following exception:

.. testoutput:: utensils

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/home/evan/workspace/qiime2/qiime2/qiime2/core/type/grammar.py", line 68, in __getitem__
       self._validate_field_(*args)
     File "/home/evan/workspace/qiime2/qiime2/qiime2/core/type/semantic.py", line 184, in _validate_field_
       raise TypeError("%r is not a variant of %r." % (value, varfield))
   TypeError: Chalk is not a variant of Dining.field['utensil'].

.. comment to catch the escaped asterisk -->* got 'em!

It appears chalk is off the menu. Let's go back over the definition for ``Dining``:

.. testcode:: utensils

   Dining = SemanticType('Dining', field_names=['utensil'],
                         field_members={ 'utensil': (Fork, Spoon) })

Unlike the simpler types, this adds ``field_names`` and ``field_members``,
if we were to look at ``Dining`` on its own:

.. testcode:: utensils

   print(Dining)

We see:

.. testoutput:: utensils

   Dining[{utensil}]

This ``{utensil}`` is the *field name*, because ``field_names`` is a list, we
could have more than one, letting us get combinatorical, but that usually
isn't necessary.

Looking at ``field_members`` we see that for the field named ``utensil`` there
are two permitted *variants*: ``Fork`` and ``Spoon``. This is why creating
``Dining[Chalk]`` didn't work so well, ``Chalk`` isn't a variant of ``Dining``'s field ``utensil``.


Extending a Type
----------------

Suppose we were satisfied with the above vocabulary of utensils. So much so,
we considered ourselves to have described all of the utensils we would ever need.
Obviously that isn't going to be true, so there should be a way for other plugins to define new types,
while still being able to organize them into our existing hierarchy of labels.

A *seperate plugin* could then define something like this:

.. testcode:: utensils

   Knife = SemanticType('Knife', variant_of=[Dining.field['utensil']])

Breaking this down, it is similar to some of the earlier invocations of the
:func:`SemanticType<qiime2.plugin.SemanticType>` factory, but there's a new argument for
``variant_of`` which seems to be providing a list of *fields* from other *composite types*.
This means a plugin can extend existing types as needed. In this case, we've
suggested that in addition to forks and spoons, there are knives.

We can also create new categories and types that belong to more than one category.
Let's create a category for kitchen utensils. A knife has already been defined, but you wouldn't
cook with a steak knife, and you wouldn't eat with a chef's knife, so there's more we can add to the
knife's story:

.. testcode:: utensils

   Kitchen = SemanticType('Kitchen', field_names=['utensil'],
                          field_members={ 'utensil': [Knife] })

   Spatula = SemanticType('Spatula', variant_of=[Kitchen.field['utensil']])
   PastryBag = SemanticType(
       'PastryBag', variant_of=[Kitchen.field['utensil'], Writing.field['implement']])

This creates a new ``Kitchen`` category, and adds ``Knife`` as a member.
It also adds ``Spatula`` to ``Kitchen`` and adds ``PastryBag`` to both ``Kitchen`` *and* ``Writing``.
In case you don't know what a pastry bag is (like me), it's how you would write "Happy Birthday" on a cake.
Just as not all knives are the same, not all pastry bags are well suited to writing (some are better for making decorative frosting-flowers).

.. testcode:: utensils

   Dining[Knife]
   Kitchen[Knife]
   Kitchen[Spatula]
   Kitchen[PastryBag]
   Writing[PastryBag]

We should :func:`register these<qiime2.plugin.Plugin.register_semantic_types>` before we forget:

.. testcode:: utensils

   other_plugin.register_semantic_types(Knife, Kitchen, Spatula, PastryBag)

Primitive Types
---------------
Primitive types are the other main kind of type you'll use in QIIME 2.
These closely match their associated data types making them simple to work with, but they also have a few
extra tricks up their sleeves to make it possible to automatically generate rich user :term:`interfaces<Interface>`.
The purpose of these types is to explain what kinds of parameters can be provided to an :term:`action`.

There are a few basic types:

- :data:`Int<qiime2.plugin.Int>`
- :data:`Bool<qiime2.plugin.Bool>`
- :data:`Float<qiime2.plugin.Float>`
- :data:`Str<qiime2.plugin.Str>`

These work essentially as you would expect, an ``Int`` holds an integer, a ``Str`` holds a unicode string.
They are capitalized to make differentiating them from their Python counterparts (``int`` and ``str``) simpler.

There are a few collection types:

- :data:`List[{elements}]<qiime2.plugin.List>`
- :data:`Set[{elements}]<qiime2.plugin.Set>`

Each of these allows you to provide one of the above basic types to their ``{elements}`` field.

There are also some metadata types:

- :data:`Metadata<qiime2.plugin.Metadata>` (the type, not the :class:`object<qiime2.metadata.Metadata>`)
- :data:`MetadataColumn[{type}]<qiime2.plugin.MetadataColumn>`
  which has the following column types (for the ``{type}`` field):

  - :data:`Numeric<qiime2.plugin.Numeric>`
  - :data:`Categorical<qiime2.plugin.Categorical>`

From these we can construct simple expressions like:

.. testsetup:: primitives

   from qiime2.plugin import (
       Int, Float, Str, List, Set, Metadata, MetadataColumn, Numeric, Choices,
       Range)

.. testcode:: primitives

   Int
   List[Int]
   Set[Str]
   Metadata
   MetadataColumn[Numeric]

Of course, just writing down a type isn't necessarily useful unless we can *use* it for something.
Let's do that now:

.. testcode:: primitives

   # These are true:
   assert      1 in Int
   # These are not:
   assert not  "banana" in Int
   assert not  0.5 in Int

   # True:
   assert      "banana" in Str
   # Not true:
   assert not  1 in Str

   # True:
   assert      [1, 2, 3] in List[Int]
   # Not true:
   assert not  ['a', 'b', 'c'] in List[Int]

   # True:
   assert      ['a', 'b', 'c'] in List[Str]
   # Not true:
   assert not  [1, 2, 3] in List[Str]

While these are all useful constructs, real-world user input must often be constrained to just a few
valid strings, or a real number bounded from zero to one. To express these ideas we need a little bit more.

Refining a Type
---------------
A *refinement type* is a type that possesses a *predicate* which further constrains the domain of a type.
Thats a formal definition anyway. The important piece is the *predicate*, which is a boolean "function" describing whether a given instance is *in* the domain, or *out* of the domain. This means we can *refine* the type to suite our needs.

Suppose we were a graphical interface. A common UI element is a dropdown list containing
predetermined choices. We can express that with a primitive type!

Choices
```````
Let's see an example of this, using the :data:`Choices<qiime2.plugin.Choices>` predicate:

.. testcode:: primitives

   # These are Python objects, so we can assign to variables:
   dropdown = Str % Choices({'banana', 'apple', 'pear'})

   assert      'banana' in dropdown
   assert not  'grape' in dropdown
   assert not  0.5 in dropdown


The ``%`` operator adds a *predicate* like ``Choices`` to a type.
You can read it as "string modulo choices" in your head if you like. It almost makes sense.

You can see how a graphical interface could inspect this type and automatically generate
a dropdown list containing "banana", "apple", and "pear".

Let's try something harder, suppose we wanted to describe some checkboxes, where the choices
can be selected at most once, but multiple different choices are allowed:

.. testcode:: primitives

   checkboxes = Set[Str % Choices({'banana', 'apple', 'pear'})]

   assert      {'banana'} in checkboxes
   assert      {'apple', 'banana'} in checkboxes
   assert not  {'banana', 'grape'} in checkboxes
   assert not  {1, 2, 3} in checkboxes
   assert not  'banana' in checkboxes

We might read that as "A set of strings modulo the choices of banana, apple, and pear".
It is a mouthful, but we've just described an entire UI element in a single line.

Additionally, this is *abstract*, we never actually asked for a checkbox. So the interface can
make its own decision about how best to represent this type in its UI. For example a
command line interface cannot show checkboxes, but it might have an interactive dialog, or
it may just accept multiple arguments for the parameter. A programmatic interface may simply
accept a set object instead. It is up to the interface to make the best choice it can.
The plugin developer does not need to worry about the representation.

.. admonition:: Interface Developer Note:

   An easy way to transfer (or dispatch on) a type is to use the ``.to_ast()`` method which will
   provide a JSON structure describing the type in a machine-friendly representation.

   For example:

   .. testcode:: primitives

      import json

      print(json.dumps(checkboxes.to_ast(), indent=2, sort_keys=True))

   .. testoutput:: primitives
      :options: +SKIP

      {
        "fields": [
          {
            "fields": [],
            "name": "Str",
            "predicate": {
              "choices": [
                "banana",
                "apple",
                "pear"
              ],
              "name": "Choices",
              "type": "predicate"
            },
            "type": "primitive"
          }
        ],
        "name": "Set",
        "predicate": {},
        "type": "collection"
      }


Range
`````
Another predicate we can use is :data:`Range<qiime2.plugin.Range>`:

.. testcode:: primitives

   proportion = Float % Range(0, 1, inclusive_end=True)

   assert      0 in proportion
   assert      0.5 in proportion
   assert      1 in proportion
   assert not  -1.5 in proportion
   assert not  1.5 in proportion
   assert not 'banana' in proportion

This can be combined with :data:`Int<qiime2.plugin.Int>` as well. As before we
can nest these kinds of expressions inside of :data:`Set<qiime2.plugin.Int>` and :data:`List<qiime2.plugin.Int>`.

Semantic Properties
```````````````````
Leaving behind the primitive types and returning the the semantic types, there is a final
trick we can use to constrain the semantics of a type. It is to use the :func:`Properties<qiime2.plugin.Properties>` predicate. This predicate can only be attached to semantic types, so we usually call them
semantic properties of the type.

Thinking back to our example involving utensiles, there was a type named:

.. testcode:: utensils

   Kitchen[Knife]

Suppose we were a plugin that specialized in cutting things, with actions such as filleting fish, paring fruit, etc. To other plugins, the distinction between different kinds of cutlery might be uninteresting. To us, however, *cutting things is what we do*. We wouldn't fillet a fish without a fillet knife. The nomenclature discussed so far lacks that granularity.

In a perfect world, we would extol the virtues of being specific about cutlery, suggesting others adopt a new
category ``Cutlery[{knife}]`` to help better model the world of things-hands-can-use.
Building consensus can be slow, though, and you are still interested in inter-operating with other plugins
(even if they don't understand why anyone would need more than one kind of knife).

To fix this, you can add a property:

.. testcode:: utensils

   Kitchen[Knife % Properties('fillet')]

What this means is that you've created a new *subtype* of ``Knife`` using the label "fillet".
There aren't any rules for recognizing a fillet knife, so its something that has to be explicitly attached (but that is the case with all semantic types).

There can additionally be more than one property on a type:

.. testcode:: utensils

   Kitchen[Knife % Properties(include=['fillet', 'sharp'])]
   Kitchen[Knife % Properties(include=['paring'], exclude=['sharp'])]

Now we can describe things like a *sharp fillet knife* or a *dull paring knife*.
To illustrate how these are used, we need to talk more about *subtyping*.

Semantic Subtyping
------------------
A subtype is some type that is *substitutable* for another. Here's another way to think
about it: the domain of the subtype exists *entirely within* the domain of the supertype.
Anywhere you could use a supertype, a subtype will suffice.

There are two ways to create this relation: with a semantic property (described above), or with a *union operator*: ``|``. In order to use a subtyping relation, we also need
an operator to test the relation, for that we can use ``<=`` and ``>=`` (which matches the Python ``set`` API).

Let's try it out:

.. testcode:: utensils

   assert      Spoon <= Spoon  # is spoon a subtype of spoon?
   assert      Spoon >= Spoon  # is spoon a supertype of spoon?
   assert not  Fork <= Spoon   # is fork a subtype of spoon?
   assert not  Fork >= Spoon   # is fork a supertype of spoon?

Here we have the makings of equality and inequality.
We see that any instance of a ``Spoon`` can be substituted wherever a ``Spoon`` is required (which is obvious enough), and we also see that a ``Fork`` will not do, when a ``Spoon`` is needed (soup comes to mind).

Unions
``````
Of course, this subtyping relationship isn't very interesting, let's use the union operator to *construct a supertype*:

.. testcode:: utensils

   assert      Spoon <= Spoon | Fork
   assert      Fork <= Spoon | Fork
   # The relationship has direction:
   assert not  Spoon >= Spoon | Fork
   assert not  Fork  >= Spoon | Fork
   # And of course, unrelated things are not equal
   assert not  Knife <= Spoon | Fork
   assert not  Knife >= Spoon | Fork

Using this mechanism we can define actions that accept a broad range of types, while still being specific about which types are known to work. Also instead of using ``A <= B <= A`` to test equality, we can use ``.equals`` (the operator is reserved for hash-equality).

We can also evaluate more sophisticated expressions:

.. testcode:: utensils

   assert not  Dining[Knife].equals(Kitchen[Knife])
   assert      Dining[Knife] <= Kitchen[Knife] | Dining[Knife]
   # Union types also have subtyping relations:
   assert      Writing[Pencil] | Writing[Pen] <= Writing[Pencil] | Writing[Pen] | Writing[Chalk]
   # or more concisely:
   assert      Writing[Pencil | Pen] <= Writing[Pencil | Pen | Chalk]

In QIIME 2, subtyping and equality are *extensional*, meaning that the order and form do not matter, only the meaning.

In other words, these expressions are the same:

.. testcode:: utensils

   assert  (Writing[Pencil] | Writing[Pen]).equals(Writing[Pen | Pencil])
   assert  Writing[Pencil | Pen].equals(Writing[Pen | Pencil])

Properties
``````````
Let us return now to the other way of constructing a subtyping relation, the :class:`semantic property<qiime2.plugin.Properties>`. We had the following definitions which we'll assign to a variable, since they are lengthy:

.. testcode:: utensils

   sharp_fillet = Kitchen[Knife % Properties(include=['fillet', 'sharp'])]
   dull_paring  = Kitchen[Knife % Properties(include=['paring'], exclude=['sharp'])]

How should these relate to a plain ``Kitchen[Knife]``? Well, because we've added information about the knife, we've *refined* the domain, and so we have a *subtype*. In other words, our fancy knifes can be used wherever a normal knife can be used. The way to think about this is we haven't created something new, paring knives and fillet knives were always in the set of ``Kitchen[Knife]``, but until we added the property we were unable to distinguish them.

.. testcode:: utensils

   assert  sharp_fillet <= Kitchen[Knife]
   assert  dull_paring  <= Kitchen[Knife]

Additionally, the combination is still a smaller domain than the domain of all kitchen knives:

.. testcode:: utensils

   assert  sharp_fillet | dull_paring <= Kitchen[Knife]

What is most important is that an action that needs something specific can avoid receiving an over-general type. For example, consider this action::

  sharpen knife : Kitchen[Knife % Properties(exclude=['sharp'])
      -> Kitchen[Knife % Properties(include=['sharp'])

This rather intuitively swaps the property of not-being sharp for the property of being sharp.
We can see how the subtyping relation allows the action to enforce this:

.. testcode:: utensils

   assert      dull_paring  <= Kitchen[Knife % Properties(exclude=['sharp'])]
   assert not  sharp_fillet <= Kitchen[Knife % Properties(exclude=['sharp'])]

One consequence of this is that an unadorned type like ``Kitchen[Knife]`` is not known to be either sharp or dull (remember it is actually supertype of both of these).

.. testcode:: utensils

   # Can't substitute any-old knife for a dull one, some of them are sharp.
   assert not  Kitchen[Knife] <= Kitchen[Knife % Properties(exclude=['sharp'])]

As a matter of practice, it would probably be easier for everyone if "sharpen knife" were to just re-sharpen the already-sharp knife.

Intersections
`````````````
There is another kind of type known as the intersection type. Currently QIIME 2 implements this only in a very limited way.
The idea is that you might have an instance that is simultanously many different types. For example, a *spork* is both a fork and a spoon (and good at neither).

Nonetheless, someday you might write something like this:

.. code-block:: python

   # This doesn't work yet
   Spork = Fork & Spoon

   assert  Spork <= Fork
   assert  Spork <= Spoon

As you can see, the relationship is inverted from a union. Why bring this up, if the above isn't implemented?
First, this syntax would be a convenient way to describe *compound artifacts*, where a lot of data is bundled up nicely in a single zip file. Second, this is how semantic properties work.

When you are dealing with multiple semantic properties, each property is *intersected* with the others, meaning that an artifact that has multiple properties associated with it is considered to have each one. This means these expressions are the same:

.. code-block:: python

   Knife % Properties(['fillet', 'sharp'])
   # is the same as:
   (Knife % Properties('fillet')) & (Knife % Properties('sharp'])
   # if `&` was implemented

It also means that this is true:

.. testcode:: utensils

   assert  Knife % Properties(['fillet', 'sharp']) <= Knife % Properties(['fillet']) <= Knife

The more information we add, the more specific our knife (and the smaller our domain).
```