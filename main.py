from datetime import datetime
from typing import Optional, Tuple
import os
from litellm import completion
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from youtube_transcript_api import YouTubeTranscriptApi

project_path = os.path.abspath(os.path.dirname(__file__))

def get_prompt(recipe_text: str, prompt_filename: str = 'prompt.md') -> str:
    env = Environment(loader=FileSystemLoader(project_path), autoescape=select_autoescape())
    template = env.get_template(prompt_filename)
    return template.render(recipe_text=recipe_text)

def get_text_from_youtube(url: str) -> str:
    video_id = url.split('watch?v=')[-1]
    text = ""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        for i in transcript:
            text += i.text + " "
    except Exception as e:
        print(f"Could not get transcript for {url}")
        print(f"Error: {e}")
        exit(1)

    return text

def strip_markdown(text: str) -> str:
    return text.replace("```markdown", "").replace("```", "").strip()

def get_recipe_from_llm(prompt: str, model: str = "openai/gpt-4o-mini") -> Tuple[str, float]:
    response = completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model=model,
    )

    recipe = strip_markdown(response.choices[0].message.content)
    cost = response._hidden_params.get("response_cost", 0.0)
    return recipe, cost

def main(url: str, prompt_file: str = "prompt.md", model: str = "openai/gpt-4o-mini", output_file: Optional[str] = None) -> None:
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/"):
        text = get_text_from_youtube(url)
    else:
        print(f"Invalid URL: {url}")
        exit(1)
    prompt = get_prompt(text, prompt_file)
    recipe, cost = get_recipe_from_llm(prompt, model)
    print(recipe)
    print(f"\n\n- Cost: {cost}")
    if not output_file:
        today_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        recipe_name = recipe.split("\n")[0].lower().replace('#', '').strip().replace(" ", "-").strip()
        if not recipe_name:
            recipe_name = "recipe"
        output_file = f"{recipe_name}-{today_string}.md"
    os.makedirs(f"{project_path}/recipes", exist_ok=True)
    with open(f"{project_path}/recipes/{output_file}", "w") as f:
        f.write(recipe)
    print(f"Recipe saved to {project_path}/recipes/{output_file}")

if __name__ == '__main__':
    today_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    parser = argparse.ArgumentParser(description='Process some URL.')
    parser.add_argument('url', type=str, help='The URL to process')
    parser.add_argument('--prompt-file', type=str, default="prompt.md", help='The prompt file to use')
    parser.add_argument('--model', type=str, default="openai/o3-mini", help='The litellm provider/model to use')
    parser.add_argument('--output-file', type=str, required=False, help='The output file to write the recipe to (default is based on the recipe name)')
    args = parser.parse_args()
    main(args.url, args.prompt_file, args.model, args.output_file)
