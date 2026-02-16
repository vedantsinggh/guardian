import requests

url = "https://alfa-leetcode-api.onrender.com/select/raw?titleSlug=two-sum"

try:
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    default_includes = "#include <iostream>\n#include <vector>\n#include <algorithms>\n"
    question = data["question"]["content"]
    code = data["question"]["codeSnippets"][0]["code"]

    with open("two-sum.cpp", "w") as file:
        file.write(default_includes)
        file.write("\n")
        file.write(code)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON from the response.")
