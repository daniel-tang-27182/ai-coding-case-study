import argparse
import json
import os
import random
import re
from datetime import datetime
import traceback
from multiprocessing.dummy import Pool as ThreadPool
from generate_puzzle import generate_puzzle
from typing import Dict, Optional, List
from openai import OpenAI

def test_models_until_success():
    parser = argparse.ArgumentParser(description='Execute test runs for logic puzzles')
    parser.add_argument('-m', '--max-attempts', type=int, default=5)
    parser.add_argument('-d', '--dry-run', type=bool, default=False)
    args = parser.parse_args()
    
    model_chunks = [
        #['moonshotai/kimi-k2-thinking', 'moonshotai/kimi-k2-0905'],
        #['google/gemini-3-flash-preview', 'deepseek/deepseek-v3.2'],
        #['anthropic/claude-haiku-4.5'],
        #['anthropic/claude-sonnet-4.5'],
    ]

    all_models = [
        'moonshotai/kimi-k2.5',
    ]
    
    people = range(2,18)
    attrs = range(1,18)
    
    all_params = [
        (model, num_people, num_attrs) 
            for model in all_models
            for num_people in people 
            for num_attrs in attrs
    ]

    puzzle_params = all_params
    print("TEST RUN PUZZLE PARAMS:")
    print(json.dumps(puzzle_params))
    random.shuffle(puzzle_params)

    if not args.dry_run:
        run_tests_until_success_parallel(puzzle_params, args.max_attempts)

def run_tests_until_success_parallel(test_params: list[(str, int, int)], max_attempts: int):
    with ThreadPool(processes=300) as pool:
        # starmap will surface exceptions
        pool.starmap(
            test_puzzle_until_success, 
            [(model, num_people, num_attributes, max_attempts) for (model, num_people, num_attributes) in test_params]
        )

def test_puzzle_until_success(model, num_people, num_attributes, max_attempts):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_TOKEN"),
    )
    if model.startswith('gpt'):
        print(f"Using OpenAI API key for model: {model}")
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    attempts = 0
    while attempts < max_attempts:
        success = test_puzzle(client, model, num_people, num_attributes)
        if success:
            print(f"SUCCESS: model = {model}, num_people = {num_people}, num_attributes = {num_attributes}")
            break
        print(f"FAILED: model = {model}, num_people = {num_people}, num_attributes = {num_attributes}, attempt = {attempts}")
        attempts += 1

def test_models():
    parser = argparse.ArgumentParser(description='Execute test runs for logic puzzles')
    parser.add_argument('-s', '--sample-size', type=int, default=1)
    parser.add_argument('-d', '--dry-run', type=bool, default=False)
    args = parser.parse_args()
    
    model_chunks = [
        #['moonshotai/kimi-k2-thinking', 'moonshotai/kimi-k2-0905'],
        ['google/gemini-3-flash-preview', 'deepseek/deepseek-v3.2'],
        ['anthropic/claude-haiku-4.5', 'google/gemini-3-pro-preview'],
        ['anthropic/claude-opus-4.5', 'anthropic/claude-sonnet-4.5'],
    ]

    all_models = [
        'google/gemini-3-flash-preview',
        'anthropic/claude-sonnet-4.5',
        'anthropic/claude-haiku-4.5',
    ]
    
    people = range(9,18)
    attrs = range(9,18)
    
    all_params = [
        (model, num_people, num_attrs) 
            for model in all_models
            for num_people in people 
            for num_attrs in attrs
    ]

    puzzle_params = all_params * args.sample_size
    print("TEST RUN PUZZLE PARAMS:")
    print(json.dumps(puzzle_params))
    random.shuffle(puzzle_params)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_TOKEN"),
    )

    if not args.dry_run:
        run_tests_parallel(client, puzzle_params)

def test_single_model():
    parser = argparse.ArgumentParser(description='Execute test runs for logic puzzles')
    parser.add_argument('-s', '--sample-size', type=int, default=1)
    parser.add_argument('-m', '--model', type=str, default='google/gemma-3-27b-it:free')
    parser.add_argument('-d', '--dry-run', type=bool, default=False)
    args = parser.parse_args()

    all_params = [
        (args.model, num_people, num_attrs) 
        for num_people in range(10, 12) 
        for num_attrs in range(12, 13)
    ]

    puzzle_params = all_params * args.sample_size
    print("TEST RUN PUZZLE PARAMS:")
    print(json.dumps(puzzle_params))
    random.shuffle(puzzle_params)
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_TOKEN"),
    )
    if args.model.startswith('gpt'):
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    if not args.dry_run:
        run_tests_parallel(client, puzzle_params)

