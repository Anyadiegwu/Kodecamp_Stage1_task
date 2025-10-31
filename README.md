A small script or function in Python that does the following:

Accepts a user prompt from input (e.g., via command line, web form, or API endpoint).
Sends this user prompt to an AI text generation API which in this case is Gemini API along with a system prompt that defines the AI’s behaviour.
 

Implements moderation checks on:

The input (to block harmful or disallowed content before sending it to the AI).
The output (to filter or flag unsafe responses before displaying them to the user).
