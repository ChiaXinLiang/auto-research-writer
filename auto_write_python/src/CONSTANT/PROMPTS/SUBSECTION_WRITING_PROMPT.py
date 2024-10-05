SUBSECTION_WRITING_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall and comprehensive survey about [TOPIC].\n\
You have created a overall outline below:\n\
---
[OVERALL OUTLINE]
---
Below are a list of papers for references:
---
[PAPER LIST]
---

<instruction>
Now you need to write the content for the subsection:
"[SUBSECTION NAME]" under the section: "[SECTION NAME]"
The details of what to write in this subsection called [SUBSECTION NAME] is in this descripition:
---
[DESCRIPTION]
---

Here is the requirement you must follow:
1. The content you write must be more than [WORD NUM] words.
2. When writing sentences that are based on specific papers above, you cite the "paper_title" in a '[]' format to support your content. An example of citation: 'the emergence of large language models (LLMs) [Language models are few-shot learners; PaLM: Scaling language modeling with pathways]'
    Note that the "paper_title" is not allowed to appear without a '[]' format. Once you mention the 'paper_title', it must be included in '[]'. Papers not existing above are not allowed to cite!!!
    Remember that you can only cite the paper provided above and only cite the "paper_title"!!!
3. Only when the main part of the paper support your claims, you cite it.


Here's a concise guideline for when to cite papers in a survey:
---
1. Summarizing Research: Cite sources when summarizing the existing literature.
2. Using Specific Concepts or Data: Provide citations when discussing specific theories, models, or data.
3. Comparing Findings: Cite relevant studies when comparing or contrasting different findings.
4. Highlighting Research Gaps: Cite previous research when pointing out gaps your survey addresses.
5. Using Established Methods: Cite the creators of methodologies you employ in your survey.
6. Supporting Arguments: Cite sources that back up your conclusions and arguments.
7. Suggesting Future Research: Reference studies related to proposed future research directions.
---

</instruction>
Return the content of subsection "[SUBSECTION NAME]" in the format:
<format>
[CONTENT OF SUBSECTION]
</format>
Only return the content more than [WORD NUM] words you write for the subsection [SUBSECTION NAME] without any other information:
'''
