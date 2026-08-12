# Root-cause debugging rubric

Ask in order:

1. What is the first observable divergence from expected behavior?
2. Which component owns the violated invariant?
3. Is the bad state created, accepted, transformed, persisted, or merely observed here?
4. Does an existing authoritative implementation already encode the correct behavior?
5. Can one regression fail before and pass after the correction?
6. Does the patch prevent invalid state or only tolerate it later?
7. Are new branches required by the contract or compensating for uncertainty?

A minimal patch is the smallest semantic correction, not necessarily the fewest changed lines.
