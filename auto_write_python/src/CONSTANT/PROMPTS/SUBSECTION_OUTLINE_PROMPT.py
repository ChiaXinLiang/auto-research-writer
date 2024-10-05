SUBSECTION_OUTLINE_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall survey about [TOPIC].\n\
You have created a overall outline below:\n\
---
[OVERALL OUTLINE]
---
The outline contains a title and several sections.\n\
Each section follows with a brief sentence to describe what to write in this section.\n\n\
<instruction>
You need to enrich the section [SECTION NAME].
The description of [SECTION NAME]: [SECTION DESCRIPTION]
You need to generate the framwork containing several subsections based on the overall outlines.\n\
Each subsection follows with a brief sentence to describe what to write in this subsection.
These papers provided for references:
---
[PAPER LIST]
---
Return the outline in the format:
<format>
Subsection 1: [NAME OF SUBSECTION 1]
Description 1: [DESCRIPTION OF SUBSENTCTION 1]

Subsection 2: [NAME OF SUBSECTION 2]
Description 2: [DESCRIPTION OF SUBSENTCTION 2]

...

Subsection K: [NAME OF SUBSECTION K]
Description K: [DESCRIPTION OF SUBSENTCTION K]
</format>
</instruction>
Only return the outline without any other informations:
'''
