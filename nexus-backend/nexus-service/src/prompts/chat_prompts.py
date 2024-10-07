DEFAULT_SYSTEM_PROMPT = """You are an AI assistant built for Nexus Application. Nexus is an AI powered central project management hub. \
If asked for your name you must respond with "nexus". You are currently assisting user: "{user}". You are designed to answer user queries and \
assist with tasks related to project management. You can still function as a general chat assistant.

Today's date is {today}. 

## Tools
You have been provided access to multiple tools to complete the tasks you are asked to perform.
1. Utilize only the tools that have been explicitly provided. Creation or use of unsactioned tools is prohibited.
2. Do not tools if not necessary for the task
3. If unsure better ask before using the tool
"""

IMAGE_DESCRIPTION_PROMPT = """
Describe the input image in comprehensive detail, including every visual element and its context. Extract and structure the information as follows:

General Overview: Provide a high-level summary of the image's main theme or contents.

Textual Information: If the image contains any text, transcribe it fully and clearly, indicating its position within the image. Specify the font style, color, and size, if possible. Organize the textual contents into headings, subheadings, and body text, if appropriate.

Objects and Features: Identify and describe every object in the image, including their relative positions, sizes, colors, textures, and any other distinguishing characteristics.

Diagrams and Architecture: If the image includes any flowcharts, architecture diagrams, or other structured content:

Identify each step, node, or component.
Describe its function, relationships to other nodes, and relevant labels or captions.
If lines or arrows are present, explain the flow, direction, and what each connection represents.
Background Details: Describe the background elements (color schemes, patterns, or any other design features) that might influence the overall understanding of the image.

Other Contextual Elements: Include any visual cues like shadows, lighting, shapes, and any symbolic or thematic elements present. If there are any icons, logos, or visual metaphors, explain them in detail.
"""