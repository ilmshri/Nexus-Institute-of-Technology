# Arabic terminology — decisions, sources, and open questions for the owner

Working glossary for the Y1S1 Arabic pass. Terms are fixed here once and reused
across all 66 lessons, so a correction made now propagates cheaply and a
correction made late does not.

**Owner: the "NEEDS YOUR CALL" table at the bottom is the one to read.** Those
are terms I could not settle from sources and did not want to silently invent.

## Source assessment (which references to trust, and how much)

**ARABTERM — arabterm.org — BEST SOURCE FOUND. Use this first.**
Trilingual EN/DE/FR + Arabic technical dictionary, 156,140 entries / 513,950
terms, produced by GIZ with the Arab League. Decisive feature: entries can be
marked *"Unified Arabic term validated during the Arabization Congress
organized by ALECSO"* — i.e. Arab League standardisation, not a crowd guess.
The **Automotive Engineering** volume carries categories that are squarely our
curriculum: *Mechanical Engineering*, *Mechanical Vibrations*, *Machine
elements*, *Hydraulics*, *Heat Engine*, *Measuring Techniques*, *Friction,
Lubrication, Bearings, Seals*, *Material Science*, *Manufacturing
technologies*.
Practical notes for whoever uses it next: the site is 2009-era TYPO3 +
MooTools and its **search box is broken** in a modern browser (the form does
not submit). Browse by direct URL instead:
`arabterm.org/index.php?id=41&L=1&tx_3m5techdict_pi1[filterCategory]=N`
where `N=1` is Automotive Engineering. Sub-category filtering is rendered
client-side and could not be driven by URL; paging works
(`Page 1 2 3 ... 151`). WebFetch is fine on it; no 403.

