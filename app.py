from flask import Flask, render_template, request
import json
import random
import re

app = Flask(__name__)

# تحميل الجمل من JSON
with open('sentences.json', encoding='utf-8') as f:
    SENTENCES = json.load(f)

# دالة لتطبيع النص (إزالة الفواصل والمسافات الزائدة)
def normalize(text):
    return re.sub(r'\s+', ' ', text.replace(',', '').strip())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_answer = normalize(request.form['user_answer'])
        correct_answer = normalize(request.form.get('correct_answer', ''))
        is_correct = user_answer == correct_answer
        return render_template('result.html', correct=is_correct, correct_answer=correct_answer)

    # في حالة GET: عرض سؤال جديد
    sentence = random.choice(SENTENCES)
    reference = sentence['reference']
    phrase = sentence['phrase']
    words = phrase.split()
    random.shuffle(words)
    return render_template('index.html', reference=reference, words=words, correct_answer=phrase)

if __name__ == '__main__':
    app.run(debug=True)
