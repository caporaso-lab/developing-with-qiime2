Glossary
========
This page serves as a reference for other documents, we don't recommend reading
it without the accompanying context provided by the rest of this documentation.

.. glossary::
   Action
     A generic term to describe a concrete :term:`method`, :term:`visualizer`,
     or :term:`pipeline`. Actions accept parameters and/or files
     (:term:`artifacts <Artifact>` or :term:`metadata`) as input, and generate
     some kind of output.

   Archive
     The directory structure of a QIIME 2 :term:`Result`.  Contains *at least*
     a root directory (named by :term:`UUID`) and a ``VERSION`` file within
     that directory.

   Artifact
     A QIIME 2 :term:`Result` that contains data to operate on.

   Deployment
     An installation of QIIME 2 as well as zero-or-more :term:`interfaces
     <Interface>` and :term:`plugins <Plugin>`.

   Directory Format
     A string that represents a particular layout of files and or directories
     as well as how their contents will be structured.

   Format
     A string that represents a particular file format.

   Framework
     The engine of orchestration that enables QIIME 2 to function together as a
     cohesive unit.

   Identifier
     A unique value that denotes an individual sample or feature.

   Identity
     Distinguishes a piece of data. QIIME 2 does not consider a rename (like
     UNIX ``mv``) to change identity, however re-running a command, would
     change identity.

   Input
     Data provided to an :term:`action`. Can be an :term:`artifact` or
     :term:`metadata`.

   Interface
     A user-interface responsible for coordinating user-specified intent into
     :term:`framework`-driven action.

   Metadata
     Columnar data for annotating additional values to existing data. Operates
     along Sample IDs or Feature IDs.

   Method
     A method accepts some combination of QIIME 2 :term:`artifacts <Artifact>`
     and :term:`parameters <Parameter>` as :term:`input`, and produces one or
     more QIIME 2 artifacts as :term:`output`.

   Output
     Objects returned by an :term:`action`. Can be :term:`artifact(s)
     <Artifact>` or :term:`visualization(s) <Visualization>`.

   Parameter
     A value that alters the behavior of an :term:`action`.

   Payload
     Data that is meant for primary consumption or interpretation (in contrast
     to *metadata* which may be useful retrospectively, but is not primarily
     useful).

   Pipeline
     A pipeline accepts some combination of QIIME 2 :term:`artifacts
     <Artifact>` and :term:`parameters <Parameter>` as :term:`input`, and
     produces one or more QIIME 2 :term:`artifacts <Artifact>` and/or
     :term:`visualizations <Visualization>` as :term:`output`.

   Plugin
     A discrete module that registers some form of additional functionality
     with the :term:`framework`, including new :term:`methods <Method>`,
     :term:`visualizers <Visualizer>`, :term:`formats <Format>`, or
     :term:`transformers <Transformer>`.

   Primitive Type
     A :term:`type` that is used to communicate parameters to an
     :term:`interface`.  These are predefined by the :term:`framework` and
     cannot be extended.

   Result
     A generic term for either a :term:`Visualization` or an :term:`Artifact`.

   Provenance
     Data describing how an analysis was performed,
     captured automatically whenever users perform a QIIME 2 :term:`Action`.
     Provenance information describes the host system, the computing environment,
     Actions performed, parameters passed, primary sources cited, and more.

   Semantic Type
     A :term:`type` that is used to classify :term:`artifacts<Artifact>` and
     how they can be used. These types may be extended by
     :term:`plugins<Plugin>`.

   Transformer
     A function registered on the :term:`framework` capable of converting data
     in one :term:`format` into data of another :term:`format`.

   Type
     A name that is used to classify how a piece of data may be used.  Most
     commonly used to refer to :term:`Semantic Type`, but can also refer to
     :term:`Primitive Type` and :term:`Visualization (Type)`.

   UUID
     Universally Unique IDentifier, in the context of QIIME 2, almost certainly
     refers to a *Version 4* UUID, which is a randomly generated ID. See this
     `RFC <https://tools.ietf.org/html/rfc4122>`_ or this `wikipedia entry
     <https://en.wikipedia.org/wiki/Universally_unique_identifier>`_ for
     details.

   View
     A particular representation of data. This includes on-disk formats and
     in-memory data structures (objects).

   Visualization
     A QIIME 2 :term:`Result` that contains an interactive visualization.

   Visualization (Type)
     The :term:`type` of a :term:`visualization`. There are no subtyping
     relations between this type and any other (it is a singleton) and cannot
     be extended (because it is a singleton).

   Visualizer
     A visualizer accepts some combination of QIIME 2 :term:`artifacts
     <Artifact>` and :term:`parameters <Parameter>` as :term:`input`, and
     produces exactly one :term:`visualization` as :term:`output`.
