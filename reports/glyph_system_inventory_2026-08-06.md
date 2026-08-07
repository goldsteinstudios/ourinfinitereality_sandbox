# The constructed glyph system: inventory

**Searched:** all 11 remote branches (filenames and content), the working tree, and `archive/MANIFEST.csv` (the off-repo binary catalogue). **Date:** 2026-08-06.

**Read this first.** The material splits into two strands that share a word and are not the same thing. Strand one is the **Guodian glyph corpus** — photographs and crops of actual Chu characters, 1,073 files, well covered elsewhere. Strand two is the **constructed system** — a grid, a stroke vocabulary, a topological classifier, and a composition tool. Only strand two is inventoried below. Where a file's name suggests strand two and it belongs to strand one, that is flagged.

---

## 1. The working tool — the most advanced piece by a wide margin

Everything here lives on branch **`claude/glyph-composer-v3-fQABj`**, which is otherwise unmerged.

| File | Size | Date | What it is |
|---|---|---|---|
| `src/components/GlyphComposer.tsx` | 82 KB, 2,571 lines | **2026-03-15** | The whole system. Grid enumerator, topological classifier, T-junction analyzer, and compound composer in one component. |
| `src/composer-main.tsx` | 246 B | 2026-03-09 | Vite entrypoint, touch-oriented, separate from the main site app. |
| `composer.html` | 529 B | 2026-03-09 | Standalone page shell for the above. |
| `docs/composer/index.html` + `assets/composer-DX8F6cAP.js` | built bundle | 2026-03-09 | Compiled deployment copy, served via GitHub Pages. |
| `docs/composer/composer_backup/` | built bundle | 2026-03-09 | A second built copy. Also present on `claude/catch-up-UKmEu`. |

**Stage: working, unfinished, parked mid-edit.** The last commit is literally `Save WIP: GlyphComposer v3 updates, framework docs, config changes`. Nothing after 2026-03-15 on that branch, and the branch has never been merged into `main` or `research-archive`.

### What the tool actually does, read from the code

**Grid and enumeration.** A configurable node grid (`gridSize`, default **3**) with optional diagonals. `getEdges` generates the edge set; `indexToEdges` maps an integer index to a subset of edges, so the whole space of figures on a grid is enumerable by counting. That is the combinatorial matrix.

**Graph analysis.** `buildGraph` turns a bit-pattern into an adjacency map, then: `getComponents` (connected parts), `hasCycle` (closed loops), `getDegreeProfile` (how many nodes of each degree), `edgeDirection` / `isCollinear` / `pathHasTurn` (whether a stroke actually bends), `walkBranchLength` (how far a branch runs before it forks or ends), `getPerimeterInfo` (perimeter total, active perimeter, ratio, interior activity).

**T-junction analysis** — `analyzeTJunction`, its own titled section of the file. Finds the degree-3 node, then reports: `isT` / `isY`, axis direction, lateral direction, axis length split into both halves (`axisLen1`, `axisLen2`), lateral length, axis orientation, symmetry, and lateral class. This is the most developed single piece of analysis in the codebase.

**The classification scheme** — `TOPO_CATEGORIES`, thirteen buckets, each with a display icon:

Line (─) · Bend (└) · Sideways T (⊣) · Y Fork (┴) · Cross (┼) · Multi-fork (┳) · Loop (○) · Enclosure (口) · Bisected (日) · Partitioned (田) · Multi-part (‖) · Complex (⁂) · Promoted (→)

**Composition rules** — the `LAYOUTS` table, which borrows the Unicode Ideographic Description Characters as its operator set: `single` (□, 1 slot), then ⿰ left-right, ⿱ top-bottom, ⿴ surround, ⿷, ⿵, ⿶ (2 slots each), and ⿲ (3 slots). Compounds nest, with recursion capped at depth 6.

**Promotion** — a `Compound` carries `promoted: boolean`, and "Promoted" is one of the topological categories. A composed compound can be pushed back into the palette as a primitive for further composition. That is the recursion of the framework, built into the tool.

