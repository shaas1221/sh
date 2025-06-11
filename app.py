from flask import Flask, render_template, request
import json
import random
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # يمكنك تغييره لأي نص تشاء

# دالة لاستخراج الكلمات من العبارة مع تجاهل الفواصل وعلامات الترقيم
def split_words(phrase):
    return re.findall(r'[\u0600-\u06FF\w]+', phrase)

# تحميل الجمل
with open('sentences.json', 'r', encoding='utf-8') as f:
    sentences = json.load(f)

@app.route('/')
def index():
    sentence = random.choice(sentences)
    reference = sentence['reference']
    words = split_words(sentence['phrase'])
    random.shuffle(words)
    return render_template('index.html',
                           reference=reference,
                           words=words)

@app.route('/check', methods=['POST'])
def check():
    reference = request.form['reference']
    raw = request.form.get('selected', '')
    selected = raw.split()
    answer = ' '.join(selected)

    correct = next(s['phrase'] for s in sentences if s['reference'] == reference)
    correct_clean = ' '.join(split_words(correct))

    is_correct = (answer == correct_clean)

    return render_template('result.html',
                           reference=reference,
                           answer=answer,
                           correct=correct_clean,
                           is_correct=is_correct)

if __name__ == '__main__':
    app.run(debug=True)
