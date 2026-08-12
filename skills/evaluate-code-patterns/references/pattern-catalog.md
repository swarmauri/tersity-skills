# Reduction pattern catalog

| Pattern | Evidence | Preferred move | Common trap |
| --- | --- | --- | --- |
| Exact clones | Same meaningful block in multiple owners | Extract stable policy or delete obsolete copy | Helper with flags for unrelated behavior |
| Near clones | Same flow with names or literals changed | Parameterize true variation | Hiding domain differences |
| Repeated branching | Same cases spread across call sites | Table dispatch or one authoritative decision | Dense clever expressions |
| Pass-through layers | Wrapper adds no policy, translation, lifecycle, or compatibility | Inline or remove layer | Breaking a documented public seam |
| Parallel models | Duplicate schemas drift together | Establish one source and boundary adapters | Reusing persistence objects everywhere |
| Boilerplate construction | Repeated assembly with stable defaults | Factory, schema, template, or declarative data | Abstracting a single instance |
| Dead compatibility | No supported caller reaches branch | Remove with release evidence | Assuming no text references means unused |
| Configuration sprawl | Same value declared in many places | Choose an authority and derive consumers | Creating another sync script |
| Catch-and-rethrow | Exception adds no context or recovery | Let it propagate | Losing cleanup or translation |
| Test duplication | Setup repeated without semantic value | Fixture, builder, or parameterization | Making tests opaque |

Prefer deletion, data, standard library, existing public APIs, and local helpers—in that order—when they preserve clarity.
