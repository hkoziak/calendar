from flask import Flask, url_for
app = Flask(__name__)

content_section = "@content"

# @app.route("/")
# def hello():
#     return read_file("Example.html")

# somefunc = app.route("/")
# hello = somefunc(hello)
@app.route("/seller")
def seller():
    return process_template("seller.frg")

@app.route("/client")
def client():
    return process_template("client.frg")

@app.route("/task")
def task():
    return process_template("task.frg")

def read_file(file_path):
    f = open(file_path, "r")
    content = f.read()
    f.close()
    return content

def find_word_position(word, line):
    line_position = 0
    line_length = len(line)
    word_length = len(word)
    while line_position <= (line_length - word_length):
        found = True
        word_position = 0
        for letter in word:
            if letter == line[line_position + word_position]:
                word_position += 1
            else:
                found = False
                break
        if found == True:
            return line_position
        line_position += 1
    return -1

def process_template(content_fragment):
    global content_section
    template = read_file("/home/galya/myweb/templates/main.tmpl")
    position = find_word_position(content_section, template)
    if position == -1:
        return "Error happened with finding content section"
    result = ""
    for i in range(position):
        result += template[i]
    insert_table = read_file("/home/galya/myweb/templates/" + content_fragment)
    result += insert_table
    for i in range((position + len(content_section)), len(template)):
        result += template[i]
    return result
