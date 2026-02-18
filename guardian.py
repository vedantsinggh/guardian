#TODO: notes taking ability
#TODO: make standalone installable application
#TODO: question list and seach
#TODO: daily problems

import requests
import subprocess
import sys
import os

is_daily = False
question_name = sys.argv[1]
if question_name == "daily": is_daily = True
url = "https://alfa-leetcode-api.onrender.com/select/raw?titleSlug=" + question_name

try:
    if is_daily:
        url = "https://alfa-leetcode-api.onrender.com/daily/raw"

    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    if is_daily:
        question_name = data["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]
    elif data["question"] is None or data is None:
        print("Cant find the specified question!")
        exit(-1)

    default_includes = "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n"

    question = None
    testcases = None
    code = None
    topic = None
    if is_daily:
        question = data["activeDailyCodingChallengeQuestion"]["question"]["content"]
        testcases = data["activeDailyCodingChallengeQuestion"]["question"]["exampleTestcases"]
        code = data["activeDailyCodingChallengeQuestion"]["question"]["codeSnippets"][0]["code"]
        topic = data["activeDailyCodingChallengeQuestion"]["question"]["topicTags"][0]["slug"]

    else:
        question = data["question"]["content"]
        testcases = data["question"]["exampleTestcases"]
        code = data["question"]["codeSnippets"][0]["code"]
        topic = data["question"]["topicTags"][0]["slug"]
    #question.replace("\n", " \n ")

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

