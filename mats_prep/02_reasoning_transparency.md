# Reasoning Transparency — notes from the actual document

**Source:** Luke Muehlhauser, "Reasoning Transparency," Open Philanthropy (now Coefficient
Giving), **1 December 2017**. Read from the OCR'd PDF in this repo. Everything below is
from the document itself, not from memory.

> **Correction notice.** An earlier version of this file was written from memory because
> the page was unreachable from my sandbox. Four things I listed as "probably in the
> document" are **not in it at all**: stating an epistemic status up front, naming the
> intended audience, using a table of contents and appendices, and anticipating the
> strongest objections to your own view. Those were my conflation with adjacent writing on
> epistemic norms. They may still be good practice; they are not this document's advice.
> I also guessed the GiveWell example was footnote 1. It isn't — it's a numbered section
> in the main body.

---

## The core question

The whole document is organised around making it easy for a reader to answer:

> **"How should I update my views in response to this?"**

Muehlhauser lists what a reader specifically wants to know:

- Has the author presented a fair or biased presentation of evidence and arguments?
- How much expertise does the author have here?
- How trustworthy is the author in general? What are their biases and conflicts of interest?
- **What was the research process that led to this analysis? What shortcuts were taken?**
- What rough level of confidence does the author have in each substantive claim?
- **What support does the author think they have for each substantive claim?**
- What are the most important takeaways, and **what could change the author's mind** about them?
- If there's data analysis: how were data collected, which analyses were done, can I access them?

He notes that standard scientific norms cover some of this (methods sections, open data,
COI statements) but not others — papers often "say little about roughly how confident the
authors are in different claims," or cite whole books "without giving any page numbers."

## The GiveWell example — and why it's a warning, not a model

The document opens with GiveWell's review of the Against Malaria Foundation as a
deliberately **"extreme" model of reasoning transparency, one that is probably more costly
than it's worth for most analysts.** That framing matters and is easy to miss.

What the AMF review does: a linked summary of key points; detailed answers to the specific
questions that bear on cost-effectiveness; a summary of the research process; **125
endnotes**, with the endnote generally providing the actual support (a quote from a paper,
a link to calculations, a quote from an expert interview); a comprehensive source table
with archived copies; and an explicit list of remaining open questions.

Muehlhauser then says plainly that most analysts, **including Open Philanthropy itself**,
don't and shouldn't invest that much. The rest of the document is about getting most of the
benefit cheaply.

> **For your exam:** this is the licence to be transparent *efficiently*. You have 100
> minutes. You cannot footnote everything. The document's own position is that you
> shouldn't try.

## The three top recommendations (verbatim)

1. **Open with a linked summary of key takeaways.**
2. **Throughout a document, indicate which considerations are most important to your key
   takeaways.**
3. **Throughout a document, indicate how confident you are in major claims, and what
   support you have for them.**

On #2, his own example of failing at it: an earlier report on carbs and obesity "doesn't
make it clear that the evidence from randomized controlled trials played the largest role
in my overall conclusions." The fix is to say, early, *which* evidence is carrying the
conclusion.

## Expressing confidence

Words are acceptable — "plausible," "likely," "unlikely," "very likely." Quantify **"when
it's worth the effort,"** partly because words like "plausible" are read differently by
different people. The document's examples span the whole range of effort:

| Style | Example from the document |
|---|---|
| Bounded probability with robustness | "at least 10% with moderate robustness, and at least 1% with high robustness" |
| Table of explicit probabilities | Per-species probabilities of consciousness — **plus** caveats that they're "hard to justify and may be unstable" |
| Confidence interval | "my own 70% confidence interval for years to HLMI is something like 10–120 years, though that estimate is unstable and uncertain" |
| Bare verbal, deliberately | "seems likely" — meaning >50%, while signalling he hasn't investigated in detail |
| Weakest verbal | "plausibly the most common" — a rough impression after some reading, not worth 1–3 more hours |
| Hedged takeaway | "seems to be" — flagging uncertainty about a *major* takeaway because the study was quick and shallow |
| Colloquial in text, precise in footnote | "I think this is a fairly complete list" → footnote: "I'm 70% confident there are fewer than 5 [systematic reviews] on this topic that I did not find…" |
| Model output | Roodman: "raised my best estimate… from 0.33% to 0.70% per decade… expanded my 95% confidence interval from 0.0–4.0% to 0.0–11.6%" |

**The pattern worth copying:** match the precision of your confidence statement to how
central the claim is. Central claims get numbers. Peripheral ones get "seems likely" — and
that phrasing *itself* signals you didn't investigate deeply, which is the honest thing.