**Reverso Context — context.reverso.net — USE ONLY AS A FREQUENCY SIGNAL.**
It is a parallel corpus (its own footer recommends "Subtitles for movies and
TV series"), not a curated glossary, and it is demonstrably wrong often enough
to be dangerous for teaching text. Errors found in minutes of use:
- "he always dreamt of becoming a mechanical engineer" rendered
  **"مهندسًا مدنياً"** — *civil* engineer.
- "Practically every company that designs and produces a product employs a
  mechanical engineer" → garbled Arabic that does not parse.
- "(it has a gauge pressure>0)" → **"(مقياس ضغطه<0)"** — the inequality is
  flipped.
- Its headline noun for *gauge pressure* is **مقياس الضغط**, which is a
  *pressure gauge* (the instrument), not gauge pressure (the quantity).
It is still useful for one question only: "is this Arabic rendering attested
in the wild?" It confirmed الضغط المقيس is real and surfaced الضغط المانومتري
as the formal/regulatory variant. Never take it as authority. Also note
WebFetch gets HTTP 403 on it; it must be read through a real browser.

## Conventions confirmed from real Arabic engineering sources

Checked against itqan.edu.sa's Arabic tree (`/ar/`) and Saudi industry pages.
itqan is genuinely bilingual — an EN/AR toggle, not an English-only site; the
Arabic tree is formal institutional MSA.

- **Latin acronyms stay inline, unchanged, inside Arabic sentences.** itqan
  writes `شهادات معتمدة من ASNT و ASME و TWI و AWS`. This matches what we do —
  every such run is additionally wrapped in `<bdi>` so bidi cannot flip the
  surrounding punctuation.
- **Glossing the Arabic term with the English on first use is normal Saudi
  technical practice**, not a crutch: tosypump.com.sa writes `الارتفاع (Head)`
  and `معدل التدفق Flow Rate`. Adopted for the few terms where the Arabic alone
  would be ambiguous to a Gulf practitioner.
- Register: formal MSA (فصحى), professor's voice — consistent with the
  English side's "no filler, no motivational language" rule.

## Settled, with evidence

| English | Arabic used | Basis |
|---|---|---|
| pump head | **الارتفاع** (glossed `<bdi>(Head)</bdi>` on first use) | tosypump.com.sa (Saudi mfr): `الارتفاع (Head)`, and `الـ Head أو الرأس`. **Corrected from my initial الرفع**, which is not the industry term. |
| hysteresis | **التخلّف** | Arabic Wikipedia (بطاء/تلاكؤ): البِطاء / التخلف / التخلفية. **Corrected from my invented compound التخلّف الهستيري.** |
| flow rate | معدل التدفق | tosypump.com.sa uses `معدل التدفق Flow Rate` |
| efficiency | الكفاءة | tosypump.com.sa `الكفاءة (Efficiency)` |
| limit (math) | النهاية | ar.wikipedia نهاية (رياضيات) |
| continuity | الاتصال | standard in Arabic calculus texts alongside الاستمرارية |
| derivative | المشتقّة | ar.wikipedia مشتق (رياضيات) |
| dimensional analysis | التحليل البُعدي | ar.wikipedia تحليل بعدي |
| mechanical inspection | الفحص الميكانيكي | itqan.edu.sa/ar |
| welding inspection | فحص اللحام | itqan.edu.sa/ar |
| NDT | فحص الاختبارات غير الإتلافية | itqan.edu.sa/ar |

## NEEDS YOUR CALL — I am not confident in these

These are in the committed text now, but flag anything wrong and I will fix it
everywhere in one pass. Ordered by how often they will recur across Y1S1.

| # | English | What I used | Alternatives I considered | Why I'm unsure |
|---|---|---|---|---|
| 1 | SI **prefix** (k, M, µ) | فخّ السابقة | **بادئة** (badi'a) | I think **بادئة** is the standard term for an SI prefix and سابقة is the grammar term. Likely a genuine error — please confirm and I'll change it. |
| 2 | **gauge** pressure | الضغط المقيس | الضغط النسبي، ضغط المقياس، الضغط الظاهري | Gulf plant usage may differ from textbook usage; "gauge vs absolute" is a recurring lesson theme so this repeats a lot. |
| 3 | **shaft** power | قدرة العمود | القدرة على العمود، قدرة المحور، قدرة العمود الدوّار | عمود vs محور for shaft — which do Kuwaiti/Gulf engineers actually say? |
| 4 | **runout** flow (pump curve) | تدفق الانفلات | أقصى تدفق، تدفق النهاية | I could not find an established Arabic rendering at all. This may be better left as `<bdi>runout</bdi>` glossed. |
| 5 | **live zero** (4–20 mA) | الصفر الحيّ | الصفر المرفوع، الصفر الحيّ | Literal calque; unsure it is used in practice. |
| 6 | data **historian** | المؤرّخ | الـ <bdi>Historian</bdi>، مسجّل البيانات | Practitioners may just say "Historian" in Latin. |
| 7 | **knockout drum** | وعاء فصل السحب | وعاء الفصل، نازع السوائل، طبل الفصل | Refinery term; Kuwaiti usage likely specific. |
| 8 | **pasteurizer** | مبستِر | جهاز البسترة، وحدة البسترة | مبستِر is a coinage; وحدة البسترة may read better. |
| 9 | compressor **trip** | الفصل | التعثّر، الفصل الوقائي، التوقّف الاضطراري | "Trip" is heavily used in plant Arabic, often untranslated. |
| 10 | **scan** (1 s scan rate) | مسح / مسحة | دورة مسح، معدل المسح | Instrumentation context. |
| 11 | **check valve** | صمام عدم الرجوع | صمام لا رجعي، صمام أحادي الاتجاه | Fairly standard but worth confirming Gulf preference. |
| 12 | **pressure head** | الارتفاع المكافئ للضغط | رأس الضغط، ضاغط السائل | Follows the corrected الارتفاع, but the compound is mine. |

## Rule I applied when unsure

Where no established Arabic term exists, I kept the English token in `<bdi>`
rather than invent one — inventing terminology in a teaching text is worse than
showing the learner the word they will actually meet on a Gulf plant floor. The
twelve above are cases where I *did* commit to an Arabic rendering and would
rather you overruled me than have it harden across 66 lessons.