def run_tests_parallel(client, test_params: list[(str, int, int)]):
    with ThreadPool(processes=300) as pool:
        # starmap will surface exceptions
        pool.starmap(
            test_puzzle, 
            [(client, model, num_people, num_attributes) for (model, num_people, num_attributes) in test_params]
        )

# Returns True if the puzzle is solved correctly, False otherwise
def test_puzzle(client, model, num_people, num_attributes) -> bool:
    # Sanitize model name for directory/filename use
    sanitized_model_name = re.sub(r'[:/\\?*\"<>|]', '_', model)
    
    # Create model-specific output directory
    outputs_dir = f"outputs/{sanitized_model_name}"
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{outputs_dir}/puzzle_{num_people}_{num_attributes}_{sanitized_model_name}_{timestamp}.txt"

    try:
        # Record input parameters 
        with open(filename, 'a') as f:
            f.write(f"<num_people>{num_people}</num_people>\n")
            f.write(f"<num_attributes>{num_attributes}</num_attributes>\n\n")

        # Generate puzzle and record prompt and expected solution
        puzzle = generate_puzzle(num_people=num_people, num_attributes=num_attributes)
        puzzle_prompt = puzzle.getPuzzlePrompt()
        with open(filename, 'a') as f:
            f.write("<puzzle_prompt>\n")
            f.write(puzzle_prompt)
            f.write("\n</puzzle_prompt>\n\n")

            f.write("<puzzle_solution>\n")
            f.write(json.dumps(puzzle.solution, indent=2))
            f.write("\n</puzzle_solution>\n\n")

        # Ask llm for puzzle solution and record solution
        response = client.responses.create(
            model=model,
            reasoning={ "effort": "medium" },
            instructions="You are a helpful assistant that solves logic grid puzzles. No puzzle is too difficult for you to solve. You will always provide a solution to the puzzle. " + \
                        "Don't write a program to solve the puzzle and don't use multiple messages. Always provide the final JSON solution in one message, " + \
                        "even if the answer is very likely to be incorrect. Do not include anything else besides the final JSON solution in the output.",
            input=f"Please solve this logic puzzle:\n\n{puzzle_prompt}"
        )
        # Extract content from responses format
        response_content = response.output_text

        with open(filename, 'a') as f:
            f.write("<llm_response>\n")
            f.write(response_content)
            f.write("\n</llm_response>\n\n")

        with open(filename, 'a') as f:
            f.write("<full_llm_response>\n")
            f.write(json.dumps(response.model_dump(), indent=2))
            f.write("\n</full_llm_response>\n\n")

        # Parse solution and check if it matches expected solution 
        parsed_solution = parse_llm_response(response_content)
        success = parsed_solution == puzzle.solution
        with open(filename, 'a') as f:
            f.write("<response_correct>\n")
            f.write(str(success))
            f.write("\n</response_correct>\n\n")
        return success
    except Exception:
        print(f"FAILED RUN: num_people = {num_people}, num_attributes = {num_attributes}")
        print(traceback.format_exc())
        with open(filename, 'a') as f:
            f.write("<exception>\n")
            f.write(traceback.format_exc())
            f.write("</exception>\n")
        return False

def parse_llm_response(content: str) -> list[Dict[str, str]]:
    solution_match = re.search(r'<solution>(.*?)</solution>', content, re.DOTALL)
    if solution_match:
        json_content = solution_match.group(1).strip()
    else:
        raise ValueError("Invalid response. <solution></solution> tags not found")
    
    try:
        parsed = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    
    if not isinstance(parsed, list):
        raise ValueError(f"Expected a JSON array, got {type(parsed).__name__}")
    
    # Validate that each element is a dictionary
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            raise ValueError(f"Element at index {i} is not a dictionary, got {type(item).__name__}")
    
    return parsed

if __name__ == "__main__":
    #test_single_model()
    #test_models()
    test_models_until_success()