## Kinds of support — the part I'd missed entirely, and the most useful part

This is a taxonomy for saying *what kind of thing* your belief rests on. Reproduced in
full, because it's the most directly transferable item in the document:

- another detailed analysis you wrote
- careful examination of one or more studies you feel qualified to assess
- careful examination of one or more studies you feel only weakly able to assess
- shallow skimming of studies you feel qualified to assess
- shallow skimming of studies you feel only weakly able to assess
- verifiable facts you can easily provide sources for
- verifiable facts you can't easily provide sources for
- expert opinion you feel comfortable assessing
- expert opinion you can't easily assess
- a vague impression from reading various sources or talking to various experts
- a general intuition about how the world works
- a simple argument that seems robust to you
- a simple argument that seems questionable to you
- a complex argument that nevertheless seems strong to you
- a complex argument that seems questionable to you
- the claim seems to follow logically from other supported claims plus background knowledge
- a source you can't remember, except that you remember thinking it trustworthy at the time
- a combination of any of the above

His worked phrasings for signalling these cheaply:

- **"Supposedly (I haven't checked)…"** — explicitly called out as good practice that
  "would rarely be found in e.g. a scientific paper."
- **"It is widely believed, and seems likely, that…"** — signals belief-because-widely-held,
  not because-I-reviewed-the-literature.
- **Admitting no basis at all:** "these numbers are just pulled from vague memories of
  conversations I've had… my estimates could easily be off by a large factor, and maybe
  even an order of magnitude."
- **Admitting you can't summarise your reasoning:** "Our reasoning behind this judgment
  cannot be easily summarized, and is based on reading about the problem and having many
  informal conversations."
- **Disclosing your priors before the investigation:** "keep in mind that I began this
  investigation as a physicalist functionalist illusionist…" — with the explicit note that
  he may be "roughly just as subject to confirmation bias as nearly all people."

## Summarising your research process

He says outright: *"Often, a good way to be transparent about the kind of support you think
you have for a claim is to summarize the research process that led to the conclusion."*
Examples:

- **"I spent less than one hour on this rapid review.** Given this limitation, I looked
  only for systematic reviews released by the Cochrane Collaboration… I also conducted a few
  Google Scholar keyword searches to see whether I could find compelling articles
  challenging the Cochrane reviews' conclusions, but I did not quickly find any."
- "I did not conduct any literature searches to produce this report. I have been following
  the small field… closely since 2011, and I felt comfortable that I already knew where to
  find most of the best recent work."
- On how a table of judgments was actually produced: "I did **not** decide on some
  particular combination rule… and then compute a resulting probability. Instead, I used my
  intuitions to generate my probabilities, then reflected on what factors seemed to be
  affecting my intuitive probabilities, and then filled out this table."

That last one is the model for your Section 6: **say how you actually arrived at your
judgments, including when the honest answer is "intuition, then rationalised."**

## Secondary recommendations

- **Provide quotes and page numbers when possible** — "even better if you can directly
  quote the most relevant passage, so the reader doesn't need to track down the source."
- **Provide data and code when possible.**
- **Provide archived copies of sources**, since links break.
- **Provide transcripts or summaries of conversations** with domain experts when possible —
  acknowledging this is often too costly, or the expert will only speak anonymously.

## What this means for the 100 minutes

The three top recommendations map onto the exam almost directly. The rest needs translating,
because you have no sources to cite and no data to publish. The transferable core:

1. **Summary first**, with the key takeaways stated as takeaways.
2. **Say which considerations are carrying your conclusion.** Not just what you believe —
   what it rests on, and which single fact would flip it.
3. **Confidence on major claims, precision proportional to centrality.** Numbers on the
   crux, "seems likely" on the periphery — and let the weak phrasing do the work of
   signalling you didn't dig.
4. **Name the kind of support.** In an exam this is: *stated in the scenario* / *my
   inference from two facts* / *my assumption* / *my intuition, unchecked*. That is the
   "kinds of support" taxonomy compressed to what your situation offers.
5. **Summarise your process.** "I spent roughly fifteen minutes on X and did not look at Y"
   is exactly the move, and it costs one sentence.
6. **Disclose your priors** where they'd affect how the reader reads you — including, if
   true, that you found one hypothesis attractive before you had evidence for it.
7. **Say what could change your mind** about each key takeaway. This is on his list of what
   readers want and it is the cheapest high-value sentence available to you.

Quote the scenario's specific details where you rely on them. That's the exam-room version
of "provide quotes and page numbers."