**Metadata a compound can carry** — `definitions[]` with a `source` field (the code names *39017.com* and *Shuowen Jiezi*), `images[]`, `guodianLocation`, `locked`, `label`, `timestamp`. So the tool was built to be pointed at real Guodian graphs, not only at invented ones.

**Persistence** — `localStorage` under `glyph-composer-library`, with JSON export and import. **Your composed library is in browser storage, not in the repo.** If it matters, export it before that profile is ever cleared.

---

## 2. The primitives database — a good schema and an empty table

| File | Size | Date | What it is |
|---|---|---|---|
| `data/primitives/schema.json` | 2.8 KB | **2026-02-26** | JSON-Schema for a stroke-primitive database: id, name, category (`stroke` / `component` / `semantic-unit`), structural role (`enclosure` / `base` / `modifier`), exemplars with slip and position, variants, frequency. Plus a `decompositions` object mapping each glyph to its primitives with position (`top`/`bottom`/`left`/`right`/`center`/`enclosing`/`enclosed`) and normalized bounding boxes. |
| `data/primitives/primitives.json` | 1.0 KB | 2026-02-26 | The database itself, `version 0.1.0`. **Four entries. Every exemplar list empty. Every frequency null. The decompositions array is empty.** |

The four entries, verbatim: **P001** "Single curve, arc shape. Ignore line thickness/ink artifacts." · **人** "Two strokes meeting at top, spreading downward. Person/figure shape." · **P002** "Vertical stroke with horizontal stroke extending right from middle. Inverted T or hook shape." · **P003** "Three strokes radiating outward from a common point. Fan or spray pattern."

Its own stated discipline: *"Visual stroke primitives — purely visual patterns, no linguistic knowledge."* And: *"Primitive IDs are arbitrary labels. You define what they look like by providing exemplar images."*

**Stage: schema complete, data barely started, abandoned after three days.** The commit trail is `Add primitives database schema and annotator tool` then `Add P003 primitive: three strokes radiating from common point`, both 2026-02-26, and nothing since. Present on `main`, `research-archive`, `rsm/v9-canon`, `fix/guodian-duplicate-slips` and `claude/catch-up-UKmEu` — so it propagated widely while staying empty.

**Note the drift.** The schema is Guodian-facing ("Stroke primitives extracted from Guodian bamboo slip glyphs", frequency counted against Laozi A). `primitives.json` is register-neutral and forbids linguistic knowledge. Two different projects in one directory, three weeks apart. The composer, a month later, went with neither and built its own vocabulary from graph topology.

---

## 3. The off-repo binaries, and a correction

Catalogued in `archive/MANIFEST.csv`, physically in the gitignored `research/archive/icloud_import/`.

| File | Size | Date | Note |
|---|---|---|---|
| `Scripts etc/Glyph Explorer/glyph explorer.pdf` | **65,470 B** | 2026-03-09 | Real file. Also duplicated at `RSM Version History/RSM v5/RSM v5.2/glyph explorer.pdf`, same size, same date. |
| `Scripts etc/Glyph Explorer/glyph matrix.pdf` | **50,190 B** | 2026-03-18 | Real file, and the **latest-dated artifact in the whole strand** — three days after the composer's last commit. Duplicate `glyph matrix copy.pdf`, identical size. |
| `glyph_matrix_7pt_16384x16384.png` (+ copy) | **0 B** | 2026-03-18 | Empty at source. Probably unrecoverable. |

**Correction to `reports/recovery_needed.md` §3c.** That report states all three of `glyph explorer.pdf`, `glyph matrix.pdf` and `glyph_matrix_7pt_16384x16384.png` are "recorded at **0 bytes** in the manifest — corrupt/empty at source; recovery may be impossible." The manifest does not say that. **Only the two PNGs are 0 bytes.** Both PDFs carry real sizes and are recoverable from your machine. Two documents were written off that are not lost.

