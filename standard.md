# DEP&CC 2.0
## Deduction-Exact Proofs & Clean Communication
### Psychopathic Tier

**Target dialects:** LaTeX (TeX Live, pinned), Lean 4 / Mathlib, Coq/Rocq, Isabelle/HOL, restricted Markdown+KaTeX  
**Version:** 2.0  
**Status:** Normative Draft Standard  
**Supersedes:** nothing  
**Applies to:** mathematics, mathematical logic, theoretical computer science, statistics, and any research paper whose load-bearing claims are deductive, computational, or statistical.

---

## Revision history

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-11-07 | Initial normative release. Chapters 1–62, Appendices A–J. Full uncompressed detail. |

---

# 1. Purpose

DEP&CC 2.0 is a writing, structuring, and verification standard for documents that must satisfy both of the following properties simultaneously:

1. **Deduction-exact discipline.**  
   Logical validity is a correctness requirement, not an aspiration. Every inference has a named justification, every hypothesis has a discharge site, every axiom has a ledger entry, and every claim has a status that cannot be silently upgraded.

2. **Clean-communication discipline.**  
   The document must remain explicit, auditable, reviewable, gap-aware, and free of hidden conventions, overloaded notation, and prose that conceals inference.

This standard is intended for work where a logical gap, an ambiguous quantifier, an unstated regularity condition, or an unreproducible experiment is unacceptable. Examples include:
- pure and applied mathematics,
- mathematical logic, set theory, model theory, proof theory,
- type theory and formalized mathematics,
- theoretical computer science: complexity, algorithms, semantics, verification,
- cryptography and security proofs,
- probability theory, stochastic processes, mathematical statistics,
- machine learning theory,
- numerical analysis and scientific computing,
- empirical research papers with statistical or computational claims,
- optimization, control theory, information theory,
- mathematical physics with rigorous claims.

The standard is deliberately strict. It assumes that:
- authors will forget hypotheses,
- referees will not check degenerate cases,
- notation will drift over 60 pages,
- constants will silently acquire dependencies,
- limits will be interchanged because "it's fine",
- `sorry` will be temporary forever,
- citations will point at theorem numbers that changed between arXiv versions,
- the abstract will claim more than Section 5 proves,
- conventions will be inherited silently from a subfield,
- and the reader will be blamed for a defect of the author.

Therefore, DEP&CC favors mechanical enforcement, explicit ledgers, measured readability, pinned artifacts, and machine-checked proof wherever possible.

---

# 2. What "DEP&CC" means

## 2.1 DEP: Deduction-Exact Proofs

DEP means that the *logical cost* of a claim is explicit, bounded, and discharged.

A theorem is not DEP-compliant merely because it is true. It is not DEP-compliant because it is published, famous, or believed. It is DEP-compliant only if its deductive structure is fully accounted for.

A DEP-compliant load-bearing theorem must be able to answer **all** of the following questions. This list is normative; it is the audit interrogatory for DEP-0.

**Statement hygiene**
- What is the exact ambient structure (set, space, category, model, theory)?
- What are the sorts/types of every symbol in the statement?
- Which quantifiers are universal, which existential, and in what order?
- Is every quantifier's domain nonempty, and is emptiness handled?
- Is the statement vacuously true, and if so is that declared?
- Does at least one non-vacuous instance exist, and is a witness given?
- Are the hypotheses stated in the statement, or only in surrounding prose?
- Are the hypotheses independent, redundant, or mutually contradictory?
- Is the conclusion an implication, equivalence, existence, uniqueness, or bound?
- If existence: is it constructive, effective, or purely classical?
- If uniqueness: up to what equivalence, and is that equivalence stated?
- If a bound: is it uniform, and in which parameters?

**Ambient conventions**
- Does $\mathbb{N}$ contain $0$?
- Is the ring commutative, unital, Noetherian, reduced?
- Is the measure complete, $\sigma$-finite, Radon, Borel, probability?
- Is the space Hausdorff, second countable, separable, complete, metrizable?
- Is the manifold smooth, with boundary, oriented, connected?
- Is the category small, locally small, complete, cocomplete, and in which universe?
- Is the graph simple, finite, directed, loopless, connected?
- Is the algebra over a field or a ring, finite-dimensional, associative, unital?
- Is the Hilbert space real or complex, separable, and which argument is linear?
- Is $\log$ natural, base 2, or base 10? Is entropy in nats or bits?
- Is $\subset$ proper inclusion or inclusion?
- Is "positive" $> 0$ or $\ge 0$? Is "increasing" strict?
- Is the Fourier transform normalized with $2\pi$ in the exponent, the prefactor, or split?
- Is the model of computation a Turing machine, RAM, word-RAM, circuit family?
- Is complexity measured in bits or arithmetic operations? Uniform or non-uniform?

**Analytic hygiene**
- Is every function claimed measurable actually measurable, and with respect to which $\sigma$-algebras?
- Is every integral well-defined (integrable, or nonnegative, or principal value declared)?
- Is every limit interchanged with another operation justified by a named theorem?
- Are the hypotheses of that theorem discharged, all of them?
- Is convergence pointwise, uniform, in measure, a.e., in $L^p$, weak, weak-*, or distributional?
- Is the exceptional null set fixed once, or does it depend on a parameter?
- If uncountably many null sets appear, is their union still null?
- Is the supremum attained? Is it $\sup$ or $\max$? Is it finite?
- Is the derivative classical, weak, distributional, Fréchet, Gâteaux, or Clarke?
- Is the interchange of $\partial$ and $\int$ dominated, or locally dominated, or uniform?
- Is Fubini or Tonelli being invoked, and are the sign/$\sigma$-finiteness hypotheses met?
- Is compactness used, and is the topology specified?
- Is a subsequence extracted, and does the notation silently reuse the original index?
- Is a diagonal argument's array countable?

**Probabilistic hygiene**
- Is the probability space named, and are all random variables defined on it?
- Is the filtration specified, and are processes adapted, predictable, optional?
- Is independence claimed pairwise or mutual? Is it conditional independence?
- Is conditioning on a null event avoided, or is a regular conditional probability constructed?
- Which version of conditional expectation is used, and does the claim depend on the version?
- Is `a.s.` attached to every statement that holds only almost surely?
- Is uniform integrability checked before exchanging limit and expectation?
- Is optional stopping justified (bounded, UI, integrable with a.s. finite stopping time)?
- Are concentration inequality preconditions met (boundedness, sub-Gaussianity, independence, martingale differences)?
- Is the distribution determined by its moments, if a moment argument is used?
- Is a limit theorem applied to a triangular array or a fixed sequence?

**Algebraic / categorical hygiene**
- Is every map claimed canonical actually canonical, or is a choice made?
- Is a choice made simultaneously for infinitely many objects, and is AC used?
- Is the diagram claimed commutative verified, or asserted?
- Is naturality in every argument, or only in some?
- Are size issues (small vs large, universe levels) explicit?
- Is an adjoint's existence proved or obtained from an adjoint functor theorem whose hypotheses are discharged?
- Is an isomorphism natural, and is the naturality square given?
- Is a "canonical identification" a definitional equality or a proved isomorphism?

**Logical hygiene**
- Is the object language / metalanguage distinction maintained?
- Is the theory effectively axiomatized where required?
- Is the logic first-order, and if not, is compactness/completeness re-justified?
- Are free variables free, and is capture avoided in every substitution?
- Is the induction on a well-founded relation, and is that relation proved well-founded?
- Is the induction measure decreasing in every case, including limit cases?
- Is the proof classical, intuitionistic, or constructive, and is that declared?
- Is LEM, AC, DC, or a choice-equivalent used invisibly (e.g. "pick a maximal element")?
- Is the incompleteness/undefinability theorem applied to a theory meeting its hypotheses?
- Are provability predicates satisfying the derivability conditions, and which ones?

**Computational hygiene**
- Is every reported number reproducible from a pinned artifact?
- Is the arithmetic exact, floating-point, interval, or certified?
- Is the numerical claim a proof, an estimate, or a heuristic?
- Is a CAS result trusted, and if so what is the trust boundary and certificate?
- Is the search space exhausted, or sampled? If sampled, with what seed?

**Dependency hygiene**
- Which prior results does the proof use, by exact identifier?
- Is the dependency graph acyclic?
- Is any cited result conditional, unpublished, retracted, or itself DEP-noncompliant?
- Is any cited result used outside its stated hypotheses?
- Is the citation pinpointed to theorem number, version, and page?

If the answer to any applicable question is "I don't know", "it's standard", or "obviously", the theorem is **not DEP-compliant**.

## 2.2 CC: Clean Communication

Clean communication does not mean "short", "elegant", "dense", or "beautiful" in a subjective sense. Density is not a virtue; it is a cost transferred to the reader.

Clean communication means the argument can be **reconstructed without guessing**.

A clean theorem must make the following obvious:
- what it asserts,
- why it is worth asserting,
- what it assumes,
- what it does not assume,
- what it generalizes and what it fails to generalize,
- what is proved, what is cited, what is conjectured,
- where the proof is,
- what the proof's structure is,
- what the notation means, locally,
- whether it is complete, partial, sketched, or gap-declared.

DEP&CC treats the following as **communication defects** when they hide inference or cost:
- "clearly", "obviously", "it is easy to see", "by standard arguments",
- "after routine computation", "by a straightforward induction",
- "the general case follows similarly",
- "we may assume without loss of generality" without a reduction,
- "by symmetry" without the invariance proof,
- "up to constants" without the constant ledger,
- "for sufficiently large $n$" without the threshold's dependencies,
- "generic", "typical", "almost all" without a measure or topology,
- "canonical", "natural", "essentially unique" without proof,
- reusing a symbol with a new meaning,
- reusing $C$ for unrelated constants in the same proof,
- suppressing the measure in `a.e.`, $L^p$, or $\int$,
- suppressing the universe in a category-theoretic claim,
- hypotheses that live only in the introduction,
- a proof whose case analysis is not exhaustively enumerated,
- a diagram asserted commutative with no verification,
- an equation chain whose middle relation is unlabelled,
- prose that mixes intuition and deduction without visual separation,
- an abstract that asserts more than the theorems entail.

## 2.3 Psychopathic Tier

"Psychopathic tier" means the standard does not rely on good intentions, mathematical taste, or the referee's generosity. It assumes violations occur unless prevented by:
- proof assistants and kernel checking,
- axiom-ledger extraction (`#print axioms`, `Print Assumptions`),
- dependency-graph extraction and cycle detection,
- symbol-registry linting,
- hypothesis discharge linting,
- readability metric gates,
- convention-manifest linting,
- citation pinning and retraction checks,
- artifact reproduction gates,
- degeneracy batteries,
- adversarial reading protocols,
- signed, expiring waivers,
- review checklists.

A rule that cannot be enforced is weak. DEP&CC rules are designed to be mechanically or structurally checkable, and Chapter 50 states exactly which are and which are not.

---

# 3. Normative terms

The following terms have normative meaning in this standard.

- **Must / Shall**: mandatory requirement. Non-compliance is a defect of the stated severity.
- **Must not / Shall not**: mandatory prohibition.
- **Should**: strong recommendation; deviation requires a written justification in the annotation block.
- **Should not**: strong discouragement; deviation requires written justification.
- **May**: permitted optional behavior.
- **Banned**: forbidden in the specified context. Severity 0 or 1.
- **Restricted**: allowed only under the explicitly stated conditions.
- **Expository-only**: allowed only in DEP-2 regions.
- **Load-bearing**: a statement whose failure invalidates a main result. Load-bearing status is transitive over the dependency graph.
- **Discharged**: a hypothesis, obligation, or gap for which a justification exists at a named location and is referenced by identifier.
- **Obligation**: a proof duty generated by a construct (e.g. well-definedness, measurability, non-vacuity, sharpness).
- **Ledger**: a versioned, machine-readable, normative artifact enumerating obligations of one kind and their discharge status.
- **Gap**: an inference that is asserted but not justified. Gaps must be registered, never silent.
- **DEP-0 / DEP-1 / DEP-2**: document region classes (Chapter 5).
- **Claim status**: the epistemic status of an assertion (Chapter 5.4).
- **Completeness status**: `complete`, `partial`, `sketch`, `gap-declared`, `placeholder`, `retracted` (Chapter 5.5).
- **IGU (Inference Granularity Unit)**: the atomic unit of justification (Chapter 11.2).
- **Cold read**: reconstruction of a statement by a competent reader in the field but not the subfield, using only the document.
- **Exterminate**: block, revert, quarantine, or delete non-compliant material (Chapter 34).

---

# 4. Core laws

These laws override all other stylistic preferences. Where a later chapter is stricter, the stricter rule wins. Where a later chapter is silent, these laws apply.

## Law 1: No hidden hypotheses
Every hypothesis must appear in the statement of the result that uses it, or in a formally referenced hypothesis ledger entry that the statement cites by identifier.

Hidden hypotheses include but are not limited to:
- finiteness, countability, $\sigma$-finiteness, separability, completeness, compactness,
- nonemptiness, connectivity, simple connectivity, orientability,
- measurability, integrability, boundedness, uniform integrability, tightness,
- continuity, semicontinuity, Lipschitzness, absolute continuity, differentiability class,
- convexity, strict convexity, closedness, properness, coercivity,
- independence, stationarity, ergodicity, mixing, exchangeability, Markov property,
- commutativity, associativity, unitality, Noetherianity, reducedness, torsion-freeness,
- characteristic assumptions, algebraic closure, perfectness,
- monicity/epicity, flatness, projectivity, injectivity, exactness,
- nondegeneracy, transversality, genericity, general position,
- positivity, strict positivity, nonvanishing,
- decidability, effective axiomatizability, recursiveness, uniformity,
- characteristic-zero, unramifiedness, smoothness,
- boundary conditions, initial conditions, growth conditions, decay conditions,
- domain restrictions, branch choices, orientation choices, normalization choices.

If a hypothesis is not written down and discharged, **it does not exist**, and any proof using it is invalid.

## Law 2: No prose-only inference
Every non-trivial inference must have a justification token: a named rule, a cited result with pinpoint reference, a formal proof artifact, or a machine-checkable computation.

A prose sentence may *describe* an inference. It may not *be* the inference.

Banned as sole justification of a non-trivial step: "clearly", "obviously", "trivially", "it follows", "one checks", "a standard argument gives", "by inspection", "as is well known", "it can be shown", "left to the reader" (in DEP-0), "similarly", "analogously", "by the same reasoning" (unless the referenced step is identified by number and the substitution is given explicitly).

## Law 3: No undefined symbols
Every symbol must be declared with a sort/type and a scope before first use, and registered in the symbol registry. A symbol has exactly one meaning in its scope. Overloading requires an entry in the overload ledger with a disambiguation rule that is mechanically applicable.

## Law 4: No silent axioms
Every foundational assumption must be in the axiom ledger: AC, DC, CC, countable choice for reals, LEM, LPO, LLPO, Markov's principle, univalence, propositional resizing, large cardinal axioms, existence of inaccessible universes, `native_decide` trust, hardware/OS axioms, and any `axiom`/`Axiom`/`Parameter` declaration.

Choice-equivalents must be detected: Zorn, Tychonoff, Hahn–Banach (full), Banach–Alaoglu, existence of algebraic closures for arbitrary fields, existence of bases for arbitrary vector spaces, existence of nonprincipal ultrafilters, existence of nonmeasurable sets, well-ordering, maximal ideal existence, Krull's theorem, Stone representation.

## Law 5: No undischarged interchanges
Any exchange of two limiting operations must have an entry in the interchange ledger with a named theorem and discharged hypotheses. This includes:
$\lim \leftrightarrow \lim$, $\lim \leftrightarrow \int$, $\lim \leftrightarrow \sum$, $\lim \leftrightarrow \partial$, $\int \leftrightarrow \int$, $\int \leftrightarrow \sum$, $\sum \leftrightarrow \sum$, $\sup \leftrightarrow \inf$, $\lim \leftrightarrow \mathbb{E}$, $\partial \leftrightarrow \int$, $\mathbb{E} \leftrightarrow \sum$, $\lim \leftrightarrow \|\cdot\|$, $\otimes \leftrightarrow \lim$, $\text{colim} \leftrightarrow \lim$, $\text{Hom} \leftrightarrow \text{colim}$, $\forall \leftrightarrow \exists$, quantifier $\leftrightarrow$ limit, $\mathbb{P} \leftrightarrow \lim$, union $\leftrightarrow$ null-set.

## Law 6: No unnamed constants
Every constant, threshold, and implicit parameter must be named, and its dependency signature declared. $C$ must be $C(d, p, \varepsilon)$ or explicitly declared absolute. Reuse of a constant symbol for a different constant in one scope is banned. "Up to constants" is banned in DEP-0 without a constant ledger.

## Law 7: No unregistered gaps
An incomplete proof is permitted; a *silently* incomplete proof is not. Every gap must be registered with an identifier, an owner, a ticket, an exact statement of what is missing, a blast radius (the transitive closure of dependents), and an expiration date.

A registered gap downgrades claim status. It never leaves claim status unchanged.

## Law 8: No unverified computation
Every numerical, symbolic, or experimental result must have a reproducible artifact: code, data, environment manifest, seeds, precision policy, and a certificate or an explicit trust declaration. An unreproducible number is not a result; it is a rumor.

## Law 9: No citation laundering
A citation must point to a specific result, in a specific version, at a specific location, whose hypotheses are discharged at the point of use. Citing a survey for a theorem, citing a paper that cites a paper, citing "see e.g.", citing a result whose statement differs, or citing a conditional result as unconditional are all defects.

## Law 10: No stale references
A cross-reference that no longer resolves, a theorem number that shifted, a bibliography entry pointing to a superseded version without a version pin, a status tag that no longer matches the proof, an axiom ledger that no longer matches `#print axioms`, a notation table that no longer matches the body — all are defects.

## Law 11: No readability debt
Readability is a measured quantity with hard thresholds (Chapter 21). A proof that is valid but unreadable is not compliant. Exceeding a readability threshold is a defect of the stated severity, not a matter of taste.

## Law 12: No claim inflation
The title, abstract, introduction, and conclusion must be logically entailed by the results actually proved, at the status actually achieved, under the hypotheses actually stated. Any strengthening in the informal layers relative to the formal layers is a Severity 0 defect.

## Law 13: No orphan results
Every stated result must be used, or explicitly declared as an independent contribution with a stated purpose. Every introduced definition must be instantiated at least once. Dead definitions and unused lemmas are documentation debt and must be deleted or justified.

## Law 14: No non-vacuous-by-assertion theorems
Every DEP-0 theorem must exhibit at least one instance satisfying its hypotheses, or explicitly declare that non-vacuity is unknown, with a ticket. A theorem whose hypotheses are unsatisfiable is not a theorem; it is a tautology wearing a costume.

---

# 5. Conformance classes

DEP&CC separates three orthogonal axes: **region class** (how strict the writing rules are), **claim status** (what is epistemically achieved), and **completeness status** (how finished the artifact is). Confusing these axes is itself a defect.

## 5.1 DEP-0: Load-bearing regions
DEP-0 is the strictest class. It includes:
- main theorems and their proofs,
- every lemma, proposition, and corollary in the transitive dependency closure of a main theorem,
- all definitions used in DEP-0 statements,
- all constructions whose well-definedness is load-bearing,
- all cryptographic security reductions,
- all safety-critical guarantees,
- all complexity upper and lower bounds claimed as results,
- all formal statements intended to correspond to prose theorems,
- all statistical claims presented as findings.

**DEP-0 requirements (summary; expanded in Chapters 8–20):**
- Every hypothesis in the statement, with an identifier, discharged or explicitly marked unused with reason.
- Every step at most 1 IGU (Chapter 11.2).
- Every symbol in the registry with sort and scope.
- Every constant named with dependency signature.
- Every interchange in the ledger.
- Every WLOG accompanied by a reduction proof.
- Every induction with measure, well-foundedness proof, base cases, and all cases.
- Every case analysis with an exhaustiveness argument.
- Every construction with a well-definedness obligation discharged.
- Non-vacuity witness present.
- Degeneracy battery executed and recorded (Chapter 30.3).
- Sharpness status declared for every hypothesis.
- Axiom ledger complete; machine-extracted where a formalization exists.
- Claim status explicit and never inflated.
- Full annotation block (Chapter 32).
- Readability thresholds of Chapter 21 met with no waiver.
- No forward references except to a declared roadmap.
- Zero `sorry`, `admit`, `Admitted`, `oops`, `abort`, `_axiom`, `postulate` in associated formal artifacts.

## 5.2 DEP-1: Supporting and derived regions
DEP-1 includes:
- lemmas not in the load-bearing closure but stated as results,
- routine verifications, computations, and standard reductions,
- extended examples and applications,
- appendix proofs of standard facts included for completeness,
- experimental methodology and analysis sections,
- algorithm descriptions and their correctness arguments where not load-bearing,
- extended tables, extended data analysis.

