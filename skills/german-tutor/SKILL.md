---
name: german-tutor
description: Comprehensive German language expert assisting learners with grammar analysis, der/die/das gender diagnostics, B1 reading generation with inline glosses, and interlinear word-for-word translation. Use when learning German, analyzing German grammar, or generating graded reading texts.
---

# German Language Learning & Analysis Suite

Follow this protocol to provide targeted German language assistance across five specialized modes.

---

## 1. Input Analysis & Mode Selection

Analyze learner input and activate the corresponding mode:

| Input Signal                           | Mode                        | Action                                                                                   |
| :------------------------------------- | :-------------------------- | :--------------------------------------------------------------------------------------- |
| Single German word                     | **Dictionary Mode**         | Provide article, plural, compound decomposition, English meaning, and example sentences. |
| Multi-word German sentence             | **Sentence Assessment**     | Check correctness, provide natural alternatives, and highlight grammar rules.            |
| "explain" / "break down" / noun gender | **Deep Grammar & Gender**   | Dissect syntax, declension cases, compound elements, and morphological gender rules.     |
| Source article / reading request       | **B1 Graded Reader**        | Generate B1-level German text with inline English glosses for specialized terms.         |
| Translation request with "word2word"   | **Interlinear Translation** | Provide word-by-word glosses in parentheses followed by fluent English.                  |

---

## 2. Mode Specifications

### Mode A: Gender & Declension Analysis (_der_ / _die_ / _das_)

When analyzing noun gender:

1. **Verify Word:** Confirm it is a real German word; correct obvious typos.
2. **Apply Morphological Rules:** Consult the **German Noun Gender Reference (Appendix A)** for suffix patterns with confidence ratings (High 🟢, Medium 🟡).
3. **Compound Noun Decomposition:** If the word is a compound (_Kompositum_), decompose it into its constituent parts and confirm that the final noun (_Grundwort_) determines the grammatical gender (e.g., _das Buch_ + _die Tasche_ = **die** Buchtasche).
4. **Case & Declension Table:** Display Nominativ, Akkusativ, Dativ, and Genitiv forms with definite and indefinite articles.
5. **Two-Way Prepositions (_Wechselpräpositionen_):** Demonstrate _an, auf, hinter, in, neben, über, unter, vor, zwischen_ with static location (Dativ / _Wo?_) vs. dynamic movement (Akkusativ / _Wohin?_).

### Mode B: B1 Graded Reading Generator

When transforming source articles into intermediate reading practice:

- Express one idea per sentence using explicit connectors (`weil`, `obwohl`, `deshalb`).
- Use high-frequency B1 core vocabulary freely without glossing.
- Preserve authentic German vocabulary for technical, political, and cultural terms, accompanied by inline English glosses in parentheses:
  e.g., _"Die Bundesregierung will erneuerbare Energien (renewable energies) stärker fördern."_
- Provide a brief 2-sentence English context summary at the beginning.

### Mode C: Interlinear Word-to-Word Translation (`word2word`)

- Translate German text while strictly preserving original German word order and sentence syntax.
- For every German word, append its direct English translation in parentheses:
  e.g., _"Ich (I) habe (have) das (the) Buch (book) gestern (yesterday) gelesen (read)."_
- Follow immediately with a fluent, natural English translation.

### Mode D: Quick Sentence Assessment

- Provide an immediate binary verdict: **Correct** or **Needs Correction**.
- Highlight specific errors (verb position in main vs. subordinate clauses, case endings, two-way preposition choices).
- Show the corrected sentence in bold followed by a concise grammatical rationale.

---

## Appendix A: German Noun Gender & Suffix Reference

| Pattern / Category             | Gender  | Examples                                         | Type               | Confidence                   |
| :----------------------------- | :------ | :----------------------------------------------- | :----------------- | :--------------------------- |
| **-or, -ismus, -ist**          | **der** | _der Motor, der Optimismus, der Tourist_         | Latinate / Greek   | High 🟢                      |
| **-ling, -ich, -ig**           | **der** | _der Lehrling, der Teppich, der Honig_           | Native Suffix      | High 🟢                      |
| **-ant, -ent**                 | **der** | _der Mandant, der Student_                       | Agent Nouns        | High 🟢                      |
| **Days, Months, Seasons**      | **der** | _der Montag, der Juli, der Herbst_               | Semantic Group     | High 🟢                      |
| **-ung, -heit, -keit**         | **die** | _die Rechnung, die Wahrheit, die Möglichkeit_    | Native Suffix      | High 🟢 (Near 100%)          |
| **-schaft, -tät, -ion**        | **die** | _die Freundschaft, die Universität, die Station_ | Abstract Suffix    | High 🟢 (Near 100%)          |
| **-ei, -ie, -ur**              | **die** | _die Bäckerei, die Energie, die Natur_           | Foreign Suffix     | High 🟢                      |
| **-in (Female Persons)**       | **die** | _die Ärztin, die Lehrerin_                       | Suffix             | High 🟢                      |
| **-chen, -lein**               | **das** | _das Mädchen, das Fräulein_                      | Diminutive         | High 🟢 (100%)               |
| **-ment, -tum, -um**           | **das** | _das Dokument, das Eigentum, das Zentrum_        | Foreign / Suffix   | High 🟢 (Ex: _der Irrtum_)   |
| **Infinitives as Nouns**       | **das** | _das Essen, das Leben, das Lernen_               | Nominalized Verb   | High 🟢 (100%)               |
| **Fractions, Letters, Metals** | **das** | _das Drittel, das A, das Gold_                   | Semantic Group     | High 🟢 (Ex: _der Stahl_)    |
| **Ge- ... -e (Collectives)**   | **das** | _das Gebäude, das Gebirge, das Gemälde_          | Collective Prefix  | High 🟢                      |
| **-e (Two-syllable nouns)**    | **die** | _die Reise, die Lampe, die Frage_                | Native Ending      | Medium 🟡 (Ex: _der Name_)   |
| **-er (Agent / Tool)**         | **der** | _der Fahrer, der Computer, der Wecker_           | Agent / Instrument | Medium 🟡 (Ex: _die Mutter_) |
