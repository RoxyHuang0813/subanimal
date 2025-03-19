from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secure_key_123'  # 正式環境請用更複雜的金鑰

ANIMALS = {
    'squirrel': '松鼠型',
    'cheetah': '獵豹型',
    'owl': '貓頭鷹型',
    'raccoon': '浣熊型',
    'wolf': '狼型',
    'peacock': '孔雀型'
}

QUESTIONS = [
    {
        'question': '看到限量商品，你的第一反應是？',
        'options': [
            {'text': '先查CP值', 'type': 'owl'},
            {'text': '立刻搶購', 'type': 'cheetah'},
            {'text': '找朋友一起買', 'type': 'raccoon'},
            {'text': '猶豫後放棄', 'type': 'squirrel'},
            {'text': '評估能否轉售獲利', 'type': 'wolf'},
            {'text': '只要夠獨特就買', 'type': 'peacock'}
        ]
    },
    {
        'question': '突然獲得10萬元，你會？',
        'options': [
            {'text': '存起來', 'type': 'squirrel'},
            {'text': '投資高風險標的', 'type': 'cheetah'},
            {'text': '請客建立人脈', 'type': 'raccoon'},
            {'text': '分散投資組合', 'type': 'owl'},
            {'text': '投入團隊專案', 'type': 'wolf'},
            {'text': '升級衣櫥或3C', 'type': 'peacock'}
        ]
    },
    {
        'question': '面對投資虧損，你的反應是？',
        'options': [
            {'text': '再也不碰投資', 'type': 'squirrel'},
            {'text': '加碼攤平', 'type': 'cheetah'},
            {'text': '問朋友怎麼辦', 'type': 'raccoon'},
            {'text': '檢視數據調整策略', 'type': 'owl'},
            {'text': '說服團隊共同承擔', 'type': 'wolf'},
            {'text': '轉移注意力消費', 'type': 'peacock'}
        ]
    },
    {
        'question': '選擇理財顧問時，你最重視？',
        'options': [
            {'text': '低風險保證', 'type': 'squirrel'},
            {'text': '高報酬案例', 'type': 'cheetah'},
            {'text': '朋友推薦', 'type': 'raccoon'},
            {'text': '歷史數據分析', 'type': 'owl'},
            {'text': '資源整合能力', 'type': 'wolf'},
            {'text': '顧問的個人形象', 'type': 'peacock'}
        ]
    },
    {
        'question': '朋友向你借錢，你會？',
        'options': [
            {'text': '找理由拒絕', 'type': 'squirrel'},
            {'text': '要求高利息', 'type': 'cheetah'},
            {'text': '勉強答應', 'type': 'raccoon'},
            {'text': '簽正式合約', 'type': 'owl'},
            {'text': '轉介合作機會替代', 'type': 'wolf'},
            {'text': '藉機要求人情回饋', 'type': 'peacock'}
        ]
    },
    {
        'question': '你如何定義「財務自由」？',
        'options': [
            {'text': '存款夠用一輩子', 'type': 'squirrel'},
            {'text': '隨時能買想要的', 'type': 'cheetah'},
            {'text': '和朋友一起致富', 'type': 'raccoon'},
            {'text': '被動收入>支出', 'type': 'owl'},
            {'text': '建立可傳承的事業', 'type': 'wolf'},
            {'text': '過上令人羨慕的生活', 'type': 'peacock'}
        ]
    },
    {
        'question': '當你發現同事薪水比你高，你會？',
        'options': [
            {'text': '焦慮自己存款不足', 'type': 'squirrel'},
            {'text': '立刻要求加薪', 'type': 'cheetah'},
            {'text': '私下詢問同事建議', 'type': 'raccoon'},
            {'text': '收集市場數據後談判', 'type': 'owl'},
            {'text': '規劃跳槽或創業', 'type': 'wolf'},
            {'text': '升級外在形象爭取機會', 'type': 'peacock'}
        ]
    },
    {
        'question': '你如何分配每日時間？',
        'options': [
            {'text': '嚴格按計畫執行', 'type': 'squirrel'},
            {'text': '隨興追求新鮮事', 'type': 'cheetah'},
            {'text': '配合朋友行程調整', 'type': 'raccoon'},
            {'text': '優化效率模組', 'type': 'owl'},
            {'text': '專注團隊目標', 'type': 'wolf'},
            {'text': '優先經營社交圈', 'type': 'peacock'}
        ]
    },
    {
        'question': '面對財務壓力時，你的紓壓方式是？',
        'options': [
            {'text': '反覆檢查存款數字', 'type': 'squirrel'},
            {'text': '衝動購物', 'type': 'cheetah'},
            {'text': '找朋友訴苦', 'type': 'raccoon'},
            {'text': '製作20頁分析報告', 'type': 'owl'},
            {'text': '規劃更大膽的投資', 'type': 'wolf'},
            {'text': '預約高級SPA療程', 'type': 'peacock'}
        ]
    },
    {
        'question': '學習新理財工具時，你會？',
        'options': [
            {'text': '只選保本型商品', 'type': 'squirrel'},
            {'text': '立刻小額試水溫', 'type': 'cheetah'},
            {'text': '參加社群跟單', 'type': 'raccoon'},
            {'text': '研讀30份財報', 'type': 'owl'},
            {'text': '整合既有資源應用', 'type': 'wolf'},
            {'text': '選擇形象最好的平台', 'type': 'peacock'}
        ]
    },
    {
        'question': '經濟衰退時，你的應對策略是？',
        'options': [
            {'text': '節省到極限', 'type': 'squirrel'},
            {'text': '賭一把逆勢操作', 'type': 'cheetah'},
            {'text': '加入互助團體', 'type': 'raccoon'},
            {'text': '重新計算安全邊際', 'type': 'owl'},
            {'text': '併購低價資產', 'type': 'wolf'},
            {'text': '維持高消費展現實力', 'type': 'peacock'}
        ]
    },
    {
        'question': '計畫旅行時，你優先考慮？',
        'options': [
            {'text': '最低預算方案', 'type': 'squirrel'},
            {'text': '說走就走的冒險', 'type': 'cheetah'},
            {'text': '朋友推薦的熱門景點', 'type': 'raccoon'},
            {'text': '性價比最優路線', 'type': 'owl'},
            {'text': '拓展商業人脈的行程', 'type': 'wolf'},
            {'text': '五星級打卡行程', 'type': 'peacock'}
        ]
    }
]

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'answers' not in session:
        session['answers'] = []
    
    if request.method == 'POST':
        selected_type = request.form.get('animal_type')
        session['answers'].append(selected_type)
        session.modified = True
    
    if len(session['answers']) >= len(QUESTIONS):
        return redirect('/result')
    
    current_q = QUESTIONS[len(session['answers'])]
    random.shuffle(current_q['options'])
    
    return render_template('test.html',
                         question=current_q['question'],
                         options=current_q['options'],
                         progress=len(session['answers'])+1,
                         total=len(QUESTIONS))

@app.route('/result')
def result():
    if 'answers' not in session or len(session['answers']) != len(QUESTIONS):
        return redirect('/')
    
    counts = {}
    for animal in session['answers']:
        counts[animal] = counts.get(animal, 0) + 1
    
    result_type = max(counts, key=lambda k: counts[k])
    
    return render_template('result.html',
                          animal=result_type,
                          animal_name=ANIMALS[result_type])

if __name__ == '__main__':
    app.run(debug=True)