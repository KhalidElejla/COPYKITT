from openai import OpenAI
import argparse

client = OpenAI()
MAX_INPUT_LENGTH = 32


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i" , type=str , required=True )
    args= parser.parse_args()
    user_input= args.input
    
    if validate_length(user_input):
      branding_snippet=generate_branding_snippet(user_input)
      keywords=generate_keywords(user_input)
    else:
       raise ValueError(F"input length is too long, it sould be equal or less than {MAX_INPUT_LENGTH}")

def validate_length(prompt : str) -> bool:
  return len(prompt)<=MAX_INPUT_LENGTH

def generate_branding_snippet(prompt: str) -> str:
  enriched_prompt= f"Generate upbeat branding snippet for {prompt}"
  print (f"Generate upbeat branding snippet for {prompt}:")
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125"	,
    messages=[
      # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": enriched_prompt}
    ],
    max_tokens=32
  )

  branding_text=completion.choices[0].message.content
  branding_text_without_quotes = branding_text.strip('"')

  # check if the sentence is completed or not
  is_sentence_completed= True if branding_text_without_quotes[-1] in [".","?", "!"] else False
  if not is_sentence_completed:
    branding_text +="..."
  
  print(f"branding_snippet: {branding_text}")
  return branding_text

def generate_keywords(prompt: str) -> list[str]:
  enriched_prompt= f"Generate related branding keywords for {prompt} as a comma seperated values"
  print (f"Generate related branding keywords for {prompt}:")
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125"	,
    messages=[
      # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": enriched_prompt}
    ],
    max_tokens=10
  )

  keywords=completion.choices[0].message.content
  lowercase_keywords= keywords.lower()
  lowercase_keywords_list= lowercase_keywords.split(",")
  print(f"keywords: {lowercase_keywords_list}")
  return lowercase_keywords_list


if __name__ == "__main__":
    main()