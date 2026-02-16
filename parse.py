import requests
import subprocess
import sys

question_name = sys.argv[1]
url = "https://alfa-leetcode-api.onrender.com/select/raw?titleSlug=" + question_name

try:
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    default_includes = "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n"
    question = data["question"]["content"]
    code = data["question"]["codeSnippets"][0]["code"]

    with open(question_name + ".cpp", "w") as file:
        file.write(default_includes)
        file.write("\n")
        file.write(code)

    subprocess.run(["vim", question_name + ".cpp"])

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON from the response.")