DEP-1 **may**:
- compress routine algebra into a single step with a CAS certificate or an explicit "expand and collect" instruction,
- cite standard results without restating hypotheses, **provided** the hypothesis discharge is recorded in the ledger,
- use "similarly" **provided** the referenced step number and the substitution mapping are given,
- defer proofs to an appendix,
- use `sketch` claim status with a registered gap.

DEP-1 **must still** satisfy Laws 1–14, the symbol registry, the convention manifest, the constant ledger, and the annotation block. DEP-1 relaxes *granularity*, never *validity*.

## 5.3 DEP-2: Expository regions
DEP-2 includes:
- abstract-adjacent motivation (but see Law 12: the abstract itself is DEP-0 for claim status),
- introduction narrative, historical remarks, intuition,
- proof overviews and roadmaps,
- discussion, limitations, future work, open problems,
- acknowledgements, related-work prose,
- pedagogical asides, informal examples clearly marked as informal.

DEP-2 **may** use informal language, heuristics, pictures without proof, analogies, and non-rigorous reasoning.

DEP-2 **must**:
- be visually and structurally separated from DEP-0/DEP-1 (dedicated environment, e.g. `\begin{depintuition}`),
- never contain a load-bearing inference,
- never introduce notation used later in DEP-0 without re-declaration in DEP-0,
- never state a claim without a claim status,
- never state a stronger claim than the DEP-0 results entail.

**The DEP-2 containment rule:** if removing every DEP-2 region from the document leaves any DEP-0 proof incomplete, the document is non-compliant. This is mechanically checkable via the dependency graph: no DEP-0 node may have a DEP-2 dependency.

## 5.4 Claim status vocabulary (closed set)
Exactly one status per claim. No other values are permitted.

| Status | Meaning | Minimum evidence |
|---|---|---|
| `machine-checked` | Kernel-verified in a pinned proof assistant, zero admitted steps, axiom ledger extracted | Artifact ID + kernel version + axiom dump + statement-fidelity audit |
| `proved` | Complete human-checked proof meeting DEP-0 | Full proof + all ledgers discharged + degeneracy battery |
| `proved-modulo` | Complete except for explicitly registered external results or gaps | Gap register entries + blast radius |
| `conditional` | Proved under a named unproved hypothesis (RH, P≠NP, conjecture X) | The hypothesis stated as a hypothesis in the theorem statement |
| `verified-numeric` | Established by certified computation over a declared finite domain | Certificate + interval/exact arithmetic + domain declaration |
| `empirical` | Supported by experiment/statistics, not deduction | Pre-registration or exploratory declaration + artifact + statistical analysis |
| `sketched` | Proof outline only; not a proof | Registered gap + owner + expiration |
| `conjectural` | Asserted as a conjecture, no proof | Explicit conjecture environment |
| `heuristic` | Non-rigorous reasoning, DEP-2 only | Containment in DEP-2 |
| `retracted` | Previously asserted, now withdrawn | Retraction record + dependent invalidation |

**Status transition rules:**
- Upgrading status requires new evidence and a review record. Silent upgrades are Severity 0.
- `sketched` $\rightarrow$ `proved` requires closing every registered gap for that node.
- `empirical` may never become `proved` without a proof.
- `verified-numeric` may never be described as `proved` for an infinite domain.
- `conditional` may never drop its condition in the abstract, title, or contribution list.

## 5.5 Completeness status vocabulary (closed set)

| Status | Meaning | Obligations |
|---|---|---|
| `complete` | All obligations discharged, all ledgers closed, reviewed | None outstanding |
| `partial` | Valid for a declared subset; missing cases enumerated | Missing-case list + owner + ticket |
| `sketch` | Outline; not usable as a dependency by DEP-0 | Gap IDs + owner + expiration |
| `gap-declared` | A specific inference is missing; everything else complete | Gap ID + blast radius + expiration |
| `placeholder` | Reserved statement, no proof, not referenced by DEP-0 | Must be unreferenced; lint-enforced |
| `retracted` | Withdrawn | Invalidation propagation completed |

A DEP-0 node with completeness status other than `complete` **must not** be depended upon by a node claiming `complete`. This is the **status contamination rule** and is mechanically enforced on the dependency DAG.

---

# 6. Toolchain and build requirements

## 6.1 Pinned toolchain
The document must build with a pinned toolchain. Required manifest `dep/toolchain.lock`:
```yaml
tex_distribution: texlive-2025
latex_engine: lualatex
engine_version: 1.18.0
latexmk_version: 4.85
biber_version: 3.10
dep_macros_version: 1.0.0
python: 3.12.7
lean: 4.14.0
mathlib_commit: 8f3a2c1e9b7d4f60a1c2e3d4f5a6b7c8d9e0f1a2
z3: 4.13.0
sagemath: 10.4
lockfile_hash: sha256:...
```
Unpinned dependencies, mutable git branches, `latest` tags, and "works on my machine" are banned.

## 6.2 Deterministic build
Identical source + toolchain + manifest must produce a byte-identical PDF, except for intentionally embedded version metadata declared in the manifest.

Builds must not depend on: locale, timezone, current date/time (unless `\depbuilddate` is explicitly enabled and recorded), absolute paths, username, hostname, file iteration order, hash seeds, network access, or environment variables not declared in the manifest.

Required: `SOURCE_DATE_EPOCH` pinned; `\pdftrailerid` fixed; font subsetting deterministic; bibliography ordering deterministic (sorting scheme declared).

## 6.3 Zero-tolerance compilation
- Zero errors.
- Zero undefined references.
- Zero undefined citations.
- Zero overfull hboxes exceeding `1.0pt` in DEP-0 regions.
- Zero multiply-defined labels.
- Zero missing glyph warnings.
- Warnings-as-errors for the `dep` macro package's own diagnostics.

## 6.4 Banned build features
- `-shell-escape` / `\write18` in release builds (external tool results must be pre-computed, hashed artifacts).
- `\input` of files outside the repository.
- Network fetches during build.
- Non-deterministic `\random`-like primitives.
- Manual editing of generated `.bbl`, `.aux`, `.toc`, or generated tables.
- Commented-out source blocks (use version control).

## 6.5 Formal artifact CI
For every formalization referenced by the document, CI must run on every commit:
1. Build with pinned toolchain and pinned library commit.
2. Kernel-check all declarations.
3. Extract axiom ledgers for every theorem cited by the document; archive the dump.
4. Assert zero admitted-proof tokens (Chapter 19.2).
5. Assert the axiom set equals the declared axiom ledger (drift is Severity 0).
6. Run the statement-fidelity audit mapping (Chapter 19.5).
7. Check elaboration time budget (Chapter 19.7).
8. Reproduce all numerical artifacts and compare hashes/tolerances.

## 6.6 Required generated artifacts
Every build must emit, into `dep/out/`:
- `symbols.json` — the symbol registry as used, with declaration sites and scopes.
- `dag.json` — the full result dependency graph, with claim/completeness statuses.
- `hypotheses.json` — hypothesis declarations and discharge sites.
- `constants.json` — constant ledger with dependency signatures.
- `interchanges.json` — interchange ledger.
- `axioms.json` — axiom ledger, merged with machine extraction where available.
- `gaps.json` — gap register with blast radii and expirations.
- `readability.json` — all Chapter 21 metrics per region.
- `claims.json` — every claim in title/abstract/intro/conclusion mapped to result IDs.
- `degeneracy.json` — degeneracy battery results per DEP-0 node.
- `citations.json` — pinned citations with version, locator, retraction-check timestamp.

A build that cannot emit these artifacts is not DEP-compliant. These are the enforcement substrate for Chapter 33.

---

# Part I — The language of mathematics: permission policy

**General rule for Part I:** if a construct is not explicitly allowed here, it is restricted in DEP-0 until its obligations are enumerated and discharged.

---

# 7. Notation and symbol discipline

## 7.1 The symbol registry
Every document must maintain `dep/symbols.yaml`. Every symbol used in DEP-0 or DEP-1 must have an entry.

```yaml
- id: sym.measure.mu
  glyph: '\mu'
  sort: 'Measure on (X, Sigma)'
  kind: measure
  scope: global
  declared_at: 'sec.prelim.def.measure_space'
  convention_refs: [conv.measure.complete, conv.sigma_algebra]
  overload: none
  first_use: 'sec.prelim.def.measure_space'
  notes: 'Always sigma-finite when integrated against; see H2.'

- id: sym.constant.C_sobolev
  glyph: 'C_{\mathrm{S}}'
  sort: 'Real, positive'
  kind: constant
  depends_on: [d, p, Omega]
  scope: 'sec.sobolev'
  declared_at: 'sec.sobolev.lem.embedding'
  uniform_in: [u]
  effective: false
  notes: 'Ineffective; obtained by compactness contradiction.'
```

