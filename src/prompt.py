import csv, random


def prompt(num_prompts, elements_path, templates_path):
    with open(elements_path, 'r') as f:
        elements = list(csv.DictReader(f))

    with open(templates_path, 'r') as f:
        templates = [line.strip() for line in f]

    prompts = [random.choice(templates).format(**random.choice(elements)) for _ in range(num_prompts)]
    return [prompt.replace('\t', '') for prompt in prompts]
