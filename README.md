# YouTube Recipe Parser

A command-line Python tool that extracts and reformats recipes from YouTube cooking video transcripts using LLMs. It fetches the video transcript, constructs a prompt with detailed formatting instructions, queries an LLM via LiteLLM, and outputs a UK-friendly markdown recipe.

Apart from converting weights and measures in the recipe to UK ones, it will also make suggestions for replacement ingredients if they are not commonly found in the UK.  It will also try and localise ingredient names (eg, 'cilantro' -> 'corriander').

## Installation

Ensure Python 3.8+ and [uv](https://docs.astral.sh/uv/) are installed.

Clone the repository:

```bash
git clone https://github.com/ohnotnow/yt-recipe-to-uk.git
cd yt-recipe-to-uk
```

Install dependencies:

```bash
uv sync
```

## Usage

```bash
uv run main.py <YOUTUBE_URL> [--prompt-file PROMPT] [--model MODEL] [--output-file FILE]
```

### Arguments

- `<YOUTUBE_URL>`: The full YouTube video URL (must include `watch?v=` or be a short `youtu.be` link)

### Options

- `--prompt-file`: Custom prompt template filename (default: `prompt.md`)
- `--model`: LLM model via LiteLLM (default: `openai/o3-mini`)
- `--output-file`: Optional name for the markdown output (default: auto-generated)

### Example

```bash
uv run main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

This will:
- Fetch and parse the transcript
- Format a recipe using the template
- Call the LLM
- Output and save the markdown recipe to `recipes/<recipe-name>-<timestamp>.md`

## Prompt Template
The prompt in `prompt.md` defines the formatting and conversion rules. It is designed to convert any English transcript into a well-structured UK-style markdown recipe.

## Environment Variables
You should set an API key for the API provider you are using.  Eg,
```bash
export OPENAI_API_KEY=...
export ANYROUTER_API_KEY=...
```

## License

This project is licensed under the MIT License.