**Rules:**
- One glyph, one meaning per scope. Scope must be `global`, `section:<id>`, or `proof:<id>`.
- A symbol may not be re-bound in a nested scope if it is free in an enclosing scope's live obligations (no shadowing of live symbols).
- Every symbol must declare its **sort** (type), not merely its name. "$f$ a function" is insufficient; "$f : X \to Y$, measurable" is required.
- Greek/Latin/blackboard/fraktur/script alphabets are semantically reserved per the convention manifest. Mixing $\mathfrak{g}$ and $g$ for unrelated objects is allowed; using $\mathfrak{g}$ for two unrelated Lie algebras is not.
- Subscripts and superscripts must have declared semantics. $x_i$ (index), $x^{(k)}$ (iteration), $x^k$ (power), $x_k$ (sequence element) must not be conflated. If both iteration and power appear, iteration **must** use parenthesized superscripts.
- Decorations ($\sim$, $\hat{}$, $\bar{}$, $'$, $*$, $\dagger$, $\circ$) must be declared once and used consistently. $*$ may not simultaneously denote dual, adjoint, convolution, Kleene star, and optimal value in one document.

## 7.2 Overload ledger
Overloading is permitted only with a mechanically applicable disambiguation rule.

| Glyph | Common overloadings | DEP&CC policy |
|---|---|---|
| $|\cdot|$ | cardinality, absolute value, norm, measure, determinant, order of element, divides | **Banned** unqualified in DEP-0. Use `\card`, `\abs`, `\norm`, `\meas`, `\det`, `\ord`. $a \mid b$ for divisibility must be `\divides` with distinct spacing. |
| $\subset$ | subset, proper subset | **Banned**. Use `\subseteq` and `\subsetneq`. |
| $(\cdot,\cdot)$ | inner product, pair, tuple, ideal generated, gcd, open interval | Restricted; declare one primary use; others must use distinct delimiters (`\ip`, `\pair`, `\ideal`, `\gcd`, `\oo`). |
| $\ll$ | asymptotic domination, absolute continuity, much less than | Restricted; `\llasymp` vs `\abscont` must be distinct macros. |
| $\sim$ | asymptotic equivalence, equinumerosity, equivalence relation, distributed as | **Banned** unqualified. `\asym`, `\eqcard`, `\simrel`, `\distas`. |
| $\cong, \simeq, \equiv$ | isomorphism, natural iso, homotopy, congruence, definitional equality | Each must be declared; natural isomorphism must be distinguishable from mere isomorphism. |
| $\otimes$ | tensor product, Kronecker product, convolution variant | Declare; index by category/ring where ambiguous (`\otimes_R`). |
| $\mathbb{E}$ | expectation, energy, edge set, exceptional divisor | Declare per scope; expectation must carry the measure: `\mathbb{E}_{\mathbb{P}}`. |
| $\mathbb{P}, \mathbb{Q}$ | probability measures, polynomials, projectives, parabolic subgroups | Distinct fonts required if co-occurring. |
| $d$ | dimension, differential, metric, degree, exterior derivative | Differential must be `\dd`; metric `\dist`; dimension `\dim`; degree `\deg`. |
| $O$ | big-O, orthogonal group, zero object, orbit | `\bigo`, `\Orth`, `\zeroobj`, `\orbit`. |
| $\log$ | base e, 2, 10 | Base must be declared in convention manifest and written explicitly when not the declared default. |
| $\mathbb{N}$ | with/without 0 | Must be `\NNzero` or `\NNpos`, or the manifest must fix it and `\NN` expands to the fixed one. |
| $[\cdot]$ | closed interval, commutator, Iverson bracket, equivalence class, index set | Declare; Iverson bracket must be `\iverson`. |

## 7.3 Notation locality: the two-page rule
In DEP-0, a reader must never need to look back more than **two pages** to find a symbol's declaration, unless the symbol is in the document's **Notation Table** (Chapter 23.4) *and* the section preamble re-declares it.

Mechanically: for each symbol occurrence, `notation_distance <= 2 pages` OR (`in_notation_table` AND `redeclared_in_section_preamble`). Violation is Severity 2 (first occurrence), Severity 1 (repeated).

## 7.4 Abuse-of-notation ledger
Abuse of notation is permitted only when registered.

```latex
\DepAbuse{abuse.function_on_classes}{
  We write $f([x])$ for $f(x)$ when $f$ is constant on equivalence classes.
}{
  Justification: \DepRef{lem.well_defined_f}.
  Disambiguation rule: applies only when the argument is syntactically a class representative.
}
```

Required fields: the abuse, the precise meaning, the justification (usually a well-definedness lemma), and a mechanical disambiguation rule. Unregistered abuse is Severity 1.

**Banned abuses (never permitted in DEP-0):**
- Identifying a measure with its density without declaring absolute continuity.
- Identifying a function with its a.e.-equivalence class while making pointwise claims.
- Identifying a random variable with its distribution while making a.s. or pathwise claims.
- Identifying isomorphic objects while making claims that are not isomorphism-invariant.
- Writing $=$ for $\cong$ in a claim about equality of objects rather than isomorphism of objects.
- Writing $\in$ for $\subseteq$.
- Suppressing a coercion that is not injective.
- Writing $f(x)$ for $f(\{x\})$ when $f$ is only defined on sets and singleton behavior matters.
- Silent identification of a space with its dual without reflexivity proof.

## 7.5 Macro discipline
- All semantic content must be carried by named macros from the `dep` package or a declared project macro file. Direct glyph entry for semantic objects is banned in DEP-0.
- Macros must be *semantic*, not *typographic*: `\norm{x}` not `\|x\|`; `\Prob` not `P`.
- Macros must not take hidden arguments or expand to different meanings in different environments.
- `\newcommand` only; `\def`, `\renewcommand` on `dep` macros, and `\let` rebinding of semantic macros are banned outside the preamble.
- Every project macro must have a registry entry stating its expansion, sort, and scope.

---

# 8. Definitions

## 8.1 Required form
Every definition must be issued in a `depdefinition` environment with the following structure:

```latex
\begin{depdefinition}[
  id=def.uniform_integrability,
  class=DEP-0,
  status=complete,
  kind=property,
  ambient={\DepRef{def.prob_space}},
  symbols={sym.family.F, sym.measure.P},
  axioms={},
  evidence={std:Billingsley-1995:sec4.5},
]
Let \DepHyp{H1}{$(\Omega,\cF,\mathbb{P})$ be a probability space} and let
\DepHyp{H2}{$\mathcal{F} \subseteq L^1(\mathbb{P})$ be a family}.
We say $\mathcal{F}$ is \emph{uniformly integrable} if
\[
  \lim_{K\to\infty}\ \sup_{X\in\mathcal{F}}\ \mathbb{E}_{\mathbb{P}}\!\abs{X}\,\iverson_{\abs{X}>K} = 0 .
\]
\end{depdefinition}
```

## 8.2 Obligations generated by a definition
Every definition generates obligations that must be discharged or explicitly marked inapplicable:

| Kind of definition | Generated obligations |
|---|---|
| **Property** (predicate) | Non-vacuity (an instance satisfying it) and non-triviality (an instance failing it). Both are mandatory in DEP-0. |
| **Object by explicit construction** | Well-definedness; the construction lands in the declared codomain. |
| **Object by implicit condition** (e.g. "the unique $x$ such that ...") | Existence **and** uniqueness, proved before use, or the definition must be reformulated with a choice operator plus a choice-ledger entry. |
| **Object by quotient** | The equivalence relation is an equivalence relation; the operation is well-defined on classes (independence of representative). |
| **Object by choice** | Choice ledger entry; AC/DC/CC classification; canonicity status declared. |
| **Object by limit / colimit** | Existence of the limit in the declared category; convergence mode; independence of presentation. |
| **Recursive definition** | Well-foundedness of the recursion; termination; uniqueness of the solution; the recursion is on a declared measure. |
| **Partial function** | Domain of definition characterized exactly; behavior outside domain declared (undefined, not zero). |
| **Notation-introducing** | Registry entry; no collision; scope declared. |
| **Parameterized family** | Behavior at degenerate parameter values ($0$, $1$, $\infty$, empty index set) declared. |

## 8.3 Definitional conservativity
A definition must not smuggle in an existence claim, a theorem, or a substantive assumption.

**Banned:**
```latex
Definition. Let W be the largest element of S.   % existence not proved
Definition. A group is a set G with operation such that G is nonempty and ... . % fine
Definition. The canonical basis of V.           % existence of a basis needs AC; canonicity false
```

If a definition requires a nontrivial theorem for its well-definedness, the theorem must precede it and be referenced. The dependency graph must record this as a hard dependency.

## 8.4 Mandatory examples
Every DEP-0 definition must be accompanied by:
1. At least one **example** satisfying it (non-vacuity witness).
2. At least one **non-example** (a near-miss that fails exactly one clause), or a declaration that the property is universally satisfied.
3. At least one **degenerate instance** from the Degeneracy Battery (Chapter 30.3), or a declaration of why none applies.

A definition without a non-example is a definition the reader cannot calibrate. Severity 2, escalating to Severity 1 for definitions with $\ge 3$ clauses.

## 8.5 Definition–terminology lock
Once a term is defined, it must be used with exactly that meaning. Synonym rotation is banned: if "uniformly integrable" is defined, the text may not later say "equi-integrable", "uniformly summable", or "tight in $L^1$" for the same notion without an explicit alias declaration in the registry.

---

# 9. Statements

## 9.1 Environment taxonomy
Use exactly these environments, with exactly these meanings:

| Environment | Meaning | Obligation |
|---|---|---|
| `deptheorem` | A main result | Full DEP-0 |
| `deplemma` | A result whose purpose is to prove a named later result | Must declare `\DepServes{thm.id}` |
| `depproposition` | A result of independent interest, not main | DEP-0 or DEP-1 |
| `depcorollary` | A result following from named results by $\le 3$ IGU | Must declare parents; proof $\le 3$ IGU or reclassify |
| `depclaim` | A local assertion inside a proof | Must be proved within the proof; scope-local |
| `depconjecture` | Unproved assertion, status `conjectural` | Must not be depended on by `complete` nodes |
| `depquestion` | Open problem | No claim |
| `depobservation` | Immediate consequence, $\le 1$ IGU | Must be $\le 1$ IGU |
| `depexample` | Instance | Must verify the property it instantiates |
| `depcounterexample` | Refutation | Must verify the failure precisely |
| `depdefinition` | Definition | Chapter 8 |
| `depconvention` | Convention fixing | Must be in the manifest |
| `depremark` | Commentary | DEP-2 |
| `depintuition` | Informal reasoning | DEP-2, contained |

Misuse of environment to lower obligations (e.g. calling a main theorem a "remark", or a 5-page proof a "corollary") is Severity 1.

## 9.2 Statement self-containment
A DEP-0 statement must be reconstructible by a cold read. Concretely:
- All quantified variables appear with domains in the statement.
- All hypotheses appear as numbered `\DepHyp` items in the statement.
- All ambient structure is either in the statement or in a `\DepAmbient{}` declaration referencing a convention-manifest entry that is *fixed for the whole document*.
- The conclusion is a single, syntactically identifiable formula or a numbered list of formulas.
- No hypothesis appears only in the proof.
- No hypothesis appears only in the section preamble unless the section preamble is a `\DepAmbient` block and the statement cites it.

**Banned statement patterns:**
```latex
Theorem. Under suitable regularity assumptions, the solution is unique.
Theorem. Let f be nice. Then ...
Theorem. For large n, ...                 % threshold and dependencies missing
Theorem. The conclusion of Lemma 3.2 holds. % not self-contained
Theorem. generically, ...                   % generic in what topology/measure?
Theorem. If the above conditions hold, ...   % "above" is not an identifier
```

## 9.3 Quantifier placement
Quantifiers must be front-loaded and explicitly ordered. Trailing quantifiers ("... for all $x$") are permitted only when the formula contains at most one quantifier.

Required canonical form:
> For all <universally quantified vars with domains>,
> there exists <existentially quantified vars with domains and dependency signature>,
> such that <quantifier-free or bounded-quantifier matrix>.

Existential witnesses must declare their dependencies: $\exists C = C(d,p) \; \forall n \ge N_0(d,p)$ — never $\forall n \exists C$ when $C$ is meant to be uniform.

**Quantifier-order audit (mandatory, mechanical):** the annotation block must record the quantifier prefix as a string, e.g. `A E A E` with domains, and the proof must be checked to establish that order. Swapping $\forall\exists$ to $\exists\forall$ anywhere between statement, proof, abstract, and contribution list is Severity 0.

## 9.4 Uniformity declaration
Every bound, convergence, continuity, or estimate must declare uniformity explicitly:
```latex
\DepUniformity{
  uniform_in = {u \in B},
  pointwise_in = {x \in Omega},
  constants_depend_on = {d, p, \lip(f)},
  effective = false,
  reason_ineffective = {compactness contradiction, \DepRef{lem.contradiction_compact}}
}
```
"Uniform" without `uniform_in` is banned. "Continuous" without specifying the topology on domain and codomain is banned when more than one topology is in play.

## 9.5 Effectivity declaration
Every existence claim must be classified:
- `constructive`: an algorithm or explicit formula is given; complexity declared if computational.
- `effective`: a computable bound is given, possibly impractical.
- `ineffective`: existence proved without a computable bound (compactness, contradiction, non-constructive choice). Must state the reason.
- `non-constructive-axiomatic`: relies on AC or equivalent; ledger entry required.

An ineffective constant may not be used in a claimed algorithmic or numerical result. That is Severity 0.

---

# 10. Quantifiers and logic

## 10.1 Binding and scope
- Every variable occurrence is bound by exactly one binder, or is free and declared in the ambient block.
- Capture-avoiding substitution is mandatory; when a substitution is performed in a proof step, the renaming must be shown if any binder is involved.
- Bound variable names must not shadow free variables of the enclosing goal.
- In DEP-0, the same letter may not be used as a bound variable in two nested binders.

## 10.2 Nesting and alternation limits (readability-enforced)

| Metric | DEP-0 limit | DEP-1 limit |
|---|---|---|
| Quantifier alternations in one display | 3 | 4 |
| Nested quantifier depth in inline text | 1 | 2 |
| Quantifiers in a single inline sentence | 2 | 3 |
| Free variables in one display | 6 | 8 |

Exceeding a limit requires either restructuring (introducing a named predicate/definition) or a waiver. "For every $\varepsilon>0$ there is $N$ such that for all $n\ge N$ there is $M$ such that for all $m\ge M$ ..." must be factored through a definition.

## 10.3 Banned or restricted quantifier phrases

| Phrase | Status | Required replacement |
|---|---|---|
| "for any" | **Banned** in DEP-0 | "for every" or "for some", explicitly |
| "for sufficiently large $n$" | Restricted | $\exists N_0 = N_0(\text{deps}) \; \forall n \ge N_0$, with deps declared |
| "for $n$ large enough" | **Banned** | as above |
| "almost all" | Restricted | "all but finitely many" / "for $\mu$-a.e." / "outside a meagre set" — must say which |
| "almost every" | Restricted | measure named |
| "almost surely" | Restricted | probability measure named; `a.s.` attached to the claim, not the paragraph |
| "generically" | Restricted | Zariski-open dense / comeagre / full measure — specify, and specify the ambient space |
| "typically" | **Banned** in DEP-0 | quantify |
| "in general" | Restricted | state the general claim or the exception |
| "eventually" | Restricted | in what order/filter, with threshold |
| "arbitrarily large" | Restricted | $\forall M \exists n > M$ |
| "all sufficiently small $\varepsilon$" | Restricted | $\exists \varepsilon_0 \; \forall \varepsilon \in (0,\varepsilon_0)$ |
| "some" | Restricted | existential with domain |
| "arbitrary" | Restricted | universal with domain; not a substitute for a choice |
| "fixed" | Restricted | must say fixed before or after which quantifier |

## 10.4 Vacuity and emptiness
Every universally quantified statement over a possibly-empty domain must have emptiness handled explicitly. Every existentially quantified statement must have nonemptiness of the domain established.

Mandatory checks recorded in the annotation block:
- empty index set, empty sum ($= 0$), empty product ($= 1$), empty supremum ($= -\infty$ or declared), empty infimum,
- $n = 0$, $n = 1$, dimension zero,
- zero measure, zero function, zero ring, trivial group, empty category, empty type,
- degenerate distribution (point mass), deterministic random variable,
- $p = 1$, $p = \infty$, $p = 0$ in $L^p$ scales,
- equality case in every inequality used.

## 10.5 Negation and classical steps
- The negation of the goal must be written explicitly when starting a proof by contradiction, with quantifiers correctly dualized. This is a mandatory proof line, not an implicit move.
- Contrapositive proofs must state the contrapositive explicitly.
- Proofs by contradiction that establish only $\neg\neg P$ must be marked as using LEM in the axiom ledger if the ambient logic is not declared classical.
- "It is not the case that all ..." must be converted to an explicit existential before use.
- Double-negation elimination, excluded middle, and proof by cases on an undecidable predicate each generate an axiom-ledger entry in constructive or unspecified settings.

## 10.6 Object language / metalanguage
In logic papers:
- Object-language formulas must be typographically distinguished from metalinguistic formulas (e.g. `\olformula{}` vs plain).
- Quotation/ Gödel-numbering must use a distinct macro; $\ulcorner \varphi \urcorner$ must not be conflated with $\varphi$.
- Provability $\vdash$, semantic entailment $\models$, and metatheoretic implication $\Rightarrow$ must be distinct macros and never conflated.
- The theory must be named at every $\vdash$ (e.g. `\provesin{PA}`), not left implicit.
- Soundness/completeness/compactness may only be invoked for logics where they hold, with the logic named.
- Incompleteness theorems require: effective axiomatizability, sufficient arithmetic (specify: interprets $Q$, or $I\Sigma_1$, or $PA$), and the relevant soundness assumption (consistency vs $\Sigma_1$-soundness vs $\omega$-consistency) — each discharged.
- Löb's theorem requires the derivability conditions D1–D3 to be verified for the specific provability predicate.

---

# 11. Proof structure

## 11.1 The proof DAG
Every proof is a directed acyclic graph of numbered steps. Requirements:
- Every step has an identifier `S<k>` local to the proof.
- Every step declares its premises: earlier steps, hypothesis IDs, or external result IDs.
- The final step must be the goal, syntactically identical to the statement's conclusion (modulo declared definitional unfolding).
- No step may depend on a later step. Cycles are Severity 0.
- No step may depend on a DEP-2 region.
- Fan-in per step $\le 5$ in DEP-0 (a step citing 6 results is too large; split it).
- Total proof length in DEP-0: if a proof exceeds **3 pages** or **40 steps**, it must be decomposed into lemmas with their own annotation blocks. Waiver required otherwise.

## 11.2 Inference Granularity Unit (IGU)
One IGU is exactly one of:
1. One application of one named inference rule or one cited theorem (with hypotheses discharged, possibly by reference to earlier steps).
2. One algebraic identity verifiable by a decision procedure (`ring`, `linarith`, `nlinarith`, `field_simp`, a CAS certificate) — the procedure must be named.
3. One definition unfolding (named definition).
4. One case split introduction (the split itself; each case is then separately developed).
5. One instantiation of a universally quantified earlier step with explicit terms.
6. One application of a declared, registered abuse of notation.
7. One monotonicity/majorization step in an inequality chain with a named justification.

**DEP-0 rule: at most 1 IGU per numbered step.** DEP-1: at most 3, and the constituent IGUs must be enumerable on request.

A step that says "by Theorem 2.1, Hölder, and Young's inequality, we obtain (4.7)" is 3 IGU and is Severity 1 in DEP-0.

## 11.3 Justification tokens
Every step must carry exactly one justification form:
```latex
\DepStep{S7}{
  \norm{f}_{L^p} \le \norm{g}_{L^p}
}{
  by = {thm.dominated_convergence},
  uses = {H2, H4, S3, S6},
  discharges = {dc.domination, dc.ae_convergence, dc.measurability},
}
```
Permitted `by` values: a result ID, a named rule from the fixed rule table (Appendix F), a decision procedure name, `definition:<id>`, `hypothesis:<id>`, `algebra:<procedure>`, `case-analysis`, `induction-hypothesis`.

**Banned `by` values:** `clear`, `obvious`, `standard`, `routine`, `computation`, `similar`, `well-known`, `elementary`, `classical` (as a justification rather than an axiom reference), `direct`, `immediate` (unless the step is $\le 1$ definition unfolding).

## 11.4 Induction discipline
Every induction must declare:
```latex
\DepInduction{
  measure = {\card{V(G)}},
  order = {well-founded on NN},
  wf_proof = {std:NN_well_founded},
  kind = {strong},
  on = {n},
  generalized = {m, H},        % parameters generalized before induction
  fixed = {\Omega},            % parameters held fixed; must be safe
  base_cases = {n=0, n=1},
  step_cases = {S4, S5, S6},
  limit_case = {not applicable, order type omega},
  ih_statement = {S3},
}
```
**Mandatory checks:**
- **Induction loading:** every parameter that varies during the induction must be generalized in the induction hypothesis. The classic defect — proving $P(n, m)$ by induction on $n$ while $m$ is fixed but changes in the recursive call — is Severity 0.
- **Base case coverage:** the base cases must cover all minimal elements of the well-founded order. For structural induction, all constructors. For transfinite induction, zero, successor, **and limit** cases.
- **Measure decrease:** every recursive invocation must strictly decrease the measure, proved, not asserted.
- **Simultaneous/mutual induction:** the joint statement must be written explicitly; you may not induct on $P$ while secretly using $Q$.
- **Nested induction depth $\le 2$** in DEP-0; deeper requires factoring into lemmas.
- **Infinite descent** must exhibit the well-founded measure explicitly.

## 11.5 WLOG discipline
Every "without loss of generality" must be accompanied by a reduction:
```latex
\DepWlog{
  assumption = {x_1 \le x_2 \le \dots \le x_n},
  reduction = {S2},
  invariance = {S1},           % proof that the goal is invariant under the reduction
  group_action = {symmetric group S_n permuting coordinates},
  orbit_representative = {sorted tuple},
}
```
Required: (a) the transformation, (b) proof that the goal and all hypotheses are invariant (or that the transformed instance implies the original), (c) proof that every instance is reducible.

**Banned WLOG:**
- WLOG by "symmetry" when the goal is not symmetric in the relevant arguments.
- WLOG by scaling when the goal is not scale-invariant, or when the constant's dependence on the scaling is then dropped.
- WLOG "by density" without proving the property is closed under the relevant limit.
- WLOG "by translation" in a non-translation-invariant setting.
- WLOG normalization that destroys a hypothesis (e.g. normalizing $\|x\|=1$ when $x=0$ is possible).

## 11.6 Case analysis
- Cases must be enumerated in a table with an **exhaustiveness proof**: the disjunction of case conditions must be proved to hold.
- Cases must be either disjoint (and declared) or overlapping (and each overlap resolved).
- Each case must terminate in the goal or a contradiction; a case that "is similar" must give the substitution mapping explicitly and the referenced case number.
- **Open case count $\le 3$** at any point in DEP-0 (cognitive stack limit, Chapter 21).
- Boundary cases must be separate cases, not folded into the interior argument.

## 11.7 Inequality chains
Every relation in a chain must be labelled with its justification. Unlabelled relations are banned in DEP-0.
```latex
\begin{depcchain}
\norm{Tf}_{L^q}
  &\le \norm{K}_{L^r}\norm{f}_{L^p}   && \text{[Young's convolution ineq.; \DepUse{H1},\DepUse{H2}; } 1/p+1/r = 1+1/q \text{ checked in S2]}\\
  &\le C(d,p)\,\norm{f}_{L^p}          && \text{[S3: kernel bound; constant } C(d,p) \text{ registered]}\\
  &= \text{RHS of } \DepRef{eq.goal}.  && \text{[definition of } C \text{, S1]}
\end{depcchain}
```
Rules:
- Mixed $\le$, $<$, $=$, $\lesssim$ in one chain must be resolved to the weakest relation, and the final relation must match the goal ($<$ vs $\le$ matters).
- $\lesssim$, $\ll$, $O(\cdot)$ in a chain require a constant-ledger entry and a declared uniformity.
- Every chain must be checkable by concatenation; a chain with a hidden additive constant is Severity 0.
- Chains longer than **5 relations** must be split.

## 11.8 Equivalences
An `iff` proof must have two explicitly labelled directions ($\Rightarrow$ and $\Leftarrow$), or a chain of equivalences where every link is an equivalence with justification. A chain that secretly uses $\Rightarrow$ in one link and claims $\Leftrightarrow$ is Severity 0. Circular chains ("(i)$\Rightarrow$(ii)$\Rightarrow$(iii)$\Rightarrow$(i)") must declare the cycle and prove every link.

## 11.9 Constructions and existence
An existence proof by construction must include a **verification block**: the constructed object is shown to satisfy every clause of the required property, clause by clause, with clause IDs. "One checks that $f$ has the required properties" is Severity 1.

## 11.10 Contradiction and minimality
- Minimal counterexample arguments must prove the minimum exists (well-ordering / well-foundedness), not merely the infimum.
- Extreme value arguments must prove attainment (compactness + semicontinuity, or finiteness), with hypotheses discharged.
- "Take a maximal element" requires Zorn's hypotheses (every chain has an upper bound) verified, plus an AC ledger entry.

## 11.11 Diagonalization and subsequences
- Every subsequence extraction must introduce a new index symbol or an explicit `\DepSubseq` declaration; silently reusing $n$ is banned in DEP-0.
- Nested subsequence extraction must be tracked; a diagonal argument must state the diagonal explicitly and prove it is a subsequence of each row after finitely many terms.
- Countability of the family being diagonalized must be stated.

## 11.12 QED discipline
- Every proof ends with `\end{depproof}` which mechanically checks that the last step's conclusion matches the goal.
- Proofs of nested claims must place `\qedhere` correctly; a floating qed after a display is a typographic defect (Severity 3) and a structural defect if it hides an unfinished case (Severity 1).
- A proof ending in a display equation, an enumeration, or a figure must use the checked closing macro.

---

# 12. Constants, parameters, and asymptotic bookkeeping

## 12.1 Constant ledger
```yaml
- id: const.C_embedding
  glyph: 'C_{\mathrm{emb}}'
  value_kind: symbolic
  depends_on: [d, p, \mathrm{Lip}(\partial\Omega)]
  uniform_in: [u, f]
  sign: positive
  finite: proved
  finite_proof: lem.embedding_bound
  effective: false
  scope: sec.sobolev
  reuse_policy: unique
```
**Rules:**
- Generic $C$, $c$, $C'$, $C_1$, $C_2$ are banned in DEP-0 unless declared as *scoped disposable constants* with an explicit convention: "In this proof, $C$ denotes a positive constant depending only on $(d,p)$, whose value may change between occurrences." This declaration must be present, must be in the manifest, and must not be used across proofs.
- If a disposable constant appears in the **statement** of a result, it is banned. Statements require named constants with declared dependencies.
- A constant may not silently acquire a dependence. If step `S7` introduces a dependence on $\varepsilon$, every subsequent use must show $C(\varepsilon)$.
- Constants absorbed into $O(\cdot)$ must be recorded; $O(\cdot)$ may not hide a parameter dependence.
- Small parameters $\varepsilon, \delta, \eta$ must have a **choosing order** declared: "choose $\delta$ depending on $\varepsilon$, then $N$ depending on $(\varepsilon,\delta)$". Circular parameter choice is Severity 0.

## 12.2 Epsilon management
Every $\varepsilon$-argument must include a **parameter selection block** at the start or end, listing the order of choices and the final substitution that yields the claimed bound (e.g. "apply with $\varepsilon' = \varepsilon/(3C)$, then $\delta = \delta(\varepsilon')$, then $N = \max(N_1,N_2)$").

The final constant must be tracked: ending with $3C\varepsilon$ and claiming $\varepsilon$ requires the explicit rescaling line. Silently relabelling $3C\varepsilon$ as $\varepsilon$ is permitted only with the declared disposable-epsilon convention and only if the goal is $\forall\varepsilon>0$. It is banned if the goal has a fixed $\varepsilon$.

## 12.3 Asymptotic notation
| Notation | Required declaration |
|---|---|
| $f = O(g)$ | limit variable and limit point; uniformity in all other parameters; the implied constant's dependencies |
| $f = o(g)$ | same; plus whether $g$ may vanish (and the convention if so) |
| $f = \Theta(g)$ | both bounds, with both constants |
| $f \ll g$ | whether Vinogradov or "much less than"; **must** use distinct macro from absolute continuity |
| $f \sim g$ | ratio $\to 1$; requires $g \neq 0$ eventually |
| $f \asymp g$ | two-sided up to constants; constants declared |
| $f = O_\varepsilon(g)$ | explicit: constant depends on $\varepsilon$; this is the required form when a parameter is present |

**Rules:**
- $=$ in asymptotics is permitted (standard abuse) but must be registered once; $\in$ is preferred in DEP-0.
- Asymptotics may not be subtracted: $O(n) - O(n) = 0$ is Severity 0.
- Asymptotics inside exponents require explicit care: $n^{O(1)}$ must declare the polynomial degree bound.
- Asymptotic statements in a **theorem statement** must give the limit and uniformity in the statement, not the proof.
- $O(\cdot)$ in a claimed complexity must declare the computational model and the input measure (bits vs value).

## 12.4 Limit and supremum hygiene
- $\sup$/$\inf$ vs $\max$/$\min$: attainment must be proved before writing $\max$.
- $\limsup$/$\liminf$ must be used when the limit's existence is not established. Writing $\lim$ before proving existence is Severity 1.
- Extended-real arithmetic must be declared: $\infty - \infty$, $0 \cdot \infty$ conventions, and whether they can arise.
- Monotone limits must state the direction and the boundedness.
- $\lim$ over a net/filter must name the directed set.

---

# 13. Analysis policy

## 13.1 The interchange ledger
Every operation exchange requires an entry:
```yaml
- id: swap.007
  location: proof.lem.main:S12
  exchange: 'lim_{n} \int_X  ->  \int_X lim_{n}'
  theorem: thm.dominated_convergence
  hypotheses:
    measurability: {status: discharged, at: S4}
    ae_convergence: {status: discharged, at: S9}
    domination: {status: discharged, at: S11, witness: 'g = C h, h \in L^1 by H3'}
    sigma_finiteness: {status: not_required, reason: 'DCT does not require it'}
  null_set_uniformity: 'single null set, independent of n; see S9'
```
**Named-theorem precondition checklists (normative; every listed item must be discharged):**

| Theorem | Preconditions that must be discharged |
|---|---|
| Monotone convergence | nonnegative (or bounded below by an integrable function), measurable, pointwise monotone a.e., same measure space |
| Dominated convergence | measurable, a.e. convergence, single integrable dominating function valid for **all** $n$, domination a.e. with one null set |
| Fatou | nonnegative (or uniform integrable lower bound); inequality direction correct |
| Vitali convergence | convergence in measure + uniform integrability + tightness (on infinite measure spaces) |
| Fubini | product $\sigma$-finite, joint measurability w.r.t. the **product** $\sigma$-algebra, integrability of $|f|$ on the product |
| Tonelli | product $\sigma$-finite, joint measurability, nonnegativity |
| Differentiation under $\int$ | pointwise differentiability, local domination of the derivative, measurability, integrability at one point |
| Leibniz with variable limits | boundary terms, differentiability of limits, continuity of the integrand |
| Uniform limit theorem | uniform convergence, continuity of each term; on what domain (compact?) |
| Dini | monotone sequence, continuous limit, compact domain |
| Arzelà–Ascoli | pointwise boundedness + equicontinuity + compact domain (or suitable generalization); target complete |
| Banach–Alaoglu | dual of a normed space; weak-* topology; **AC/ultrafilter ledger entry** |
| Hahn–Banach (normed, general) | sublinear dominating functional; **DC/AC ledger entry** for the general case |
| Baire category | complete metric (or locally compact Hausdorff); countably many sets; closed/open as required |
| Riesz representation | locally compact Hausdorff, positive functional, Radon measure conventions declared |
| Radon–Nikodym | $\sigma$-finite (both measures, or the standard variant), absolute continuity, target measure $\sigma$-finite |
| Lebesgue decomposition | $\sigma$-finiteness |
| Egorov | finite measure, a.e. convergence, measurable functions |
| Lusin | Radon measure, measurable function, finite measure on the relevant set |
| Sobolev embedding | domain regularity (cone/Lipschitz/extension property), exponent relation, dimension, $p$ range including endpoints |
| Rellich–Kondrachov | bounded domain, boundary regularity, strict exponent inequality |
| Stone–Weierstrass | compact Hausdorff, subalgebra, separates points, contains constants (or the locally compact variant), real vs complex + self-adjointness |
| Implicit/inverse function | continuous differentiability (not mere differentiability), invertibility of derivative at the point, Banach completeness |
| Picard–Lindelöf | Lipschitz in the state variable uniformly in time, continuity in time, completeness; local vs global distinction |
| Gronwall | integrability of the coefficient, nonnegativity, absolute continuity of the comparison function |
| Taylor with remainder | differentiability class, remainder form (Lagrange/integral/Peano) and its exact hypotheses |
| Interchange of $\sum$ and $\int$ | Tonelli/DCT for series; absolute convergence if rearranging |
| Rearrangement of a series | absolute convergence, or unconditional convergence in the relevant topology; Riemann rearrangement warning |
| Analytic continuation | connectedness of the domain, identity theorem hypotheses (accumulation point in the domain) |
| Residue theorem | contour winding numbers, isolated singularities, no singularities on the contour, orientation, decay estimates for arcs |

## 13.2 Modes of convergence
Every convergence claim must name its mode. The document must contain a mode hierarchy table if more than two modes are used, and every implication between modes must be justified with the required extra hypotheses (e.g. a.e. + domination $\Rightarrow$ $L^1$; in measure $\Rightarrow$ a.e. along a subsequence; $L^p$ $\Rightarrow$ in measure; weak + norm convergence $\Rightarrow$ strong in uniformly convex spaces).

**Banned:** the unqualified word "converges" in DEP-0 when more than one mode is in play.

## 13.3 Null sets
- Every `a.e.` must name the measure.
- A countable union of null sets is null; an uncountable union is not. Any argument taking a union over an uncountable index set must be flagged and reworked (Fubini, continuity, separability, or a fixed dense countable set).
- Statements "for a.e. $x$, for all $y$" and "for all $y$, for a.e. $x$" are different; the order must be written explicitly and the null set's dependence declared.
- Modifying a function on a null set may destroy pointwise claims. Any such modification must be recorded, and any later pointwise claim about the modified function is Severity 0 unless re-justified.

## 13.4 Function spaces
- $L^p$ elements are equivalence classes. Pointwise evaluation of an $L^p$ element is banned without a chosen representative and a justification.
- The measure and the $\sigma$-algebra must be named for every space: $L^p(X, \Sigma, \mu)$.
- Endpoint cases $p = 1, \infty$, and $p < 1$ (quasi-normed, no triangle inequality) must be handled explicitly.
- Duality claims require the correct $p$ range and $\sigma$-finiteness where needed ($(L^\infty)^* \neq L^1$).
- Density claims must specify the topology of density.
- Inclusion claims must specify the measure's finiteness ($L^q \subseteq L^p$ for finite measure, $p \le q$).

## 13.5 Compactness
Every compactness argument must state the topology, the space, and the compactness source (Heine–Borel, Tychonoff + AC, Banach–Alaoglu + AC, Prokhorov + tightness + Polish, Arzelà–Ascoli, weak compactness + reflexivity + boundedness, Rellich). "By compactness" alone is Severity 1.

## 13.6 Differentiability
The derivative notion must be named: classical, one-sided, approximate, weak, distributional, Fréchet, Gâteaux, Hadamard, Clarke, viscosity. Implications between them require justification. Existence of all partials does not imply differentiability; any argument using this must be flagged Severity 0.

---

# 14. Algebra, category theory, and structure

## 14.1 Structure declarations
Every algebraic object must have its structure fully declared in the convention manifest or the statement:
- **Group:** finite/infinite, abelian, torsion, finitely generated, finitely presented, topological (and then continuity of operations).
- **Ring:** commutative?, unital?, $1 \neq 0$?, domain?, reduced?, Noetherian?, characteristic?, graded?, local?, complete?
- **Module:** left/right/bi, unital action?, finitely generated?, projective?, flat?, torsion-free?, over which ring?
- **Algebra:** associative?, unital?, over field or ring?, finite-dimensional?, separable?, central?
- **Field:** characteristic, perfect?, algebraically closed?, ordered?, complete?, valuation?
- **Vector space:** dimension (possibly infinite), over which field, topological?, basis existence (AC).
- **Lattice/order:** partial/total, complete?, distributive?, modular?, bounded?, well-founded?
- **Graph:** simple?, directed?, loops?, multi-edges?, finite?, connected?, weighted (and weight domain)?

## 14.2 Canonicity and choice
- The word **canonical** is restricted. It may be used only when a construction is given without arbitrary choices and is proved natural/invariant, or when it is a definitional/universal-property-derived map.
- The word **natural** requires a naturality square (or the full naturality transformation with components and the commutative square) in DEP-0.
- "Essentially unique" requires uniqueness up to a specified equivalence, and the equivalence must be specified (unique iso? unique iso compatible with data? contractible space of choices?).
- Any simultaneous choice over an infinite family requires a choice-ledger entry classifying the strength (AC, DC, CC, $AC_\omega(\mathbb{R})$, finite choice, or definable choice).
- "Fix a basis", "fix an algebraic closure", "fix a well-ordering", "fix a nonprincipal ultrafilter", "fix a Hamel basis", "fix a Vitali set" each generate an axiom-ledger entry with strength.

## 14.3 Size and universes
- Every category must declare: small, locally small, essentially small, large, and relative to which universe.
- Grothendieck universes / inaccessible cardinals must be in the axiom ledger.
- Functor categories, presheaf categories, and $\mathbf{Set}$ must have their size handled; "the category of all sets" requires a universe declaration.
- Yoneda requires local smallness. Adjoint functor theorems require completeness + solution-set / accessibility conditions; each must be discharged.
- (Co)limit existence must be established, not assumed; $\text{colim}$ over a large diagram may not exist.
- Universe polymorphism in formalizations must be declared and consistent; `Type u` vs `Prop` misuse is Severity 0 if it changes the meaning.

## 14.4 Diagrams
- Every diagram claimed commutative must either be (a) verified cell-by-cell with justifications, or (b) obtained by a named composition/pasting rule with the constituent cells identified.
- Diagram chases must be written as element chases with explicit elements and their images, or as a composition of named morphisms with equations. "Diagram chasing gives the result" is Severity 1.
- Non-commutative diagrams must be marked as such; a diagram with a $\neq$ cell must be explicit.
- Dashed arrows must have their existence-and-uniqueness justification attached.

## 14.5 Exactness and homological arguments
- Every sequence claimed exact must have exactness at each spot justified, or a reference to a named lemma providing it.
- Snake lemma / five lemma / nine lemma applications must verify the diagram hypotheses (rows exact, columns exact, which maps mono/epi).
- Derived functor arguments must specify the resolution class (projective/injective/flat), its existence, and independence of resolution.
- Spectral sequence arguments must state the convergence type (strong, weak, conditional), the quadrant, boundedness/filtration hypotheses, and the abutment. Conditional convergence must not be reported as strong.

---

# 15. Probability and stochastic processes

## 15.1 Mandatory ambient block
Every probabilistic section must open with:
```latex
\DepProbSpace{
  space = {(\Omega, \cF, \mathbb{P})},
  complete = {yes},
  filtration = {(\cF_t)_{t \ge 0}, right-continuous, complete},
  index_set = {[0,\infty)},
  state_space = {(E, \cE), Polish},
  rv_convention = {real-valued unless stated},
  ae_measure = {\mathbb{P}},
  cond_exp_version = {arbitrary fixed version; claims are version-independent (see S2)},
}
```

## 15.2 Independence
- "Independent" must specify: pairwise, mutual, or conditionally independent given a named $\sigma$-algebra.
- Independence of $\sigma$-algebras vs events vs random variables must be distinguished.
- Uncorrelated $\neq$ independent; any use of the implication requires joint Gaussianity or another stated justification.
- Independence must be preserved-check when passing to functions, limits, subsequences, or conditionings.

## 15.3 Conditioning
- Conditioning on a null event is banned unless a regular conditional probability is constructed and its existence hypotheses discharged (standard Borel / Polish target).
- Conditional expectation is defined only up to a.s. equality. Every claim must be either version-independent or a version must be fixed and declared.
- $\mathbb{E}[X \mid Y]$ vs $\mathbb{E}[X \mid \sigma(Y)]$ must be distinguished when the Doob–Dynkin representation is used; the representing function's measurability must be stated.
- Tower property requires nesting of $\sigma$-algebras; state the nesting.
- Conditional independence is not implied by unconditional independence, nor conversely.

## 15.4 Limit theorems
| Theorem | Preconditions to discharge |
|---|---|
| LLN (weak) | integrability, pairwise independence or variance/dependence control, identical distribution or Lindeberg-type condition |
| LLN (strong) | integrability ($\mathbb{E}|X| < \infty$), i.i.d. or specified dependence; the a.s. statement's null set |
| CLT (classical) | i.i.d., finite nonzero variance, correct centering/scaling; conclusion is convergence in distribution |
| CLT (Lindeberg/Lyapunov) | independence, triangular array, Lindeberg condition or Lyapunov moment condition, variance normalization |
| CLT (dependent) | mixing/martingale conditions explicitly verified |
| Berry–Esseen | third absolute moment, i.i.d., constant's dependence |
| Continuous mapping | continuity set of the limit has full measure |
| Slutsky | one sequence converges in distribution, the other in probability to a constant |
| Portmanteau | which equivalent form is used |
| Prokhorov | tightness, Polish space for the converse |
| Skorokhod representation | Polish target; the new space is not the original — claims must be transferred back carefully |
| Borel–Cantelli I | summability; no independence needed |
| Borel–Cantelli II | summability **and independence** (or a stated substitute) |
| Kolmogorov 0–1 | tail event of an independent sequence; identify the tail $\sigma$-algebra |
| Martingale convergence | submartingale + $\sup \mathbb{E}[X_n^+] < \infty$, or UI martingale for $L^1$ convergence |
| Optional stopping | bounded stopping time, or UI martingale, or integrable stopping time + bounded increments |
| Doob's inequalities | nonnegative submartingale / martingale, right-continuity, $p > 1$ for $L^p$ maximal inequality |
| Girsanov | Novikov/Kazamaki condition, equivalence of measures on the relevant $\sigma$-algebra, finite horizon |
| Itô formula | $C^{1,2}$ (or the stated weak version), semimartingale, integrability of the integrand |
| Kolmogorov extension | consistency, standard Borel/Polish state space |
| Ergodic theorem | measure-preserving transformation, integrability, ergodicity for the constant limit |

## 15.5 Concentration and tails
Every concentration inequality application must discharge: independence or martingale structure, boundedness or sub-Gaussian/sub-exponential parameters, variance proxy, and the exact form of the tail bound. Constants in exponents must be tracked; $\exp(-ct^2)$ with unnamed $c$ is banned in a claimed rate.

## 15.6 Distributional hygiene
- The distribution must be named with parameters and parameterization convention (e.g. Gamma shape/rate vs shape/scale; Normal mean/variance vs mean/precision).
- Moment generating functions may not exist; using them requires existence in a neighborhood of 0.
- Moment problems: a distribution is not determined by its moments in general; determinacy must be justified (Carleman, bounded support, etc.).
- Characteristic functions always exist; prefer them, and state the inversion theorem's hypotheses when inverting.
- Densities exist only under absolute continuity; writing $p_X(x)$ requires it.

---

# 16. Statistics and empirical inference

## 16.1 Model and estimand
Every statistical claim must declare:
- the sampling model and the population/target,
- the estimand (a functional of the distribution, written mathematically),
- the estimator (a measurable function of the data),
- the identification argument (why the estimand is identifiable from the observables),
- the assumptions required for identification vs for estimation vs for inference (these are three different lists and must be separated).

## 16.2 Assumption discharge
Every invoked theorem (consistency, asymptotic normality, efficiency, minimax rate, coverage) must have its regularity conditions discharged: identifiability, compactness or convexity of the parameter space, continuity/differentiability, dominance for uniform LLN, nonsingular information, interior point, moment conditions, rate conditions for nuisance estimation, Donsker/cross-fitting conditions where used.

## 16.3 Uncertainty reporting
- Every point estimate must have an uncertainty statement: standard error, confidence interval with method and nominal level, or posterior interval with prior.
- The interval's interpretation must be correct (frequentist coverage vs posterior probability). Misinterpretation is Severity 0.
- Bootstrap must declare: resampling scheme, number of replicates, seed, validity conditions, and whether it is percentile/BCa/basic/studentized.
- Asymptotic intervals must not be reported as exact.

## 16.4 Multiplicity and selection
- The number of hypotheses tested must be reported.
- The multiplicity correction must be named (Bonferroni, Holm, BH-FDR, permutation-based) with the family defined **before** analysis.
- Selective reporting, outcome switching, and post-hoc subgroup claims must be declared as exploratory.
- Any claim whose significance depends on an undisclosed search over specifications is Severity 0.

## 16.5 Pre-registration and confirmatory/exploratory separation
DEP-0 statistical claims must be either:
- **confirmatory**: pre-registered hypothesis, analysis plan, sample size / stopping rule, and primary outcome, with a timestamped artifact ID; deviations logged; or
- **exploratory**: explicitly labelled, with no confirmatory language, no $p$-value presented as confirmatory evidence, and effect sizes with intervals reported.

Mixing the two in one sentence is Severity 0.

## 16.6 Power, sample size, and stopping
- Sample size justification (a priori power analysis with assumed effect size, or a declared sequential design with alpha-spending) is mandatory for confirmatory claims.
- Optional stopping without correction is Severity 0.
- Post-hoc power computed from the observed effect is banned as evidence.

## 16.7 Data provenance and leakage
- Data source, version, license, collection protocol, and exclusion rules must be recorded.
- Train/validation/test separation must be described, with the exact split procedure and seed.
- Any preprocessing fitted on data must be fitted on training data only; leakage is Severity 0.
- Temporal, group, and subject leakage must be explicitly addressed.
- Duplicates across splits must be checked and the check reported.

---

# 17. Computability, complexity, and algorithms

## 17.1 Model declaration
Every computational claim must declare: model (TM, multi-tape TM, RAM, word-RAM with word size, circuit family, oracle machine, quantum circuit, BSS), input encoding, input size measure (bit length vs numeric value vs number of items), uniformity (logspace-uniform, P-uniform, non-uniform), and the resource measure (time, space, size, depth, queries, communication, rounds).

## 17.2 Reduction discipline
Every reduction must declare its type (many-one/Karp, Turing/Cook, truth-table, parsimonious, approximation-preserving, gap-preserving, randomized, subexponential, fine-grained), its cost, and the correctness proof in both directions where required.

- NP-hardness must specify: the source problem, the reduction, polynomial time in the **bit** encoding, and the correctness equivalence.
- Strong vs weak NP-hardness must be distinguished; pseudo-polynomial algorithms must not be called polynomial.
- Approximation hardness must state the gap, the completeness/soundness parameters, and the assumption (P$\neq$NP, UGC, ETH, SETH).
- Fine-grained reductions must track the exact parameter blowup.

## 17.3 Randomized classes
`BPP`, `RP`, `coRP`, `ZPP` definitions must fix the error constants and state amplification (with the independence and repetition cost). One-sided vs two-sided error must not be conflated. "With high probability" must be quantified ($1 - n^{-c}$ for which $c$, for all $c$, or a fixed $c$).

## 17.4 Algorithm correctness
Every algorithm must have:
- pseudocode with typed inputs and outputs,
- preconditions and postconditions,
- a termination proof with a variant measure,
- a correctness proof with a loop invariant per loop (initialization, maintenance, termination),
- a complexity analysis with the model declared,
- worst-case vs average-case vs amortized clearly separated,
- the input distribution declared for average-case claims,
- numerical stability discussion if floating-point.

## 17.5 Constructivity and effectivity
- "Computable" must specify total vs partial, and the model.
- "Decidable" vs "semi-decidable" vs "co-semi-decidable" must not be conflated.
- "Effective" bounds must be extractable; a bound proved by contradiction with no modulus must be marked ineffective.
- Non-constructive existence may not be used inside a claimed algorithm.

---

# 18. Numerical and experimental mathematics

## 18.1 Arithmetic classification
Every numerical claim must be classified:

| Class | Meaning | Admissible as proof? |
|---|---|---|
| `exact` | integer/rational/algebraic exact arithmetic | Yes |
| `certified` | interval arithmetic / ball arithmetic with rigorous enclosures, or a checkable certificate | Yes, with certificate |
| `verified-symbolic` | CAS result with an independently checkable certificate (e.g. a factorization, a Gröbner basis with cofactors) | Yes, with certificate verification |
| `floating` | IEEE-754 arithmetic without enclosure | **No** |
| `heuristic-numeric` | numerical evidence, no enclosure | **No**; status `empirical` |

Reporting a `floating` result as a proof is Severity 0.

## 18.2 Required numerical manifest
```yaml
- id: num.eigenvalue_bound
  claim: 'lambda_min(A) > 0.0173'
  class: certified
  method: 'Arb ball arithmetic, 256-bit'
  library: arb-2.23.0
  certificate: dep/artifacts/num_eig_001.cert
  verifier: tools/verify_eig.py
  verifier_hash: sha256:...
  rounding: 'round-to-nearest, IEEE-754 binary64 for the outer loop; ball enclosure for the bound'
  conditioning: 'kappa(A) <= 3.2e4, certified'
  failure_policy: 'verifier exits nonzero if enclosure does not exclude 0'
  seed: n/a
  hardware: 'x86-64, no fast-math'
  compiler_flags: '-O2 -ffp-contract=off'
```

## 18.3 Floating-point policy
- `-ffast-math`, `-funsafe-math-optimizations`, and any flag permitting reassociation are banned for any computation whose result is load-bearing, unless the claim is `empirical` and the flag is recorded.
- FMA contraction must be declared (`-ffp-contract=off` or `on`), because it changes results.
- Reduction order must be fixed and recorded for reproducibility (parallel reductions are non-associative).
- BLAS/LAPACK backend, version, and thread count must be pinned.
- NaN/Inf/denormal behavior must be declared.
- Cancellation, conditioning, and backward/forward error must be discussed for any claim of numerical accuracy.

## 18.4 CAS trust boundary
A CAS is not a proof oracle. Every CAS-derived load-bearing result must have either:
1. an independently verifiable certificate checked by a small, audited verifier, or
2. a formal proof in a proof assistant, or
3. a re-derivation by a second, independent system with matching results **and** a declared status of `verified-numeric` rather than `proved`.

"It follows from Mathematica" is Severity 0.

## 18.5 Search and enumeration
- Exhaustive searches must declare the search space, the pruning rules, and a proof that pruning preserves completeness.
- Sampled searches must declare the sampling distribution, the seed, and the fact that the result is not exhaustive.
- "We searched up to $10^9$ and found no counterexample" is `empirical`, never `proved`.

---

# 19. Formal verification policy

## 19.1 Admitted-proof ban
In any artifact backing a `machine-checked` claim, the following tokens are banned outright:

| System | Banned tokens |
|---|---|
| Lean 4 | `sorry`, `admit`, `native_decide` (unless waived with TCB entry), `axiom` (unless ledgered), `unsafe` (unless isolated + audited), `implemented_by` on load-bearing definitions, `partial` on functions claimed total |
| Coq/Rocq | `Admitted`, `admit`, `Abort` (in a claimed-complete file), `Axiom`, `Parameter`, `Hypothesis` at top level (unless ledgered), `Unset Guard Checking`, `Unset Positivity Checking` |
| Isabelle | `sorry`, `oops`, `axiomatization` (unless ledgered), `ML` blocks that install axioms, `nitpick`/`quickcheck` reported as proof |
| HOL4/HOL Light | `prove(..., cheat)`, `new_axiom` (unless ledgered), `mk_thm` |
| SMT | infinite timeout, `unknown` treated as `unsat`, `(set-option :produce-proofs false)` when a proof is claimed |

A single occurrence downgrades the claim from `machine-checked` to `sketched` and triggers Severity 0 if the document claims `machine-checked`.

## 19.2 Axiom ledger extraction
CI must run and archive:
- Lean: `#print axioms Theorem.Name` for every cited theorem.
- Coq: `Print Assumptions Theorem_Name.`
- Isabelle: `thm` + unused/axiom audit via `Nitpick`-free theory dependency report.

The extracted set must equal the declared ledger. Expected standard axioms (`propext`, `Classical.choice`, `Quot.sound`, `funext`, `propext`, `JMeq_eq`, `proof_irrelevance`) must be enumerated explicitly — not omitted because they are "standard".

## 19.3 Trusted computing base (TCB)
The TCB must be enumerated: kernel version, elaborator, any `native_decide` compiler trust, any external solver whose `unsat` is trusted, any proof-producing tool, any `sorry`-free but axiom-bearing library. Each entry needs a justification and an owner.

## 19.4 Universe, `Prop`, and totality hygiene
- `Prop` vs `Type` must be intentional; a theorem stated in `Prop` about a `Type`-level construction must not silently change computational content.
- Universe levels must be explicit where they matter; `Type*` elaboration results must be recorded for load-bearing definitions.
- `partial`/`unsafe` definitions must not appear in theorem statements claimed to be about total functions.
- Classical tactics (`by_contra`, `classical`) generate LEM ledger entries in constructive developments.

## 19.5 Statement-fidelity audit
**This is the most important rule in this chapter.** A machine-checked theorem is worthless if its statement does not mean what the prose says.

Every `machine-checked` claim must ship a **fidelity mapping**: a two-column table mapping each component of the prose statement to the formal term, reviewed and signed.

```yaml
- prose: 'for every nonempty finite graph G'
  formal: '(G : SimpleGraph V) [Fintype V] [Nonempty V]'
  audit: 'matches; note SimpleGraph excludes loops and multi-edges — see conv.graph.simple'
- prose: 'there is a proper 3-coloring'
  formal: '∃ c : V → Fin 3, G.ProperColoring c'
  audit: 'ProperColoring requires adjacent vertices differ; matches'
- prose: 'the bound is uniform in G'
  formal: 'the ∃C precedes ∀G in the formal statement'
  audit: 'verified: quantifier order A E confirmed'
```

Mandatory audit checks:
- Quantifier order matches.
- Hypotheses match exactly (no extra formal hypothesis, no missing one).
- Definitions unfold to the intended mathematical objects (no `Nat` subtraction truncation standing in for integer subtraction; no `Int` standing in for $\mathbb{R}$; no `Fin n` overflow standing in for $\mathbb{Z}$).
- Degenerate cases have the same meaning in both ($0$, empty, $n=0$).
- The formal statement is not trivially true (e.g. hypothesis `False`, or an empty type).
- Non-vacuity is witnessed formally too.

A mismatch is Severity 0. "The Lean theorem is basically the same" is Severity 0.

## 19.6 Refinement to implementations
If a paper claims an *implementation* is verified:
- Either the implementation is extracted by a trusted/proven extraction mechanism (recorded), or
- a refinement proof links the implementation's semantics (including machine integers, memory, concurrency) to the model, or
- the claim must be downgraded to "the algorithm is verified; the implementation is not".

Modeling `uint32` as $\mathbb{Z}$, or memory as a mathematical map without aliasing, and claiming the C++ code verified, is Severity 0.

## 19.7 Tactic brittleness and budgets
- `simp` without an explicit lemma list is restricted in DEP-0 formalizations (library updates change its behavior); `simp only [...]` is required for load-bearing proofs.
- Automation-heavy tactics (`aesop`, `omega`, `polyrith`, `nlinarith`, `decide`) must have a declared time budget and a recorded elaboration time.
- `decide` on large goals must have its kernel reduction cost budgeted and recorded.
- Proof term size and elaboration time regressions beyond a declared threshold fail CI.
- Library upgrades require re-running the fidelity audit for every cited theorem whose statement or definitional unfolding changed.

## 19.8 SMT policy
- Every solver invocation must have a finite, declared timeout.
- `unknown` and timeout are **not** `unsat`. Treating them as success is Severity 0.
- Quantifier instantiation patterns must be declared when quantifiers are present; incompleteness must be acknowledged.
- Solver version pinned; proof logs archived; if the solver's `unsat` is trusted, it is a TCB entry.
- Finite-domain "verification" must state the bound and must not be described as unbounded.

---

# 20. Foundations and the axiom ledger

## 20.1 Required declaration
Every document must declare its foundational setting in the manifest:
```yaml
foundation:
  base_theory: ZFC
  logic: classical-first-order
  universes: none
  choice: full-AC
  constructivity: classical
  extra_axioms: []
  formalization_foundation: null   # or 'Lean-Quot-sound + propext + Classical.choice'
```

## 20.2 Choice-strength classification
Every use of choice must be classified into one of: `finite-choice`, $AC_\omega$, $AC_\omega(\mathbb{R})$, DC, CC, BPI/ultrafilter, `full-AC`, `global-choice`, `none`.

The following must be flagged automatically by the linter's phrase list and manually confirmed:

| Phrase | Typical strength |
|---|---|
| "choose a basis" (arbitrary vector space) | full AC |
| "well-order the set" | full AC |
| "take a maximal ideal" (arbitrary ring) | full AC (Krull) |
| "extend this functional" (Hahn–Banach, general) | BPI / DC depending on form |
| "take a convergent subnet / cluster point" (Banach–Alaoglu) | BPI |
| "Tychonoff for compact Hausdorff" | BPI |
| "Tychonoff general" | full AC |
| "there exists a nonprincipal ultrafilter" | BPI |
| "there exists a nonmeasurable set" | some choice (not ZF-provable) |
| "every infinite set has a countably infinite subset" | $AC_\omega$-ish (Dedekind-infinite) |
| "countable union of countable sets is countable" | $AC_\omega$ |
| "sequentially continuous $\Rightarrow$ continuous" | $AC_\omega(\mathbb{R})$ in general |
| "recursive construction of length $\omega$" | DC (or $AC_\omega$) unless the choice is definable |
| "pick $x_n$ for each $n$" | $AC_\omega$ unless a definable selection exists |

**Mitigation requirement:** if a result claims to be choice-free but uses one of these phrases, the author must either give a definable selection or downgrade the claim. This is Severity 1, escalating to Severity 0 for papers whose contribution is about choice strength or constructivity.

## 20.3 Constructive status
If the document claims constructive validity:
- LEM, LPO, LLPO, Markov's principle, and $\neg\neg$-elimination must each be ledgered at each use.
- Proof by contradiction establishing a positive statement is banned.
- "Either $x = 0$ or $x \neq 0$" for reals requires LPO; must be flagged.
- Suprema of arbitrary bounded sets require care; locatedness must be addressed.
- The Brouwer–Heyting–Kolmogorov interpretation must be respected for $\exists$ (a witness is required).

## 20.4 Reverse-math and strength annotations (recommended)
For results in logic or foundations, DEP-0 results **should** annotate the weakest known subsystem ($\text{RCA}_0$, $\text{WKL}_0$, $\text{ACA}_0$, $\text{ATR}_0$, $\Pi^1_1\text{-CA}_0$) in which the proof goes through, and whether the reversal is proved.

## 20.5 Large cardinal and consistency assumptions
Any large cardinal, determinacy, forcing axiom, or consistency assumption must be:
- stated as a hypothesis in the theorem statement,
- ledgered,
- reflected in the abstract and contribution list (Law 12),
- accompanied by its known consistency strength relative to standard assumptions.

---

# Part II — Communication engineering

---

# 21. Readability: measured, not felt

Readability is a set of computed metrics with hard thresholds. All metrics are computed per region and emitted to `readability.json`. Thresholds are defaults; a project may tighten them, never loosen them without a waiver.

## 21.1 Metric table

| ID | Metric | Definition | DEP-0 | DEP-1 | DEP-2 |
|---|---|---|---|---|---|
| R01 | Sentence length, max | words per sentence, math counted as 1 token per symbol group | 40 | 50 | 60 |
| R02 | Sentence length, mean | rolling mean per paragraph | 22 | 26 | 30 |
| R03 | Paragraph length | lines of typeset output | 8 | 12 | 14 |
| R04 | Symbols per display | distinct symbol tokens in one equation | 9 | 12 | 16 |
| R05 | Display width | fraction of `\linewidth` | 1.0 | 1.0 | 1.0 |
| R06 | Quantifier alternations | per display | 3 | 4 | — |
| R07 | Nesting depth (delimiters) | max bracket/paren nesting in a display | 4 | 5 | 6 |
| R08 | Cognitive stack depth | simultaneously open cases + inductions + contradictions + subsequence extractions | 3 | 4 | — |
| R09 | Notation distance | pages to declaration (or notation-table + preamble re-declaration) | 2 | 4 | — |
| R10 | Forward reference distance | any reference to a not-yet-stated result | 0 (banned except roadmap) | $\le 1$ section | — |
| R11 | Proof length before decomposition | pages / steps | 3 / 40 | 6 / 80 | — |
| R12 | Step fan-in | premises cited per step | 5 | 7 | — |
| R13 | Chain length | relations in one inequality/equality chain | 5 | 7 | — |
| R14 | Lemma fan-out | results depending on one lemma before it must be split | 12 | 20 | — |
| R15 | Definition–use gap | pages between a definition and its first use | 5 | 10 | — |
| R16 | Uninterrupted formal text | consecutive displays with no prose | 3 | 5 | — |
| R17 | Prose-free proof fraction | fraction of proof steps with no prose connective | $\le 0.5$ | $\le 0.7$ | — |
| R18 | Acronym load | undefined-at-first-use acronyms | 0 | 0 | 0 |
| R19 | Section preamble presence | every section $\ge 1$ page has a preamble stating goal + notation + roadmap | required | required | recommended |
| R20 | Signpost density | per proof $\ge 1$ page, explicit structural markers ("Step 1 of 3: ...") | $\ge 1$ per page | $\ge 1$ per 2 pages | — |
| R21 | Hedging density | hedges per 100 words in DEP-0 | $\le 1$ | $\le 2$ | — |
| R22 | Banned-phrase count | Appendix A occurrences | 0 | 0 | $\le 2$ |
| R23 | Cold-read score | Chapter 21.4 checklist, fraction passed | 1.0 | $\ge 0.9$ | — |
| R24 | Dependency depth | longest chain from axioms/known results to a main theorem | reported; > 25 requires a dependency figure | | |

## 21.2 Cognitive stack accounting (R08)
The stack is incremented by: opening a case, opening an induction, opening a contradiction, opening a subsequence extraction, opening a "suffices to show" reduction, opening a nested claim. It is decremented by the matching close. Every open must have an explicit close marker (`\DepCloseCase`, `\DepEndInduction`, `\DepEndReduction`).

**Suffices-to-show reductions** (`\DepSuffices`) must state the reduction proof: why the new goal implies the old. A "suffices" without the implication proof is Severity 0 — this is one of the most common silent gaps in mathematics.

## 21.3 The one-idea rule
- One idea per sentence.
- One step per numbered proof line.
- One purpose per paragraph, stated in its first sentence.
- One main claim per theorem environment (conjunctions of $\ge 3$ independent conclusions must be split or clearly numbered as parts with separate proofs).

## 21.4 Cold-read protocol (R23)
A designated reader in the field but not the subfield must, using only the document, complete the following for each DEP-0 theorem, without asking the author:
1. State the ambient structures.
2. List every hypothesis with its identifier.
3. State the conclusion as a formula.
4. Give the quantifier prefix.
5. Name the claim status and completeness status.
6. Give one instance satisfying the hypotheses.
7. Give one instance failing at least one hypothesis.
8. Identify which prior results the proof uses.
9. Identify the proof's top-level structure (induction / contradiction / construction / cases).
10. Identify where each hypothesis is used.

Score = fraction completed correctly. DEP-0 requires 10/10. A failure indicates a document defect, not a reader defect.

## 21.5 Structural signposting requirements
Every DEP-0 proof longer than one page must begin with a **proof roadmap** in DEP-2-marked prose, listing the steps and their purposes, and must reference the roadmap at each transition. The roadmap is not load-bearing (Chapter 5.3 containment applies).

Every section $\ge 1$ page must have a preamble: purpose, notation introduced, results contained, dependencies on other sections.

---

# 22. Prose style

## 22.1 Banned and restricted phrases
Appendix A is the full normative table. Core bans in DEP-0/DEP-1:

**Justification-masking (banned):** clearly, obviously, trivially, evidently, it is easy to see, one sees immediately, a routine computation, a standard argument, by standard techniques, it can be shown, it is well known that (without citation), after some algebra, straightforward, elementary manipulation, the reader may verify, left to the reader, exercise for the reader, without difficulty, plainly.

**Scope-masking (banned):** in general (unqualified), under mild assumptions, under suitable conditions, for appropriate choices, with the obvious modifications, mutatis mutandis (without specifying the mutations), by symmetry (without invariance proof), similarly (without step reference), analogously (same), the other cases are similar (same).

**Canonicity-masking (restricted, requires ledger):** canonical, natural, essentially unique, unique up to isomorphism (without saying which), the obvious map, the induced map (without construction).

**Novelty/marketing (banned in DEP-0/DEP-1; restricted in DEP-2):** novel, new (as a quality claim), powerful, elegant, beautiful, deep (as praise), surprising, remarkable, striking, state-of-the-art, superior, significantly (non-statistically), dramatically, vastly, optimal (without an optimality claim record), first (without a priority record).

**Hedging (restricted, density-limited):** somewhat, rather, quite, arguably, seemingly, appears to, seems to, tends to, may potentially, could possibly.

## 22.2 Voice, tense, person
- First person plural ("we") for authorial choices and constructions. Not for the reader's actions ("we see that" is permitted only for genuinely immediate observations, $\le 1$ IGU).
- Present tense for mathematics ("Theorem 3.1 gives"), past for historical acts ("Fermat proved").
- Passive voice permitted for object-focus, banned to hide agency in methodological choices ("the outliers were removed" must name who and by what rule).
- Imperative permitted only in explicitly labelled instructions to the reader for a mechanical operation ("expand the square").

## 22.3 Terminology lock
- One term per concept, one concept per term, document-wide.
- All technical terms must be defined before use or cited to a pinpoint external definition.
- Acronyms expanded at first use in the body (abstract counts separately) and listed in a glossary.
- No synonym rotation for elegance. Elegance is not a defense.

## 22.4 Sentence-level rules
- No sentence begins with a mathematical symbol.
- No two mathematical symbols are adjacent without an intervening word or a relation.
- Displays are parts of sentences and carry punctuation.
- No display is a complete sentence on its own without a lead-in.
- Every display is referenced at least once, or it is decorative and must be inlined or deleted (Law 13).
- Numbered displays must be referenced; unreferenced numbered displays are Severity 3, escalating if load-bearing (then it is a missing reference, Severity 2).

## 22.5 Claims about difficulty and importance
Statements about a result's difficulty, importance, or novelty are DEP-2 only, and require either a citation or an explicit argument. "This is the first result of its kind" requires a priority record: a literature search with date, databases, queries, and inclusion criteria, archived.

---

# 23. Document architecture

## 23.1 Atomic file topology
One logical unit per file. Required layout:
```text
paper/
├── main.tex
├── dep/
│   ├── manifest.yaml
│   ├── conventions.yaml
│   ├── symbols.yaml
│   ├── axioms.yaml
│   ├── constants.yaml
│   ├── interchanges.yaml
│   ├── gaps.yaml
│   ├── claims.yaml
│   ├── waivers/
│   ├── artifacts/
│   └── out/                      # generated, never hand-edited
├── front/
│   ├── abstract.tex
│   ├── notation_table.tex
│   └── results_table.tex
├── sections/
│   ├── intro.tex
│   ├── prelims.tex
│   └── ...
├── definitions/
│   ├── def_uniform_integrability.tex
│   └── def_tightness.tex
├── statements/
│   ├── thm_main.tex
│   ├── lem_compactness.tex
│   └── cor_rate.tex
├── proofs/
│   ├── proof_thm_main.tex
│   ├── proof_lem_compactness.tex
│   └── proof_cor_rate.tex
├── examples/
│   ├── ex_witness_main.tex
│   └── cex_dropping_H3.tex
├── formal/
│   ├── lean/
│   └── fidelity/
├── experiments/
│   ├── code/
│   ├── data/
│   ├── env/
│   └── results/
├── quarantine/
└── tools/
    └── dep_lint/
```
**Rules:**
- **One statement per file. One proof per file.** Statement and proof are separate files; the statement file must compile without the proof (with the proof obligation registered).
- No file named `misc`, `utils`, `helpers`, `notes`, `extra`, `old`, `new`, `final`, `final2`, `junk`.
- Line limits: statement file $\le 120$ lines; proof file $\le 400$ lines (DEP-0) / 800 (DEP-1); section prose file $\le 600$ lines. Exceeding requires decomposition into lemmas, not a waiver, unless the content is a single irreducible computation (then declare and provide a CAS certificate).
- Generated content lives only in `dep/out/` and `experiments/results/`, is never hand-edited, and has a golden test.
- Quarantined material is excluded from the build and carries a manifest with reason, owner, ticket, deadline, disposition.

## 23.2 Statement/proof separation contract
The statement file must be readable and checkable in isolation. It declares: hypotheses, conclusion, statuses, dependencies of the *statement* (definitions used), and the pointer to its proof. The proof file declares its dependencies (lemmas used) and discharges the obligations.

This makes it mechanically possible to verify Law 1 (no hypotheses in the proof only) and to compute the statement-level dependency graph independently of proofs.

## 23.3 The results table
`front/results_table.tex` is generated and mandatory. Columns:

| ID | Type | Statement (one line) | Claim status | Complete? | Depends on | Axioms | Sharpness | Witness | Proof |
|---|---|---|---|---|---|---|---|---|---|

A reader must be able to see the entire logical inventory of the paper on two pages.

## 23.4 The notation table
Generated from `symbols.yaml`. Columns: glyph, sort, meaning, scope, declaration site, page. Grouped by scope. Must be complete for DEP-0 symbols.

## 23.5 The hypothesis ledger
Generated. For every hypothesis of every DEP-0 result: ID, text, discharge sites, and whether it is necessary (sharpness status). Unused hypotheses must be either removed or explicitly marked:
```latex
\DepUnusedHyp{H4}{Retained for comparability with \cite{...}; not needed for the proof. See \DepRef{rem.H4_unnecessary}.}
```
An unused, unmarked hypothesis is Severity 2 (it misleads about the result's strength).

## 23.6 The gap register
```yaml
- id: gap.tightness_step
  node: lem.tightness
  missing: 'Construction of a compact set K with P(X_n \notin K) < eps uniformly in n; the current argument only gives it for each fixed n.'
  quantifier_error: '∀n∃K asserted where ∃K∀n needed'
  blast_radius: [lem.tightness, thm.main, cor.rate, abstract.claim2]
  owner: a.author
  ticket: DEP-114
  opened: 2026-09-02
  expires: 2026-12-01
  status: open
  downgrades: {lem.tightness: sketched, thm.main: proved-modulo, cor.rate: proved-modulo}
```
Expired gaps trigger automatic retraction of dependent claims from the `complete` category and a build failure.

## 23.7 Abstract and introduction contract
**Abstract rules (DEP-0 for claim status, DEP-2 for prose style):**
- Every claim in the abstract maps to a result ID in `claims.yaml`.
- The claim's status and hypotheses must be reflected. A `conditional` result must carry its condition in the abstract. A `proved-modulo` result must say so.
- No claim of optimality without an optimality record (Chapter 29).
- No quantitative claim without the corresponding artifact.
- Length $\le 250$ words unless the venue requires otherwise; the limit is a readability constraint, not a licence to drop hypotheses. Use "under [named hypotheses]" if space is tight.

**Introduction rules:**
- Must contain a **contribution list**, each item mapping to result IDs with statuses.
- Must contain a **limitations paragraph** referencing Chapter 30.4.
- Must contain a **proof-technique overview** marked DEP-2.
- Must not contain any load-bearing inference.
- Related work must be pinpointed and fair; mischaracterizing prior work to inflate novelty is Severity 0.

## 23.8 Dependency figure
If dependency depth (R24) exceeds 25, or the number of DEP-0 nodes exceeds 30, a generated dependency figure is mandatory, with main results highlighted and no cycles.

---

# 24. LaTeX and typography policy

## 24.1 Required packages and engine
- Engine: pinned (LuaLaTeX recommended for Unicode and font control).
- `amsmath`, `amsthm`, `mathtools`, `amssymb` (glyphs only via `dep` wrappers), `microtype`, `hyperref` (last), `cleveref` (after `hyperref`), `booktabs`, `siunitx`, `dep` (the project standard package).
- `tikz-cd` or `tikz` for diagrams; `pgfplots` for plots, generated from data.
- Banned: packages that redefine core math semantics silently, packages that alter numbering non-deterministically, `subeqn` hacks, `\usepackage{times}`-style unpinned font swaps.

## 24.2 Banned commands
| Command | Reason | Replacement |
|---|---|---|
| `\def` | unscoped, no arity checking | `\newcommand` |
| `$$...$$` | TeX primitive spacing bugs | `\[...\]` or `equation` |
| `\eqnarray` | broken spacing | `align` |
| `\over`, `\atop`, `\choose` | ambiguous precedence | `\frac`, `\binom` |
| `\left...\right` across line breaks | fails | `\bigl...\bigr` etc. with manual sizing |
| `\nonumber` on a load-bearing equation | breaks referencing | number it |
| Manual theorem numbers | drift | environments + labels |
| `\hspace{-...}` to fix content | hides overflow | rewrite the display |
| `\text{italic-variable}` | wrong semantics | `\mathit` or a declared macro |
| `\mathrm{d}x` typed manually | inconsistent | `\dd x` |
| `\mbox` for math | breaks math spacing | `\text` in the right place, or restructure |
| `\footnote` containing load-bearing hypotheses | Law 1 | move to the statement |
| `\includegraphics` of a raster plot of data | non-reproducible | generated vector plot from data |
| `\today` unpinned | non-determinism | pinned date macro |
| `\label` without a prefix scheme | collisions | Chapter 24.4 |

## 24.3 Display math rules
- Every display is punctuated as part of its sentence.
- Alignment: relation symbols aligned in multi-line displays; the relation goes at the start of the continuation line.
- No display exceeds the text width (R05).
- Delimiter sizing is manual and consistent (`\bigl`, `\Bigl`, ...); automatic `\left\right` permitted only for single-line displays with height $\le 2$ levels.
- Sub-display spacing must not be manually adjusted to fit content.
- Every `align` row is one IGU in DEP-0 (Chapter 11.2), with its justification in a right-hand `\text{[...]}` column or an accompanying prose line.

## 24.4 Label and reference scheme
Mandatory prefixes:
```text
def:<name>      thm:<name>      lem:<name>      prop:<name>
cor:<name>      claim:<name>    conj:<name>     rem:<name>
ex:<name>       cex:<name>      conv:<name>
eq:<name>       fig:<name>      tab:<name>      alg:<name>
sec:<name>      app:<name>
proof:<node>:S<k>               hyp:<node>:H<k>
swap:<n>        gap:<name>      const:<name>    sym:<name>
```
Rules:
- Labels are semantic and stable; renaming a label is a breaking change requiring a deprecation alias.
- `\cref`/`\Cref` only; bare `\ref` for results is banned (it loses the type).
- `\eqref` for equations.
- Every external citation is pinpointed: `\cite[Thm.~4.12, p.~87, v3]{Author2020}`. Bare `\cite{Author2020}` for a specific theorem is Severity 1.
- Cross-file references resolved through the generated index; no hardcoded numbers anywhere.

## 24.5 Theorem environment styling
- Statement text in italic, headings in bold small caps, hypothesis labels upright.
- Proof environment with an explicit end marker; nested proofs use a distinct marker.
- DEP-2 environments (`depintuition`, `depremark`) visually distinct (e.g. shaded or smaller font) and mechanically tagged.
- Status badges printed in the margin for every DEP-0 node: `[proved · complete]`, `[conditional · gap-declared]`. A reader must never have to hunt for the status.

## 24.6 Unicode and encoding
- UTF-8 source. Unicode math in source is banned in favor of macros (except in comments), because it defeats linting.
- Consistent glyph choices: `\emptyset` vs `\varnothing` fixed in the manifest; `\epsilon` vs `\varepsilon` fixed; `\phi` vs `\varphi` fixed; `\le` vs `\leq` fixed by macro.

---

# 25. Figures, tables, and diagrams

## 25.1 General rules
- Every figure and table is referenced in the text and its purpose stated.
- Captions must be self-contained: a reader looking only at the figure must understand what is shown, what the axes are, what the error bars mean, and what the takeaway is.
- Vector formats for generated graphics (PDF/SVG). Raster only for photographs, at $\ge 300$ dpi, with the source archived.
- Colorblind-safe palettes; no information encoded by color alone (use markers/line styles too).
- Fonts in figures must match the body font family and be $\ge$ the caption size at final scale.

## 25.2 Data plots
Mandatory declarations: axis quantities and units, scale (linear/log, base), error bar semantics (SD, SEM, 95% CI, IQR — say which), $n$ per group, the estimator plotted, the number of seeds/replicates, and the artifact ID of the generating script + data hash.

Banned: truncated axes without an explicit break marker and a declaration; dual axes without justification; smoothed curves without stating the smoother and bandwidth; connecting discrete points to imply continuity without justification; 3-D effects on 2-D data; pie charts for comparison of magnitudes.

## 25.3 Commutative diagrams
- Normative content, not decoration: subject to Chapter 14.4.
- Every arrow labelled with its morphism.
- Every cell that is claimed commutative has a justification reference (in the caption or an adjacent proof).
- Dashed/$\exists!$ arrows annotated with their universal property.
- Diagram source in `tikz-cd` in the repository; no images of diagrams.

## 25.4 Tables of results
- Numeric entries must state precision and rounding rule.
- Bold "best" entries must declare the comparison criterion and whether differences are statistically meaningful.
- Every table generated from a data artifact with a hash; hand-typed numbers are banned.
- Units and uncertainty in the header, not repeated per cell.

---

# 26. Citations, attribution, and priority

## 26.1 Pinning
Every bibliography entry must include: authors, title, venue, year, **version identifier** (arXiv `vN`, DOI, journal volume/pages), and a stable locator. For arXiv preprints, the version used must be pinned and the date recorded.

## 26.2 Pinpoint requirement
Citing a specific result requires: result number in that version, page or section, and the statement's hypotheses checked against the use site. The hypothesis discharge is recorded in the hypothesis ledger with `source: external`.

## 26.3 Prohibited citation practices
- "See, e.g., [1–7]" as justification for a specific step.
- Citing a survey or textbook for a result whose hypotheses the author has not checked.
- Citing a paper that itself cites the result, without following the chain.
- Citing a retracted paper without noting the retraction and checking the used result.
- Citing a conditional result as unconditional.
- Citing an unpublished manuscript as `proved` without an available manuscript artifact.
- "Personal communication" as the sole support for a DEP-0 step (permitted only as attribution, never as justification).
- Citation padding: references not used and not surveyed.

## 26.4 Retraction and version drift check
CI must check every citation against a retraction database and against the pinned version's existence, at a recorded timestamp. A citation to a superseded version is permitted only if the specific cited result is unchanged, which must be verified and recorded.

## 26.5 Attribution of lemmas
Every lemma that is not original must be attributed with a pinpoint citation, even if the proof is rewritten. "For completeness we include the proof" does not transfer attribution. Presenting a known lemma as new is Severity 0.

## 26.6 Formalized-library attribution
Citing Mathlib/Archive of Formal Proofs/etc. requires the commit hash, the declaration name, and the axiom footprint.

---

# Part III — Research-paper obligations

---

# 27. The contribution ledger

## 27.1 Claim–evidence mapping
`dep/claims.yaml` maps **every** claim in the title, abstract, introduction, contribution list, section summaries, and conclusion to result IDs.

```yaml
- id: claim.abstract.2
  text: 'We prove a sharp O(n log n) upper bound for X under H1-H3.'
  location: abstract:l4
  maps_to: [thm.main_upper]
  status_inherited: proved
  hypothesis_reflection: 'H1-H3 named in abstract'
  optimality_record: opt.main
  audit:
    sharpness: 'matching lower bound thm.main_lower'
    model: 'word-RAM, w = Theta(log n)'
    uniformity: 'worst-case'
  verdict: pass
```

## 27.2 Inflation checks (mechanical)
The linter compares the claim text's asserted strength to the mapped result's recorded strength on these axes:
- quantifier order,
- hypothesis set (no dropped hypotheses),
- claim status (no `sketched` $\rightarrow$ "we prove"),
- constants/uniformity (no asymptotic $\rightarrow$ exact),
- model (no word-RAM $\rightarrow$ "linear time" without qualification),
- optimality (no upper bound $\rightarrow$ "optimal"),
- generality (no special case $\rightarrow$ "in general"),
- conditionality (no `conditional` $\rightarrow$ unconditional),
- scope (no finite-domain verification $\rightarrow$ "for all $n$").

Any inflation is Severity 0.

## 27.3 Title rules
The title may not assert a result the paper does not prove at the stated status. Titles containing "Optimal", "Sharp", "Tight", "First", "Complete characterization", "Solving", "Settling" require the corresponding record. Titles are DEP-0 for claim status.

---

# 28. Empirical and experimental sections

## 28.1 Required structure
Every empirical section must contain, in order:
1. **Question and estimand.** What is being measured, formally.
2. **Design.** Confirmatory vs exploratory; pre-registration ID or explicit exploratory declaration.
3. **Data.** Provenance, version, license, size, collection, exclusions, splits, leakage checks.
4. **Methods.** Algorithms with versions and hyperparameters; the full search budget.
5. **Baselines.** Justified, tuned with an equal budget, cited with versions.
6. **Metrics.** Definitions, units, direction of improvement, and why they measure the estimand.
7. **Uncertainty.** Intervals, method, seeds, replicate counts.
8. **Multiplicity.** Family, correction, and the pre-specified primary outcome.
9. **Ablations.** Which component contributes what.
10. **Threats to validity.** Confounds, selection effects, distribution shift, implementation artifacts.
11. **Negative results.** What did not work; what failed to replicate.
12. **Reproducibility.** Artifact ID, environment, commands, expected outputs and tolerances.

## 28.2 Fair-comparison rules
- Equal hyperparameter search budget for baselines, or an explicit declaration of the asymmetry and its direction.
- Equal compute budget or an explicit declaration.
- No test-set tuning. Any test-set evaluation must be single-shot per declared hypothesis, or corrected.
- Reported results must be over multiple seeds with the count declared; single-seed results are `empirical` with a mandatory variance caveat.
- Cherry-picked qualitative examples must be labelled as selected, with the selection rule.

## 28.3 Statistical reporting minimum
For every comparison: effect size with units, interval estimate with method and level, sample size, test statistic and exact $p$ if a test is used, the test's assumptions checked, and the multiplicity correction. "Significantly better" without these is Severity 0.

## 28.4 Reproducibility artifacts
```yaml
artifact:
  id: art.exp_003
  code_commit: 4f2a91c
  container: dep/artifacts/exp003.sif
  container_hash: sha256:...
  environment_lock: experiments/env/lock.txt
  seeds: [1,2,3,4,5,6,7,8,9,10]
  hardware: 'A100-80GB x1, CUDA 12.4, driver 550.54'
  determinism: 'torch.use_deterministic_algorithms(True); NCCL_ALGO=Tree; NCCL_PROTO=Simple'
  runtime: '14h22m'
  expected_outputs: experiments/results/exp003_golden.json
  tolerance: 'relative 1e-6 for scalars; bitwise for integer counters'
  license: MIT
  data_doi: 10.xxxx/xxxxx
```
Non-reproducible experiments must be labelled `empirical · unreproducible` in the results table, and may not support a DEP-0 claim.

---

# 29. Optimality, sharpness, and tightness claims

## 29.1 Optimality classes
| Class | Meaning | Required evidence |
|---|---|---|
| `OPT-0: best-known` | No better result known under the same model and assumptions | Literature record with search date/queries; explicit "to our knowledge" |
| `OPT-1: matched-bound` | Upper bound matches a proved lower bound in the same model | Both results, with matching constants/parameters and identical model |
| `OPT-2: provably optimal` | A lower bound proof shows no better is possible in a precisely specified class/model | The lower bound theorem, the model, the class of algorithms, and the quantifiers |

## 29.2 Rules
- "Optimal" without a class is banned.
- Optimality is **model-relative and class-relative**. Every claim must state: the model, the resource, the class of algorithms/objects quantified over, and the parameter regime.
- An upper bound alone never justifies "optimal", "tight", or "sharp". Severity 0.
- Matching up to constants is `OPT-1 up to constants` and must say so; matching in exponent only is `OPT-1 in exponent` and must say so.
- Lower bounds must state whether they are unconditional, conditional, information-theoretic, in a restricted model (comparison-based, algebraic, streaming, communication), or against a specific algorithm class.
- "Sharp" for an inequality requires an equality case (or an asymptotically achieving family) exhibited.
- Every hypothesis of a sharp result must have a sharpness status: `sharp (counterexample cex.X)`, `not sharp (gap known)`, `unknown (ticket)`.

## 29.3 Optimality record
```latex
\DepOptimal{
  class = {OPT-2},
  model = {comparison-based, worst-case, deterministic},
  resource = {comparisons},
  quantified_over = {all deterministic comparison algorithms},
  upper = {thm.upper},
  lower = {thm.lower},
  match = {exact, including constant},
  regime = {n \ge 2},
  evidence = {both proofs complete; degeneracy battery passed},
}
```

---

# 30. Counterexamples, sharpness, limitations, and the Degeneracy Crucible

## 30.1 Hypothesis-necessity obligation
For each DEP-0 theorem with $k$ hypotheses, the author must produce, for each hypothesis $H_i$, one of:
- a **counterexample** showing the conclusion fails when $H_i$ is dropped (all other hypotheses retained), or
- a **proof that $H_i$ is redundant**, or
- a declaration `sharpness unknown` with an owner and ticket.

A theorem with zero counterexamples and zero declarations is Severity 1. A theorem whose abstract claims sharpness with zero counterexamples is Severity 0.

## 30.2 Counterexample verification
A counterexample must be verified clause by clause: each retained hypothesis is checked to hold, the dropped hypothesis is checked to fail, and the conclusion is checked to fail. "Consider a non-measurable set" without exhibiting the failure is a sketch, not a counterexample.

## 30.3 The Degeneracy Crucible
Every DEP-0 theorem must be attacked with a fixed battery of degenerate instantiations, before submission. The battery is domain-adapted from this master list; inapplicable probes must be marked `n/a` with a reason.

**Master degeneracy battery (minimum applicable probes must be executed and recorded):**
*Cardinality/size:* empty set; singleton; two elements; $n = 0$; $n = 1$; countably infinite; uncountable; proper class.
*Algebra:* zero ring; trivial group; characteristic 2; characteristic $p$; non-commutative; zero divisors; nilpotents; non-reduced; torsion; non-finitely-generated; empty product; identity element; idempotents.
*Order/analysis:* $\sup$ not attained; $\inf = -\infty$; empty supremum; boundary point; equality case in every inequality; non-strict inequality where strict is claimed; discontinuity at one point; measure-zero exceptional set; dense null set; nowhere-differentiable function; unbounded variation; oscillation without limit; conditionally convergent series.
*Measure/probability:* zero measure; infinite measure; non-$\sigma$-finite; non-complete; point mass; degenerate random variable; deterministic process; perfectly dependent variables; uncorrelated but dependent; heavy tails (no variance); no mean; conditioning on a null event; non-measurable set; non-tight family; non-UI family; stopping time infinite with positive probability.
*Topology/geometry:* non-Hausdorff; non-compact; non-separable; non-metrizable; disconnected; empty space; boundary; non-orientable; non-simply-connected; incomplete metric; non-locally-compact; infinite-dimensional.
*Category/logic:* empty category; empty type; initial/terminal object; non-locally-small; large diagram; empty diagram; inconsistent theory; empty model; non-standard model; intuitionistic countermodel; `Prop` vs `Type` mismatch.
*Computation:* zero-length input; empty string; maximum integer; overflow; adversarial tie-breaking; all-equal keys; sorted/reverse-sorted input; duplicate elements; disconnected graph; self-loop; multigraph; zero weights; negative weights; zero-capacity edge.
*Statistics:* $n = 1$; perfect separation; collinearity; zero variance; ties; all-missing group; single cluster; distribution shift; label leakage; duplicated rows.

**Quota:** at least $4k + 8$ applicable probes per DEP-0 theorem with $k$ hypotheses, or all applicable probes if fewer exist. Each probe records: instantiation, hypotheses satisfied (yes/no), conclusion holds (yes/no), verdict (`passes`, `counterexample found`, `n/a + reason`).

## 30.4 Gap regression rule
When a gap or counterexample invalidates a claim, the fix must be accompanied by a **regression battery** of at least $4k + 8$ probes targeting the *class* of the defect, not just the specific instance. The class must be named (e.g. "quantifier-order errors in tightness arguments", "null-set dependence on a parameter").

Additionally, the same class must be swept across the entire document: every other node using the same pattern must be re-audited, and the sweep recorded. Fixing one instance and closing the ticket is Severity 1.

## 30.5 Limitations section (mandatory)
Every paper must have a limitations section stating:
- which hypotheses are believed to be artifacts of the proof rather than the phenomenon,
- which regimes are not covered,
- which claims are conditional and on what,
- which results are ineffective and why,
- which experiments did not replicate,
- what the strongest known counterexample to a generalization is,
- what would break if a foundational assumption were dropped.

A limitations section saying "none known" without a recorded search is Severity 1.

---

# 31. Reproducibility and artifact qualification

## 31.1 Artifact classes
| Class | Meaning |
|---|---|
| `A0` | No artifact required (pure deduction, no computation) |
| `A1` | Artifact provided, runs, produces the claimed tables/figures within tolerance |
| `A2` | `A1` + independently reproduced by a reviewer on a clean machine |
| `A3` | `A2` + formal proofs kernel-checked on a clean machine with matching axiom ledger |

DEP-0 claims of type `verified-numeric`, `machine-checked`, or `empirical` require at least `A1`, and `machine-checked` requires `A3` for the `machine-checked` badge.

## 31.2 Clean-machine requirement
An artifact that requires the author's machine, an undocumented environment variable, a network service, an unpinned dependency, or a manual step not in the manifest, is not an artifact. It is a story.

## 31.3 Data and code availability statements
Must be specific: repository DOI, commit, license, and access conditions. "Available on request" is banned for DEP-0 empirical claims. "Code will be released" is banned; release before submission or downgrade the claim.

---

# Part IV — Annotation, enforcement, and extermination

---

# 32. The annotation standard

## 32.1 Zero-cost requirement
Annotations are metadata. They must not alter the mathematical content. They are rendered as margin badges and/or a machine-readable sidecar; the generated sidecar is subject to all rules of this standard.

## 32.2 Required fields (every DEP-0 and DEP-1 node)
```latex
\DepBlock{
  ID          = thm.main_upper,
  FILE        = statements/thm_main.tex,
  CLASS       = DEP-0,
  WHAT        = {Worst-case comparison upper bound for sorted-set intersection.},
  WHY         = {Improves the exponent over [Prior2019, Thm 3.1] from 2 to 1+o(1) in the sparse regime.},
  STATUS      = proved,          % claim status, Chapter 5.4
  COMPLETE    = complete,        % completeness status, Chapter 5.5
  AMBIENT     = {conv.model.wordRAM, conv.graph.simple},
  HYP         = {H1, H2, H3},
  QUANTIFIERS = {A A E A},        % with domains in the statement
  CONCLUSION  = {eq.main_bound},
  DEPENDS     = {lem.sparse_partition, lem.potential, thm.prior_lower},
  AXIOMS      = {none beyond ZFC},
  CONSTANTS   = {const.C_part, const.c_pot},
  INTERCHANGE = {swap.007, swap.011},
  UNIFORMITY  = {uniform in the input family; constants depend on (d,p)},
  EFFECTIVE   = {yes; modulus computable in poly time},
  WITNESS     = {ex.witness_main},
  SHARPNESS   = {H1: sharp (cex.drop_H1); H2: sharp (cex.drop_H2); H3: unknown (DEP-201)},
  DEGENERACY  = {dep/out/degeneracy/thm_main_upper.json, 20/20 applicable probes passed},
  FIDELITY    = {formal/fidelity/thm_main_upper.yaml},  % if machine-checked
  EVIDENCE    = {proofs/proof_thm_main.tex; formal/lean/MainUpper.lean@4f2a91c},
  GAP         = {none},
  OWNER       = {a.author},
  REVIEW      = {2026-10-28, b.referee, cold-read 10/10},
}
```

## 32.3 Field semantics
| Field | Rule |
|---|---|
| `WHAT` | One sentence, no repetition of the name, no marketing. Must name the mathematical object and the property. |
| `WHY` | Must state the purpose and, when a choice was made, the rejected alternative. "It is interesting" is banned. |
| `STATUS` | Exactly one value from Chapter 5.4. |
| `COMPLETE` | Exactly one value from Chapter 5.5. |
| `HYP` | Must match the `\DepHyp` declarations in the statement exactly. Mismatch is Severity 0. |
| `QUANTIFIERS` | The prefix string; must match the statement and the proof's final step. |
| `DEPENDS` | Must match the extracted proof DAG. Undeclared dependencies are Severity 0. |
| `AXIOMS` | Must match the axiom ledger; machine-extracted where available. |
| `WITNESS` | Required for DEP-0 (Law 14). `none` requires a ticket. |
| `SHARPNESS` | One entry per hypothesis. |
| `DEGENERACY` | Artifact reference; quota per Chapter 30.3. |
| `GAP` | Gap IDs or `none`. Non-`none` forces `COMPLETE ≠ complete`. |
| `EVIDENCE` | Proof location; for `machine-checked`, the pinned artifact. |
| `REVIEW` | Date, reviewer, cold-read score. Absent for `complete` is Severity 1. |

## 32.4 Optional fields
`SERVES` (for lemmas), `GENERALIZES`, `NOT_GENERALIZING` (with counterexample), `SUPERSEDES`, `SUPERSEDED_BY`, `PORTABILITY` (foundations sensitivity), `SECURITY` (for cryptographic claims), `TICKET`, `WAIVER`, `PRIORITY` (for novelty claims), `ARTIFACT`, `PREREG`.

## 32.5 Cryptographic extension
For security proofs, additionally required:
```latex
\DepSecurity{
  MODEL       = {IND-CCA2, random oracle model},
  ADVERSARY   = {PPT, adaptive, q_H hash queries, q_D decapsulation queries},
  ASSUMPTION  = {MLWE_{n,q,chi}},
  REDUCTION   = {tight; loss factor 1, or loss q_H},
  TIGHTNESS   = {concrete bound: Adv <= 2 Adv_MLWE + q_H/2^k},
  IDEALIZATION= {ROM; QROM not claimed},
  SIDE_CHANNEL= {not constant-time; not claimed},
  SCOPE       = {classical adversaries only; post-quantum not claimed},
}
```
Claiming a security property without the model, the adversary class, the assumption, and the concrete loss is Severity 0. A ROM proof described as standard-model is Severity 0. A loose reduction described as tight is Severity 0.

---

# 33. Mechanical enforcement: dep_lint

`tools/dep_lint` is a DEP-2 tool subject to this standard. It is data-driven: every pattern, threshold, and severity lives in `.dep/dep_lint.json`. It exits nonzero on any Severity 0 or 1 finding, or on document/configuration drift.

## 33.1 Invocation and exit codes
```text
dep_lint [options] <paths>
  -c, --config <path>     default .dep/dep_lint.json
  -t, --self-test
  -v, --version
```
| Code | Meaning |
|---|---|
| 0 | No failing findings |
| 1 | Findings at a severity in `fail_on` (default 0,1), or failed self-test |
| 2 | Bootstrap failure (`DEP-LINT-BOOT-<n>`) |
| 3 | Usage error |

Deterministic: sorted traversal, sorted output by (file, line, rule, message), no locale/time/environment dependence.

## 33.2 Rule catalog
Each rule below must exist in the configuration and have a heading here; `DEP-LINT-DOC-SYNC` enforces the correspondence.

### Rule DEP-LINT-BLOCK
**Severity 1. Chapters 32.2, 5.** Every statement and proof environment must be preceded by a `\DepBlock` containing all required fields. Parameters: `required_fields`, `allowed_statuses`, `allowed_completeness`.

### Rule DEP-LINT-STATUS-VALUE
**Severity 1. Chapter 5.4/5.5.** `STATUS` and `COMPLETE` values must be in the closed vocabularies.

### Rule DEP-LINT-STATUS-CONTAMINATION
**Severity 0. Chapter 5.5.** A node with `COMPLETE=complete` must not depend on a node with any other completeness status, nor on `conditional`/`sketched`/`conjectural`/`empirical` claim statuses (except `machine-checked`/`proved`/`verified-numeric` where the latter is used only for finite-domain subclaims).

### Rule DEP-LINT-DAG-CYCLE
**Severity 0. Chapter 11.1.** The extracted dependency graph must be acyclic, including definition dependencies.

### Rule DEP-LINT-HYP-DECLARED
**Severity 0. Law 1, Chapter 9.2.** Every `\DepUse{Hk}` must resolve to a `\DepHyp{Hk}` in the same statement. Free-floating hypotheses are rejected.

### Rule DEP-LINT-HYP-DISCHARGED
**Severity 1. Law 1, Chapter 23.5.** Every declared hypothesis must be used in the proof or explicitly marked `\DepUnusedHyp` with a reason.

### Rule DEP-LINT-SYMBOL-REGISTERED
**Severity 1. Law 3, Chapter 7.1.** Every semantic macro used must have a registry entry with sort and scope, and a declaration site at or before first use.

### Rule DEP-LINT-SYMBOL-SHADOW
**Severity 0. Chapter 7.1, 10.1.** A symbol must not be re-bound while free in a live enclosing obligation.

### Rule DEP-LINT-OVERLOAD
**Severity 1. Chapter 7.2.** Glyphs on the banned/restricted overload list must use the disambiguating macro or have an overload-ledger entry with a mechanical rule.

### Rule DEP-LINT-CONVENTION
**Severity 1. Chapter 7, Appendix B.** Every convention-manifest key referenced by an `AMBIENT` field must exist and have a fixed value; every ambiguous term on the convention list appearing in DEP-0 must resolve to a manifest entry.

### Rule DEP-LINT-BANNED-PHRASE
**Severity 1 (DEP-0/1), 3 (DEP-2). Chapter 22.1, Appendix A.** Occurrences of the banned-phrase table outside a sanctioned form. Parameters: `pattern`, `icase`, `exempt_environments`, `max_per_100_words_dep2`.

### Rule DEP-LINT-JUSTIFICATION
**Severity 1. Chapter 11.3.** Every `\DepStep` must have a `by` value from the permitted set; banned justification words are rejected.

### Rule DEP-LINT-IGU
**Severity 1 (DEP-0), 2 (DEP-1). Chapter 11.2.** A step citing more than one theorem, or more than the permitted IGU count, is rejected. Parameters: `max_igu_dep0=1`, `max_igu_dep1=3`, `max_fanin_dep0=5`.

### Rule DEP-LINT-SWAP-LEDGER
**Severity 0. Law 5, Chapter 13.1.** Detected interchange patterns (`lim` adjacent to $\int$/$\sum$/$\partial$/$\mathbb{E}$, nested $\int$, $\sup$/$\inf$ swap) must have a ledger entry with a named theorem and all preconditions marked discharged.

### Rule DEP-LINT-CONSTANT
**Severity 1. Law 6, Chapter 12.1.** Every constant symbol must be in the ledger with a dependency signature; disposable-constant conventions must be declared and scoped to one proof; constants in statements must be named.

### Rule DEP-LINT-EPSILON-ORDER
**Severity 1. Chapter 12.2.** An $\varepsilon$-argument ($\ge 2$ of $\varepsilon,\delta,\eta,N,M$ bound in one proof) must contain a `\DepParamOrder` block.

### Rule DEP-LINT-WLOG
**Severity 0. Chapter 11.5.** Every WLOG token must be a `\DepWlog` with `reduction` and `invariance` fields resolving to proof steps.

### Rule DEP-LINT-INDUCTION
**Severity 0. Chapter 11.4.** Every induction must be a `\DepInduction` with measure, well-foundedness reference, base cases, and a `generalized` list; every parameter appearing in a recursive invocation must be in `generalized` or proved fixed.

### Rule DEP-LINT-SUFFICES
**Severity 0. Chapter 21.2.** Every "suffices to show"/"it suffices" must be a `\DepSuffices` with a reduction proof reference.

### Rule DEP-LINT-CASES
**Severity 1. Chapter 11.6.** Case analyses must have an exhaustiveness step and matching close markers; open stack depth must not exceed R08.

### Rule DEP-LINT-CHAIN-LABEL
**Severity 1. Chapter 11.7.** Every relation in a `depcchain` must carry a justification column entry; chains exceeding R13 are rejected.

### Rule DEP-LINT-IFF
**Severity 0. Chapter 11.8.** An `iff` goal must have both directions or an equivalence chain with per-link equivalence justification.

### Rule DEP-LINT-VACUITY
**Severity 1. Law 14, Chapter 30.** Every DEP-0 theorem must have a `WITNESS` or a ticketed `unknown` declaration.

### Rule DEP-LINT-SHARPNESS
**Severity 1 (2 if abstract claims sharpness $\rightarrow$ 0). Chapter 30.1.** Every hypothesis must have a sharpness status.

### Rule DEP-LINT-DEGENERACY
**Severity 1. Chapter 30.3.** The degeneracy artifact must exist, meet the quota, and mark every inapplicable probe with a reason.

### Rule DEP-LINT-AXIOM-DRIFT
**Severity 0. Law 4, Chapter 19.2.** Declared axiom ledger must equal the machine-extracted set for every `machine-checked` node.

### Rule DEP-LINT-ADMITTED
**Severity 0. Chapter 19.1.** Banned proof-skip tokens in any artifact backing a `machine-checked` claim.

### Rule DEP-LINT-FIDELITY
**Severity 0. Chapter 19.5.** Every `machine-checked` node must have a fidelity mapping covering every hypothesis, the quantifier prefix, and the conclusion, with a signed review.

### Rule DEP-LINT-CHOICE-PHRASE
**Severity 1. Chapter 20.2.** Choice-suggesting phrases must have a choice-ledger entry with a strength classification.

### Rule DEP-LINT-MODE-UNQUALIFIED
**Severity 1. Chapters 13.2, 15.** "converges", "continuous", "a.e.", "independent", "integrable" without their required qualifiers in a scope where more than one meaning is registered.

### Rule DEP-LINT-CLAIM-INFLATION
**Severity 0. Law 12, Chapter 27.2.** Every claim in title/abstract/intro/contribution/conclusion must map to result IDs and pass the strength comparison on all axes.

### Rule DEP-LINT-CITE-PINPOINT
**Severity 1. Chapter 26.2.** Citations used as step justifications must have a locator and a pinned version.

### Rule DEP-LINT-CITE-RETRACTION
**Severity 1. Chapter 26.4.** Retraction/version check must be present and within the configured freshness window.

### Rule DEP-LINT-READABILITY
**Severity 2 (first), 1 (repeat). Chapter 21.1.** All R01–R24 metrics against thresholds. Parameters: the metric table.

### Rule DEP-LINT-NOTATION-DISTANCE
**Severity 2/1. Chapter 7.3.** R09 enforcement using the typeset page map.

### Rule DEP-LINT-FORWARD-REF
**Severity 1. Chapter 21.1 R10.** Forward references in DEP-0 outside a declared roadmap.

### Rule DEP-LINT-DEP2-CONTAINMENT
**Severity 0. Chapter 5.3.** No DEP-0 node may depend on a DEP-2 region.

### Rule DEP-LINT-ATOMIC-FILE
**Severity 1. Chapter 23.1.** One statement/proof per file; line limits; banned file names.

### Rule DEP-LINT-LATEX-BANNED
**Severity 2 (some 1). Chapter 24.2.** Banned commands and environments.

### Rule DEP-LINT-LABEL-SCHEME
**Severity 2. Chapter 24.4.** Label prefixes and `\cref` usage.

### Rule DEP-LINT-FIGURE-PROVENANCE
**Severity 1. Chapter 25.** Every figure/table must have a generating artifact and hash; error-bar semantics and $n$ declared for data plots.

### Rule DEP-LINT-EMPIRICAL-MINIMUM
**Severity 0 for missing uncertainty/multiplicity on a DEP-0 claim; 1 otherwise. Chapters 16, 28.** Required empirical fields present; confirmatory/exploratory declared; leakage check recorded.

### Rule DEP-LINT-NUMERIC-CLASS
**Severity 0. Chapter 18.1.** A `floating` or `heuristic-numeric` result may not back a `proved` claim.

### Rule DEP-LINT-GAP-EXPIRY
**Severity 1. Chapter 23.6.** Expired gaps fail the build and force status downgrade of the blast radius.

### Rule DEP-LINT-WAIVER-EXPIRY
**Severity 1. Chapter 34.6.** Expired waivers fail the build.

### Rule DEP-LINT-ORPHAN
**Severity 2. Law 13.** Unreferenced results, unused definitions, unreferenced numbered displays.

### Rule DEP-LINT-DOC-SYNC
**Severity 1. Law 10, Chapter 33.** Every configured rule has a heading here; every documented rule exists in configuration; headings unique; document `Version:` equals `standard.version`.

## 33.3 Bootstrap error codes
| Code | Meaning |
|---|---|
| 1 | I/O failure reading configuration, manifest, ledger, or document |
| 2 | Parse failure (JSON/YAML/TeX) with file, line, column |
| 3 | Include cycle or excessive depth |
| 4 | Missing required key |
| 5 | Wrong type |
| 6 | Unknown check primitive |
| 7 | Severity out of range 0–3 |
| 8 | Invalid regular expression |

## 33.4 Known limits (review remains mandatory for these)
The linter is lexical and structural. It does **not** decide mathematical truth. The following require human review, the Degeneracy Crucible, formalization, or CI artifacts:
- correctness of a cited theorem's application beyond hypothesis-name matching,
- semantic correctness of an algebraic step not covered by a decision procedure,
- whether a "canonical" map is truly canonical,
- whether a counterexample truly satisfies the retained hypotheses,
- whether a fidelity mapping is honest (it can be checked for coverage, not for truth),
- whether the prose `WHAT` matches the mathematics,
- novelty and priority,
- statistical design validity beyond field presence,
- whether an `n/a` degeneracy probe is genuinely inapplicable.

Claiming "lint passes, therefore the paper is correct" is Severity 0.

## 33.5 Self-verification gate
A change to the tool, configuration, or this chapter is compliant only if: the tool builds warning-clean; it lints its own sources to zero Severity 0/1; `--self-test` passes every scenario with exact expected counts; `DEP-LINT-DOC-SYNC` passes. Adding a rule requires updating configuration and this chapter in the same change.

---

# 34. Violation handling and extermination

## 34.1 Prime rule
> Non-compliant mathematics is not merged, not submitted, and not cited as established.
> If detected before submission, it is blocked.
> If detected after submission, it is corrected, downgraded, or retracted.
> **We exterminate the error, not the author.**

## 34.2 Severity classes
### Severity 0 — Exterminate immediately
- Any invalid inference in a load-bearing result.
- Quantifier-order error between statement, proof, and abstract.
- Undischarged interchange.
- Hidden hypothesis in a load-bearing result.
- Circular dependency.
- `sorry`/`Admitted` in a `machine-checked` claim.
- Axiom-ledger drift.
- Statement-fidelity mismatch.
- Claim inflation (abstract/title stronger than results).
- `floating` result presented as proof.
- Optimality claim without a lower bound.
- Security claim without model/adversary/assumption/loss.
- Test-set leakage; undisclosed optional stopping; undisclosed multiplicity.
- Misattributed lemma presented as new.
- WLOG without invariance; "suffices" without reduction.
- Induction loading error.
- DEP-2 region load-bearing.
- Status contamination.

**Response:** block; if merged/published, correct or retract immediately; compute blast radius; downgrade all dependents; add regression battery (Chapter 30.4); add lint rule if possible; write an extermination report; notify citing sections and, if published, the venue.

### Severity 1 — Exterminate unless emergency waiver
Missing annotation block; missing hypothesis discharge; missing witness; missing sharpness status; missing degeneracy artifact; unregistered symbol; unnamed constant; unlabelled chain; non-pinpoint citation; expired gap; expired waiver; missing cold-read review; atomic-file violation; missing empirical field on a non-DEP-0 claim.

**Response:** block; repair or downgrade; waiver only if written, owned, reviewed, and expiring.

### Severity 2 — Reject and request repair
Readability threshold violations (first occurrence); orphan results; unused hypotheses unmarked; label-scheme violations; banned LaTeX commands; missing non-example; vague `WHY`; overlong files.

### Severity 3 — Warn and educate
Typographic nits; punctuation of displays; minor prose; formatting inconsistencies not affecting meaning.

## 34.3 Extermination pipeline
1. **Structure** — files, headers, annotation blocks, statuses.
2. **Registry** — symbols, conventions, constants, axioms.
3. **Logic** — hypothesis discharge, DAG, IGU, WLOG, induction, suffices, cases, chains.
4. **Ledgers** — interchanges, gaps, choice, sharpness, degeneracy.
5. **Formal** — kernel check, admitted-token scan, axiom extraction, fidelity coverage.
6. **Numeric** — artifact reproduction, arithmetic class, certificates.
7. **Empirical** — design fields, multiplicity, leakage, intervals, seeds.
8. **Claims** — inflation check across all informal layers.
9. **Readability** — R01–R24, cold-read score.
10. **Citations** — pinning, locators, retraction freshness.
11. **Verdict** — `PASS`, `WARN`, `FAIL`, `EXTERMINATE`.

## 34.4 Actions
- **Reject** (unmerged): close with rule, evidence, and CI run ID.
- **Downgrade**: change claim/completeness status, propagate to the blast radius, regenerate the results table and abstract mapping.
- **Quarantine**: move to `quarantine/`, exclude from build, add manifest with reason, owner, ticket, deadline, disposition (`repair` or `delete`).
- **Retract**: for published material; publish a correction/erratum with the exact statement affected, the counterexample or gap, and the corrected statement if known.
- **Delete**: dead definitions, unused lemmas, expired quarantine, unsupported conjectures presented as results.

## 34.5 Blast-radius propagation
Invalidating node $N$ requires computing the transitive closure of dependents $D(N)$ and, for each node in $D(N)$, either re-proving it without $N$ or downgrading its status. The abstract and contribution list must be re-audited. This is mechanical and mandatory. Silently leaving dependents at `complete` is Severity 0.

## 34.6 Waivers
Stored in `.dep/waivers/`, YAML, with: `id`, `rule`, `node`, `violation`, `reason`, `owner`, `logic_review`, `stats_review` (if applicable), `created`, `expires`, `status`. Maximum lifetime 90 days. Waivers may never cover: invalid inference, admitted proofs, claim inflation, axiom drift, fidelity mismatch, or leakage. Expired waivers auto-fail the build.

## 34.7 Extermination report
`.dep/exterminations/<date>-<ticket>.md` containing: node, violation, rule, severity, detection method, counterexample or gap, blast radius, action taken, regression battery ID, follow-up ticket, and the class-level sweep results.

Reports are institutional memory. They are not optional.

## 34.8 Human handling
Attack the defect, not the person.

Good: "This violates Law 5: the interchange at S12 has no domination hypothesis. The step must be justified or the claim downgraded."

Bad: "You are careless."

Repeated violations trigger pairing, additional review, and mandatory checklist sign-off — not blame. The object of extermination is the error.

## 34.9 Extermination examples
**Example 1 — Interchange without domination.**
```latex
S12: \lim_n \int f_n = \int \lim_n f_n     [by convergence of f_n]
```
Verdict: `EXTERMINATE`. Rule: Law 5 / 13.1. Pointwise convergence alone does not suffice; $f_n = n\cdot\mathbf{1}_{(0,1/n)}$ is a counterexample to the step. Action: produce a dominating function or use Vitali with UI; otherwise downgrade.

**Example 2 — Quantifier swap in a tightness argument.**
Statement claims $\exists K \forall n$, proof establishes $\forall n \exists K$.
Verdict: `EXTERMINATE`. Rule: 9.3 / 27.2. Action: register gap, downgrade `thm.main` to `proved-modulo`, fix abstract.

**Example 3 — Hidden $\sigma$-finiteness.**
Radon–Nikodym applied to a non-$\sigma$-finite measure.
Verdict: `EXTERMINATE`. Rule: Law 1 / 13.1. Action: add $\sigma$-finiteness as `H4`, re-run degeneracy battery with a non-$\sigma$-finite probe.

**Example 4 — WLOG by scaling that drops $x = 0$.**
Verdict: `EXTERMINATE`. Rule: 11.5. Action: split the $x = 0$ case.

**Example 5 — Induction loading.**
Induction on $n$ with $m$ fixed, but the recursive call uses $m+1$.
Verdict: `EXTERMINATE`. Rule: 11.4. Action: generalize $m$ in the IH and re-prove.

**Example 6 — `sorry` in a claimed-verified paper.**
Verdict: `EXTERMINATE`. Rule: 19.1. Action: downgrade to `sketched`, remove "verified" from title/abstract, notify co-authors, open ticket.

**Example 7 — Unbounded integers modeling `uint32`.**
Verdict: `EXTERMINATE`. Rule: 19.5/19.6. Action: remodel with `UInt32` and wrapping semantics, or drop the implementation claim.

**Example 8 — "Optimal" with only an upper bound.**
Verdict: `EXTERMINATE`. Rule: 29.2. Action: prove a lower bound or replace with `OPT-0 best-known` plus a literature record.

**Example 9 — Abstract drops the condition.**
Theorem is `conditional on RH`; abstract says "We prove...".
Verdict: `EXTERMINATE`. Rule: Law 12. Action: rewrite abstract; re-audit all claims.

**Example 10 — $p < 0.05$ after 40 unreported comparisons.**
Verdict: `EXTERMINATE`. Rule: 16.4. Action: report the family, apply correction, relabel as exploratory.

**Example 11 — Single null set per $n$, union over $n$ uncountable.**
Verdict: `EXTERMINATE`. Rule: 13.3. Action: fix a countable dense set or use a continuity argument.

**Example 12 — Non-vacuous theorem with unsatisfiable hypotheses.**
`H1` requires a compact infinite-dimensional normed space.
Verdict: `EXTERMINATE`. Rule: Law 14. Action: the theorem is vacuous; delete or repair the hypotheses.

---

# 35. Review checklists

## 35.1 Statement checklist
- [ ] All hypotheses in the statement, with IDs.
- [ ] Quantifier prefix recorded and correct.
- [ ] Ambient structures and conventions fixed.
- [ ] Conclusion syntactically identifiable.
- [ ] Uniformity and effectivity declared.
- [ ] Non-vacuity witness exists.
- [ ] Claim status and completeness status correct.
- [ ] Sharpness status per hypothesis.

## 35.2 Proof checklist
- [ ] DAG acyclic; declared dependencies match.
- [ ] $\le 1$ IGU per step (DEP-0).
- [ ] Every step justified by a permitted token.
- [ ] Every hypothesis discharged or marked unused.
- [ ] Every interchange ledgered with preconditions.
- [ ] Every WLOG has invariance + reduction.
- [ ] Every induction has measure, well-foundedness, base cases, generalization.
- [ ] Every "suffices" has a reduction proof.
- [ ] Cases exhaustive, closed, stack $\le 3$.
- [ ] Chains labelled, $\le 5$ relations.
- [ ] `iff` both directions.
- [ ] Constructions verified clause by clause.
- [ ] Subsequences tracked; diagonal countable.
- [ ] Final step matches the goal.

## 35.3 Notation checklist
- [ ] Every symbol registered with sort and scope.
- [ ] No shadowing of live symbols.
- [ ] No unregistered overloading or abuse.
- [ ] Notation distance $\le 2$ pages or table + preamble.
- [ ] Convention manifest complete.

## 35.4 Foundations checklist
- [ ] Axiom ledger complete and machine-matched.
- [ ] Choice-strength classified at each use.
- [ ] Constructive status consistent with claims.
- [ ] Zero admitted tokens.
- [ ] TCB enumerated.
- [ ] Fidelity mapping complete and signed.

## 35.5 Analysis/probability checklist
- [ ] Modes of convergence named.
- [ ] Null sets named, counted, and uniform where needed.
- [ ] $L^p$ elements not evaluated pointwise without representatives.
- [ ] Independence type declared.
- [ ] Conditioning avoids null events or constructs RCP.
- [ ] UI/optional stopping/concentration preconditions discharged.

## 35.6 Empirical checklist
- [ ] Confirmatory/exploratory declared.
- [ ] Estimand, identification, estimation, inference assumptions separated.
- [ ] Data provenance, splits, leakage checks.
- [ ] Baselines with equal budget.
- [ ] Effect sizes, intervals, methods, $n$, seeds.
- [ ] Multiplicity family and correction.
- [ ] Ablations and negative results.
- [ ] Artifact reproduces on a clean machine.

## 35.7 Communication checklist
- [ ] R01–R24 within thresholds.
- [ ] Cold read 10/10 for every DEP-0 theorem.
- [ ] No banned phrases.
- [ ] Roadmaps and section preambles present.
- [ ] DEP-2 containment verified.
- [ ] Figures self-contained with provenance.
- [ ] Abstract/title/intro claims mapped and non-inflated.
- [ ] Limitations section present and specific.

## 35.8 Repository checklist
- [ ] Atomic files; statement/proof separated.
- [ ] No junk-drawer files.
- [ ] Ledgers generated and current.
- [ ] Quarantine excluded and ticketed.
- [ ] Waivers written, owned, expiring.
- [ ] Extermination reports archived.
- [ ] Toolchain pinned; build deterministic.

---

# 36. Worked examples

## 36.1 Compliant DEP-0 statement
```latex
\DepBlock{
  ID=lem.ui_dct, CLASS=DEP-0, STATUS=proved, COMPLETE=complete,
  WHAT={L1 convergence of a uniformly integrable, in-probability convergent sequence.},
  WHY={Needed at S12 of thm.main to exchange limit and expectation without a dominating function, which H3 does not provide.},
  AMBIENT={conv.prob.complete},
  HYP={H1,H2,H3}, QUANTIFIERS={A A A},
  DEPENDS={def.uniform_integrability, thm.vitali},
  AXIOMS={ZFC, AC_omega (choice of subsequence indices; see choice.004)},
  CONSTANTS={none}, INTERCHANGE={swap.014},
  UNIFORMITY={n/a}, EFFECTIVE={no; modulus not extracted},
  WITNESS={ex.ui_bounded_L2}, SHARPNESS={H2: sharp (cex.escaping_mass); H3: sharp (cex.heavy_tail)},
  DEGENERACY={dep/out/degeneracy/lem_ui_dct.json, 16/16},
  EVIDENCE={proofs/proof_lem_ui_dct.tex},
  GAP={none}, OWNER={a.author}, REVIEW={2026-10-28, b.referee, 10/10},
}
\begin{deplemma}[id=lem.ui_dct]
\DepAmbient{conv.prob.complete}
Let \DepHyp{H1}{$(X_n)_{n\ge1}$ and $X$ be real-valued random variables on $(\Omega,\cF,\mathbb{P})$},
    \DepHyp{H2}{$X_n \to X$ in probability}, and
    \DepHyp{H3}{$\{X_n\}_{n\ge1}$ is uniformly integrable (\DepRef{def.uniform_integrability})}.
Then $X \in L^1(\mathbb{P})$ and $\lim_{n\to\infty}\mathbb{E}_{\mathbb{P}}\abs{X_n - X} = 0$.
\end{deplemma}
```

## 36.2 Compliant proof skeleton
```latex
\begin{depproof}[id=proof.lem.ui_dct]
\DepRoadmap{Step 1: integrability of the limit via Fatou along an a.s. subsequence.
            Step 2: uniform integrability of the differences.
            Step 3: truncation estimate and parameter selection.}

\DepStep{S1}{X \in L^1(\mathbb{P})}{by=thm.fatou, uses={H2,S0}, discharges={fatou.nonneg, fatou.measurable}}
\DepSubseq{S0}{n_k}{justification={thm.prob_to_ae_subseq, uses={H2}}}
\DepStep{S2}{\{X_n - X\} \text{ is UI}}{by=lem.ui_diff, uses={H3,S1}}
\DepParamOrder{choose K = K(\eps) by H3 and S2; then n_0 = n_0(\eps,K) by H2}
\DepStep{S3}{\mathbb{E}\abs{X_n-X} \le \eps + K\,\mathbb{P}(\abs{X_n-X} > \eps/K)}{by=lem.truncation_split, uses={S2}}
\DepStep{S4}{\mathbb{E}\abs{X_n-X} \le 2\eps \quad (n \ge n_0)}{by=algebra:linarith, uses={H2,S3}}
\DepClose{goal}{S4}
\end{depproof}
```
Note: `S0` precedes `S1` in dependency but is displayed after for readability; the DAG, not the display order, is normative. The linter checks the DAG.

## 36.3 Compliant gap declaration
```latex
\DepBlock{
  ID=thm.main, STATUS=proved-modulo, COMPLETE=gap-declared,
  GAP={gap.tightness_step},
  WHAT={...}, WHY={...},
  ...
}
% Abstract mapping:
% claim.abstract.1 -> thm.main (proved-modulo) -> abstract text MUST say
% "conditional on Lemma 5.3, whose proof is incomplete" or the claim must be removed.
```

## 36.4 Non-compliant specimen (annotated)
```latex
Theorem. Let f_n be a sequence of continuous functions converging to f.
Then \int f_n \to \int f.                       % (1) no domain, no measure, no mode,
                                                % (2) false as stated, (3) no hypotheses IDs
Proof. Clearly f is continuous, and by a standard argument we may pass to the
limit under the integral. The general case follows similarly. \qed
% (4) "clearly" — false: pointwise limit of continuous need not be continuous
% (5) "standard argument" — no theorem, no domination, Law 2 + Law 5
% (6) "general case similarly" — no reference, no substitution
% (7) no annotation block, no witness, no degeneracy, no status
```
Verdict: `EXTERMINATE`, Severity 0, seven distinct violations. This is the canonical failure mode the standard exists to prevent.

---

# 37. Submission and release qualification

A document is DEP&CC-qualified only if it ships:
1. Pinned toolchain manifest and deterministic build evidence.
2. Generated symbol registry, notation table, results table.
3. Complete hypothesis, constant, interchange, choice, and axiom ledgers.
4. Acyclic dependency graph and (if required) dependency figure.
5. Gap register with blast radii; zero expired gaps.
6. Degeneracy Crucible artifacts meeting quota for every DEP-0 node.
7. Sharpness records or ticketed unknowns for every DEP-0 hypothesis.
8. Non-vacuity witnesses for every DEP-0 theorem.
9. Claim–evidence mapping with zero inflation findings.
10. Cold-read scores of 10/10 for DEP-0.
11. Readability report within thresholds.
12. Pinned, pinpointed bibliography with retraction-check timestamps.
13. Formal artifacts with zero admitted tokens, matching axiom ledgers, and signed fidelity mappings (if `machine-checked` claimed).
14. Numerical certificates and arithmetic-class declarations (if `verified-numeric` claimed).
15. Empirical artifacts at `A1` or better, with design declarations (if `empirical` claimed).
16. Optimality records for every optimality/sharpness/tightness claim.
17. Limitations section.
18. Waiver list (all unexpired) and extermination report summary.
19. `dep_lint` run at zero Severity 0/1.

Missing any applicable artifact means the document is **not qualified**, regardless of whether the mathematics is correct. Correctness that cannot be audited is not a result; it is a claim.

---

# 38. Final clause

> DEP&CC does not negotiate with unjustified inference.

If a statement cannot show:
- what it assumes,
- what it asserts,
- in what order the quantifiers come,
- what it depends on,
- which axioms it uses,
- where each hypothesis is discharged,
- why each interchange is legal,
- what its constants depend on,
- what witness makes it non-vacuous,
- what breaks when a hypothesis is dropped,
- what its epistemic status is,
- and how a competent reader reconstructs it without asking,

then it is not a theorem. It is a sentence.

It is repaired, downgraded, quarantined, or exterminated.

**The mathematics does not care about your intuition.
The referee does not care about your reputation.
The reader does not care about your elegance.
Prove it completely. State it exactly. Write it so it can be checked.**

---

# Appendix A — Banned and restricted phrase table (normative)

| Phrase | Class | Required replacement |
|---|---|---|
| clearly / obviously / trivially / evidently / plainly | Banned DEP-0/1 | `\DepStep` with a `by` token |
| it is easy to see / one sees immediately | Banned | explicit step |
| a standard argument / by standard techniques | Banned | named theorem + discharge |
| routine computation / after some algebra | Banned | `algebra:<procedure>` + certificate |
| it can be shown / it follows that (no reference) | Banned | step ID |
| well known | Restricted | pinpoint citation |
| left to the reader / exercise | Banned DEP-0 | full proof or registered gap |
| similarly / analogously / likewise | Restricted | step ID + explicit substitution |
| the general case follows similarly | Banned | the general argument |
| mutatis mutandis | Restricted | list the mutations |
| WLOG / without loss of generality | Restricted | `\DepWlog` with invariance + reduction |
| by symmetry | Restricted | invariance proof |
| it suffices to show | Restricted | `\DepSuffices` with reduction proof |
| for sufficiently large n | Restricted | $\exists N_0(\text{deps}) \; \forall n\ge N_0$ |
| for any | Banned DEP-0 | "for every" / "for some" |
| almost all / almost every | Restricted | measure or cofinite, named |
| generically / typically | Restricted/Banned | topology or measure, named |
| under mild / suitable / appropriate assumptions | Banned | the assumptions |
| canonical / natural | Restricted | construction + naturality square |
| essentially unique | Restricted | uniqueness up to a named equivalence |
| the obvious map | Banned | define it |
| up to constants | Restricted | constant ledger |
| optimal / sharp / tight | Restricted | optimality record |
| novel / new / first | Restricted (DEP-2 only) | priority record |
| powerful / elegant / beautiful / deep / remarkable | Banned DEP-0/1 | delete |
| significantly (non-statistical) | Banned | effect size + interval, or delete |
| state-of-the-art | Restricted | comparison record with equal budgets |
| we conjecture (in a theorem) | Banned | `depconjecture` environment |
| it is conjectured that (as support) | Banned | cannot support a `complete` node |

---

# Appendix B — Convention manifest (mandatory keys, minimum set)

```yaml
conv.NN.includes_zero: true
conv.subset.symbol: '\subseteq (non-proper); \subsetneq (proper)'
conv.positive: '> 0'          # nonnegative written explicitly
conv.increasing: 'non-strict' # strictly increasing written explicitly
conv.ring: 'associative, unital, 1 != 0, not necessarily commutative'
conv.module: 'left, unital'
conv.algebra: 'associative, unital, over a commutative ring unless stated'
conv.graph: 'finite, simple, undirected, loopless'
conv.manifold: 'second countable, Hausdorff, without boundary, C^\infty'
conv.measure: 'countably additive, on a sigma-algebra; completeness stated per use'
conv.measure.default: 'Lebesgue on R^d when unadorned; otherwise named'
conv.integral: 'Lebesgue unless the symbol \int_{Riemann} is used'
conv.Lp: 'equivalence classes; measure named at each use'
conv.hilbert: 'complex, separable unless stated; inner product linear in the first argument'
conv.smooth: 'C^\infty'
conv.log: 'natural log; \log_2 written explicitly; entropy in nats'
conv.fourier: '\hat f(\xi) = \int f(x) e^{-2\pi i x\xi} dx'
conv.normal: 'N(mean, variance)'
conv.gamma: 'Gamma(shape, rate)'
conv.complexity.model: 'multi-tape TM; bit length; deterministic unless stated'
conv.wordram: 'w = Theta(log n)'
conv.w.h.p.: '1 - n^{-c} for every constant c > 0, with n the declared input size'
conv.category.size: 'relative to a fixed universe U; Set = U-small sets'
conv.ordinal.omega: 'first infinite ordinal; NN when the order is irrelevant'
conv.empty_sum: 0
conv.empty_product: 1
conv.empty_sup: '-\infty (extended reals)'
conv.zero_to_zero: '0^0 = 1 in combinatorial contexts; undefined in analysis; stated per use'
conv.decimal_rounding: 'round-half-even; reported to 3 significant figures unless stated'
conv.iid: 'mutually independent, identically distributed'
conv.ae: 'with respect to the measure named at the point of use'
conv.universe: 'no Grothendieck universes; large categories handled by size annotations'
```
Every key must be fixed. "Standard" is not a value.

---

# Appendix C — Hypothesis ledger template

| Hyp ID | Node | Text | Discharged at | External source | Necessary? | Counterexample |
|---|---|---|---|---|---|---|
| H1 | thm.main | $X$ Polish | S2, S7 | — | sharp | cex.nonpolish |
| H2 | thm.main | $\mu$ $\sigma$-finite | S4 | thm.radon_nikodym | sharp | cex.counting_measure |
| H3 | thm.main | $f$ bounded | — | — | unused (marked) | rem.H3_unnecessary |

---

# Appendix D — Interchange ledger template

| ID | Location | Exchange | Theorem | Preconditions | Status |
|---|---|---|---|---|---|
| swap.007 | proof.main:S12 | $\lim \int \to \int \lim$ | DCT | measurability S4; a.e. conv S9; domination S11 | discharged |
| swap.011 | proof.main:S18 | $\int\int \to \int\int$ | Fubini | $\sigma$-finite H2; product-measurable S15; $\int|f| < \infty$ S17 | discharged |
| swap.014 | proof.ui:S3 | $\lim \mathbb{E} \to \mathbb{E} \lim$ | Vitali | in prob H2; UI H3; tightness (finite measure) | discharged |

---

# Appendix E — Degeneracy probe record template

```yaml
node: thm.main
hypothesis_count: 3
quota: 20
probes:
  - {id: dg.empty, instantiation: 'X = emptyset', applicable: false, reason: 'H1 requires nonempty'}
  - {id: dg.singleton, instantiation: 'X = {*}', hyps_hold: true, conclusion_holds: true, verdict: passes}
  - {id: dg.pointmass, instantiation: 'mu = delta_x', hyps_hold: true, conclusion_holds: true, verdict: passes}
  - {id: dg.nonsigmafinite, instantiation: 'mu = counting on R', hyps_hold: false, fails: H2, verdict: 'counterexample -> cex.counting_measure'}
  # ... 16 more
summary: {applicable: 20, executed: 20, passes: 18, counterexamples: 2, na: 4}
```

---

# Appendix F — Permitted justification tokens (closed set)

`hypothesis:<id>` · `definition:<id>` · `thm.<id>` / `lem.<id>` / `prop.<id>` / `cor.<id>` (internal) · `ext:<bibkey>:<locator>` · `axiom:<id>` · `rule:modus-ponens` · `rule:universal-instantiation` · `rule:existential-introduction` · `rule:conjunction-intro/elim` · `rule:disjunction-elim` · `rule:contraposition` · `rule:contradiction` (LEM ledger) · `rule:substitution` (with renaming if binders present) · `algebra:ring` · `algebra:field_simp` · `algebra:linarith` · `algebra:nlinarith` · `algebra:omega` · `algebra:cas:<certificate-id>` · `case-analysis` (with exhaustiveness step) · `induction-hypothesis:<id>` · `abuse:<id>` · `computation:certified:<artifact-id>`.

Nothing else. In particular, no token whose meaning is "trust me".

---

# Appendix G — Readability threshold quick reference

| Metric | DEP-0 | Where |
|---|---|---|
| Max sentence words | 40 | R01 |
| Mean sentence words | 22 | R02 |
| Symbols per display | 9 | R04 |
| Quantifier alternations | 3 | R06 |
| Cognitive stack | 3 | R08 |
| Notation distance | 2 pages | R09 |
| Forward references | 0 | R10 |
| Proof length | 3 pages / 40 steps | R11 |
| Step fan-in | 5 | R12 |
| Chain length | 5 | R13 |
| IGU per step | 1 | 11.2 |
| Cold read | 10/10 | R23 |
| Banned phrases | 0 | R22 |

---

# Appendix H — Status decision procedure

```text
Is there a kernel-checked proof with zero admitted tokens and a signed fidelity map?
  yes -> machine-checked
  no  -> Is there a complete human proof meeting DEP-0?
           yes -> Are all external dependencies proved/complete?
                    yes -> proved
                    no  -> proved-modulo   (register gaps; propagate)
           no  -> Is the claim proved under a named unproved hypothesis?
                    yes -> conditional     (condition in the statement AND abstract)
                    no  -> Is it established by certified computation on a declared finite domain?
                             yes -> verified-numeric  (never "proved" for infinite domains)
                             no  -> Is it supported by experiment?
                                      yes -> empirical (design + artifact required)
                                      no  -> Is there an outline?
                                               yes -> sketched (gap registered)
                                               no  -> conjectural / heuristic (DEP-2 only)
```

---

# Appendix I — Glossary (selected)

**Blast radius** — transitive closure of dependents of an invalidated node.
**Cold read** — reconstruction without author contact (21.4).
**Degeneracy Crucible** — mandatory battery of degenerate instantiations (30.3).
**Discharge** — to supply and reference a justification for an obligation.
**Fidelity mapping** — audited correspondence between prose and formal statement (19.5).
**IGU** — one atomic justification (11.2).
**Interchange** — exchange of two limiting operations (Law 5).
**Induction loading** — generalizing all varying parameters before inducting (11.4).
**Status contamination** — a `complete` node depending on an incomplete one (5.5).
**Statement-fidelity mismatch** — the formal theorem does not mean the prose theorem (19.5).
**Exterminate** — block, downgrade, quarantine, retract, or delete (34).

---

# Appendix J — Minimum viable adoption (for projects that cannot adopt everything at once)

Adoption must be monotone and declared. A project may declare `DEP&CC 2.0 Profile: Core`, which requires, non-negotiably:
1. Laws 1–14 with no exceptions.
2. Annotation blocks with `STATUS`, `COMPLETE`, `HYP`, `DEPENDS`, `GAP`.
3. Symbol registry and convention manifest.
4. Hypothesis discharge and DAG acyclicity.
5. Interchange ledger.
6. Zero claim inflation.
7. Zero admitted tokens in anything called verified.
8. Banned-phrase list.
9. `dep_lint` at zero Severity 0.

Everything else may be phased in with a dated plan in the manifest. **Core is not a permanent resting place.** A profile declaration without a dated full-conformance plan is Severity 1.

---

*End of DEP&CC 2.0.*
