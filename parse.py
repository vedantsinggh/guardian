#TODO: notes taking ability
#TODO: make standalone installable application

import requests
import subprocess
import sys
import os

question_name = sys.argv[1]
url = "https://alfa-leetcode-api.onrender.com/select/raw?titleSlug=" + question_name

try:
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    if data["question"] is None or data is None:
        print("Cant find the specified question!")
        exit(-1)

    default_includes = "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n"
    question = data["question"]["content"]
    testcases = data["question"]["exampleTestcases"]
    #question.replace("\n", " \n ")

    code = data["question"]["codeSnippets"][0]["code"]
    topic = data["question"]["topicTags"][0]["slug"]
    main_function = """\n\nint main(){
/*
Example testcases
"""
    end_function = """
*/

    Solution solution;
    cout << \"Output: \\n\";
    cout << solution.<enter function name>() << \"\\n\";
}
    """

    if not os.path.exists(topic):
        os.mkdir(topic)

    if not os.path.exists(topic + "/" + question_name):
        os.mkdir(topic + "/" + question_name)

    file_name = "./" + topic + "/" + question_name + "/" + question_name
    with open(file_name + ".cpp", "w") as file:
        file.write(default_includes)
        file.write("\n")
        file.write(code)
        file.write(main_function)
        file.write(testcases)
        file.write(end_function)

    with open("./" + topic + "/" + question_name + "/notes.html", "w") as file:
        file.write(question)

    subprocess.run(["vim", file_name + ".cpp"])

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON from the response.")

