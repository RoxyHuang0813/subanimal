from flask import Flask, render_template, request, session, redirect, url_for, make_response

import random
from waitress import serve

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


# 定義每種動物類型的隨機語錄
ANIMAL_QUOTES = {
    'squirrel': [
        "我存錢不是為了給你花的耶！",
        "我的存款比你的八卦還多！",
        "折扣再低，也比不上存款帶來的安全感！",
        "存錢才是快樂的來源，花錢只會讓我焦慮！",
        "你買快樂，我買未來！"
    ],
    'cheetah': [
        "我很大方，但不代表你可以佔我便宜！",
        "人生苦短，買了再說！",
        "沒花掉的錢，等於沒存在過！",
        "有賺有花，才是真正的享受人生！",
        "等我存夠錢？那機會早就溜走啦！"
    ],
    'owl': [
        "數據才是我的真愛，衝動？不存在的！",
        "沒有完美的計劃，我怎麼可能出手？",
        "沒有Excel，我怎麼知道這筆錢值不值得花？",
        "別人怕沒錢，我怕沒資訊！",
        "理財不是感覺，而是邏輯！"
    ],
    'raccoon': [
        "大家說好才是真的好，獨樂樂不如眾樂樂！",
        "朋友的推薦，比黃金還珍貴！",
        "沒有你陪，這錢花起來就沒靈魂！",
        "團購99折？我立刻揪團！",
        "比省錢更重要的，是一起花錢的快樂！"
    ],
    'wolf': [
        "帶領團隊衝鋒陷陣，財富自然滾滾來！",
        "我的策略，就是讓錢為我工作！",
        "沒有資源？整合起來就有了！",
        "投資不只是錢，還有關係、資訊和時機！",
        "財富不是偶然，是精心佈局的結果！"
    ],
    'peacock': [
        "品味，就是我的最佳投資！",
        "生活要有儀式感，錢包也要跟上！",
        "窮得只剩錢？我可不想這樣！",
        "錢不是問題，問題是怎麼花得漂亮！",
        "別問我為什麼買，因為值得！"
    ]
}


# 定義每種動物對應的大K老師對話
TEACHER_DIALOGUES = {
    'squirrel': '你是謹慎的松鼠型！喜歡儲備資源，適合穩健的理財方式。',
    'cheetah': '你是敏捷的獵豹型！喜歡快速行動，適合高風險高報酬的投資。',
    'owl': '你是智慧的貓頭鷹型！喜歡分析數據，適合長期投資策略。',
    'raccoon': '你是靈活的浣熊型！喜歡與人合作，適合團隊投資或合夥創業。',
    'wolf': '你是領導的狼型！喜歡掌控全局，適合創業或管理大型專案。',
    'peacock': '你是耀眼的孔雀型！喜歡展現自我，適合品牌經營或創意產業。'
}


# 定義每種動物類型的故事
ANIMAL_STORIES = {
    'squirrel': '''
        松鼠型的人天生就是儲蓄高手！你總是未雨綢繆，喜歡為未來做準備。
        你的理財風格穩健，偏好低風險的投資工具，例如定存或債券。
        雖然有時會被認為過於保守，但你的謹慎讓你在經濟波動中屹立不搖。
        建議你偶爾嘗試一些中等風險的投資，讓財富增長更有彈性！
    ''',
    'cheetah': '''
        獵豹型的人行動迅速，喜歡追求高報酬！你總是能抓住機會，快速做出決策。
        你的理財風格偏向高風險高報酬，例如股票或加密貨幣。
        雖然你的衝勁十足，但要注意避免過度冒險，適時停損才能長久獲利。
        建議你學習更多風險管理技巧，讓投資更穩健！
    ''',
    'owl': '''
        貓頭鷹型的人理性且善於分析！你總是透過數據和邏輯來做出決策。
        你的理財風格偏向長期投資，例如指數基金或房地產。
        雖然你的策略穩健，但要注意避免過度分析而錯失機會。
        建議你偶爾相信直覺，讓投資更有彈性！
    ''',
    'raccoon': '''
        浣熊型的人喜歡與人合作，善於利用人脈資源！你總是能透過團隊達成目標。
        你的理財風格偏向合夥投資或創業，例如共同基金或合夥事業。
        雖然你的人際關係是你的優勢，但要注意避免過度依賴他人。
        建議你培養獨立判斷能力，讓投資更自主！
    ''',
    'wolf': '''
        狼型的人天生就是領導者！你善於整合資源，帶領團隊達成目標。
        你的理財風格偏向創業或大型專案，例如創投或企業併購。
        雖然你的領導能力強，但要注意避免過度擴張。
        建議你學習更多風險控制技巧，讓事業更穩健！
    ''',
    'peacock': '''
        孔雀型的人喜歡展現自我，追求獨特與品味！你總是能吸引眾人的目光。
        你的理財風格偏向品牌經營或創意產業，例如時尚或藝術投資。
        雖然你的品味獨特，但要注意避免過度消費。
        建議你學習更多理財規劃技巧，讓財富更持久！
    '''
}

# 新增故事頁面路由
@app.route('/story/<animal>')
def story(animal):
    story_content = ANIMAL_STORIES.get(animal, '沒有找到該動物的故事。')
    return render_template('story.html', story_content=story_content, animal_name=ANIMALS.get(animal, '未知動物'))



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
        return redirect(url_for('index'))

    counts = {}
    for animal in session['answers']:
        counts[animal] = counts.get(animal, 0) + 1
    result_type = max(counts, key=lambda k: counts[k])



    teacher_dialogue = TEACHER_DIALOGUES.get(result_type, '恭喜你完成測驗！快把專屬你的財富性格分享給朋友吧！')
    random_quote = random.choice(ANIMAL_QUOTES.get(result_type, ["歡迎來到潛意識財富森林！"]))


    response = make_response(render_template(
        'result.html',
        animal=result_type,
        animal_name=ANIMALS[result_type],

        teacher_dialogue=teacher_dialogue,
        random_quote=random_quote

    ))
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