**The `7pt` in that filename is worth noticing.** The composer's grid size is a live parameter defaulting to 3. A seven-point configuration is a much larger enumeration than anything the default produces, and a 16384-pixel square render is what you would make to look at all of it at once. Stated as an observation, not a derivation: nothing in the code fixes the relationship between the grid parameter and that image's dimensions, and I have not seen the file.

---

## 4. What does not exist

**No Colab spec, and no notebook of any kind.** Zero `.ipynb` files on any of the eleven branches. Zero occurrences of "colab" in any tracked file on any branch, and zero rows in `archive/MANIFEST.csv`. If a Colab spec exists it is outside the repository and outside the iCloud archive that was catalogued — a chat, a Drive doc, or a browser tab.

**No Notability exports.** Zero rows matching "notability" in the manifest, zero on any branch.

**No hand-drawn glyph sketches identifiable as such.** The nearest things, both flagged elsewhere: the **seven missing NotebookLM source images** (`IMG_2372.png`, `IMG_2506.png`, `IMG_2538.jpeg`, `IMG_8606.jpeg`, `IMG_8618.jpeg` and two more, itemized in `reports/recovery_needed.md` §3b), which are the hand-drawn geometry the Gₙ/Bₙ/Pₙ notation was read off and which the recovery report calls the highest-value absent asset in the corpus; and **24 undescribed screenshots** from 5 and 12 November 2025 in the manifest's `Visuals/` folder.

---

## 5. A trap in the naming

`structural_primitives.md` — present on `claude/glyph-composer-v3-fQABj` (2026-03-15), `guodian-rsm-rebuild`, `sphere_model`, `docset-pipeline` (as `rsm/takes/`), and `archive/rsm-versions/v0.971/090-structural-primitivesmd.md` — **has nothing to do with the glyph system.** It is the v5.5 logic mapping: the 14-step entailment chain, P₀ / Oₙ / Gₙ / Bₙ / Pₙ / Rₙ / 1ₙ, the Lorentz correspondence, the dimensionality argument, the 道生一 table. "Primitives" there means the framework's structural elements.

Same for `archive/rsm-versions/v0.99/001-computings-ancient-roots-and-future-primitiveness.md`.

Any future search for the glyph system will surface these first and they will waste an hour each time.

---

## 6. The adjacent strand, for completeness

`python_analysis/` on the same branch (last touched **2025-12-05**) is a Guodian radical-analysis suite, not the constructed system: `radical_cooccurrence.py`, `radical_dictionary.py`, `translation_engine.py`, `ttc_parser.py`, `cross_reference_extractor.py`, plus outputs including `cross_reference_network.html`/`.json` and a set of PNG visualizations. It is the closest thing in the repo to "high-res glyph analysis," and it analyses the historical corpus rather than the invented one.

---

## 7. Stage summary

| Piece | Stage |
|---|---|
| Composer tool | **Working and deployed**, parked mid-edit 2026-03-15, on an unmerged branch |
| Topological classifier (13 categories) | **Complete**, in code, unwritten anywhere in prose |
| T-junction analysis | **Most developed single analysis**, in code only |
| Composition operators (IDC layouts) | **Complete**, 8 layouts, nesting to depth 6 |
| Promotion loop | **Implemented**, undocumented |
| Primitives database | **Schema complete, 4 rows, no exemplars, no decompositions.** Stalled 2026-02-26 |
| Composed library | **In browser localStorage only.** Not in the repo |
| Glyph explorer / matrix PDFs | **Off-repo, intact, recoverable.** Latest artifact 2026-03-18 |
| 16384px matrix render | **0 bytes.** Probably gone |
| Colab spec | **Not found anywhere** |
| Notability sketches | **Not found anywhere** |
| Written definition of the system | **Does not exist.** The scheme lives only as TypeScript |

The single largest gap is the last row. There is a complete classification scheme and a working composition grammar in this project, and no document anywhere states them in words.

---

*Not sealed. Section 3's correction is checkable against `archive/MANIFEST.csv`; everything else is read from tracked files at the paths and dates given.*
