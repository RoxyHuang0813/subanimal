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
    'squirrel': '你是謹慎的松鼠型！喜歡儲備資源，適合穩健的理財方式。療癒小提示：「你的內在安全感，是否只能來自金錢？如果沒有存款，你會怎麼定義自己的價值？」催眠可以幫助你放下金錢焦慮，找到真正的內在安全感。',
    'cheetah': '你是敏捷的獵豹型！喜歡快速行動，適合高風險高報酬的投資。療癒小提示：「你的決策模式是否來自害怕錯過？這種焦慮感，可能與過去未完成的渴望有關。」催眠可以探索你的內在潛意識，培養穩定強大的內心。',
    'owl': '你是智慧的貓頭鷹型！喜歡分析數據，適合長期投資策略。療癒小提示：「你是否過度分析，以至於難以行動？這種控制欲，可能來自對犯錯的恐懼。」催眠可以協助你調整過度完美主義，學會信任自己的直覺。',
    'raccoon': '你是靈活的浣熊型！喜歡與人合作，適合團隊投資或合夥創業。療癒小提示：「你是否常常為了別人而做財務決策？你的金錢模式，是否來自想要被接納？」催眠可以幫助你建立自我價值，不再依賴外界認可。',
    'wolf': '你是領導的狼型！喜歡掌控全局，適合創業或管理大型專案。療癒小提示：「你是否把財富當作掌控人生的方式？如果不做領導者，你如何定義自己？」催眠可以讓你放下控制焦慮，讓財富流動更自由。',
    'peacock': '你是耀眼的孔雀型！喜歡展現自我，適合品牌經營或創意產業。療癒小提示：「你是否認為金錢能定義你的價值？如果沒有華麗外表時，你是否仍然感覺自己足夠好？」催眠可以協助你探索自我，讓財務選擇更加平衡。'
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

# 新增分享頁面路由
@app.route('/share')
def share():
    return render_template('share.html')

QUESTIONS = [
    {
        'question': '看到便利商店出了新的限量商品，你的第一反應是？',
        'options': [
            {'text': '還是要上網查怎樣才是C/P值最高', 'type': 'owl'},
            {'text': '只要我喜歡不用等打折，我現在就買!', 'type': 'cheetah'},
            {'text': '限量耶，好東西一定要買來跟好朋友分享', 'type': 'raccoon'},
            {'text': '說不定賣不完還會再打折，我再等等', 'type': 'squirrel'},
            {'text': '主管之前好像有提過，我先幫他買看他要不要，', 'type': 'wolf'},
            {'text': '昨天新聞有看到，好像很多人要搶，那還是買一下好了', 'type': 'peacock'}
        ]
    },
    {
        'question': '今年年終發了獎金10萬元，你會？',
        'options': [
            {'text': '先存起來，再想想要買什麼', 'type': 'squirrel'},
            {'text': '比特幣現在是低點，這筆錢買了一定翻倍', 'type': 'cheetah'},
            {'text': '我朋友說想吃教父牛排，發年終了我請他', 'type': 'raccoon'},
            {'text': '30%存起來/30%買東西/剩下40%買股票好了', 'type': 'owl'},
            {'text': '朋友想開店，要不然我拿這筆錢投資當股東好了', 'type': 'wolf'},
            {'text': '我的手機跟家裡冰箱可以換新了', 'type': 'peacock'}
        ]
    },
    {
        'question': '面對投資虧損，你的反應是？',
        'options': [
            {'text': '我以後再也不投資了', 'type': 'squirrel'},
            {'text': '應該趁低點加碼攤平才對', 'type': 'cheetah'},
            {'text': '我問一下銀行的朋友看看', 'type': 'raccoon'},
            {'text': '一定是我之前分析得不對，我再研究一下', 'type': 'owl'},
            {'text': '該賣就賣，當斷則斷', 'type': 'wolf'},
            {'text': '不想面對，先放著以後再說', 'type': 'peacock'}
        ]
    },
    {
        'question': '選擇理財商品時，你最重視？',
        'options': [
            {'text': '風險越低越好，定存我也能接受', 'type': 'squirrel'},
            {'text': '高風險高回報,賭賭看', 'type': 'cheetah'},
            {'text': '我朋友說那支會漲，可以買', 'type': 'raccoon'},
            {'text': '我先分析一下歷年的投報率再決定', 'type': 'owl'},
            {'text': '要能随時變現，像儲蓄險這種的我不買', 'type': 'wolf'},
            {'text': '投顧老師經驗豐富，我聽他的', 'type': 'peacock'}
        ]
    },
    {
        'question': '朋友向你借錢，你會？',
        'options': [
            {'text': '想辦法找理由拒絕', 'type': 'squirrel'},
            {'text': '就算親兄弟還是要算利息哦', 'type': 'cheetah'},
            {'text': '很為難，可能會勉強答應', 'type': 'raccoon'},
            {'text': '我可以借，但是一定要簽借據', 'type': 'owl'},
            {'text': '有什麼好康大家互相回饋一下也不是不行', 'type': 'wolf'},
            {'text': '態度好的求求我，我可以考慮', 'type': 'peacock'}
        ]
    },
    {
        'question': '你如何定義「財務自由」？',
        'options': [
            {'text': '我的存款夠用一輩子', 'type': 'squirrel'},
            {'text': '錢多到想要什麼就能買什麼', 'type': 'cheetah'},
            {'text': '錢只要夠用就好，家人朋友才是最重要的資產', 'type': 'raccoon'},
            {'text': '當然是被動收入>支出', 'type': 'owl'},
            {'text': '要有事業，沒有都是幫人打工哪來的自由', 'type': 'wolf'},
            {'text': '像貴婦那樣令人羨慕的生活才自由', 'type': 'peacock'}
        ]
    },
    {
        'question': '當你發現朋友的財務狀況比你好，你會？',
        'options': [
            {'text': '焦慮自己存款不足', 'type': 'squirrel'},
            {'text': '我也有機會賺大錢，不會輸他', 'type': 'cheetah'},
            {'text': '問問朋友怎麼做到的', 'type': 'raccoon'},
            {'text': '研究對方的投資策略並調整自己的計畫', 'type': 'owl'},
            {'text': '回去想想怎麼樣才能賺更多錢', 'type': 'wolf'},
            {'text': '錢就是要花在自己身上，存那麼多幹嘛', 'type': 'peacock'}
        ]
    },
    {
        'question': '你通常如何規劃一天的行程？',
        'options': [
            {'text': '每天都差不多，滿固定的', 'type': 'squirrel'},
            {'text': '不一定，看情況調整', 'type': 'cheetah'},
            {'text': '如果朋友揪我我都會去', 'type': 'raccoon'},
            {'text': '我有寫行事曆安排每一天的行程', 'type': 'owl'},
            {'text': '我的年度目標有達到就好，不會規劃到每一天', 'type': 'wolf'},
            {'text': '喜歡拓展社交圈，人多的地方都去', 'type': 'peacock'}
        ]
    },
    {
        'question': '面對財務壓力時，你的解決方式是？',
        'options': [
            {'text': '反覆計算存款還夠不夠', 'type': 'squirrel'},
            {'text': '壓力越大越愛亂買', 'type': 'cheetah'},
            {'text': '找朋友訴苦', 'type': 'raccoon'},
            {'text': '越分析越清楚，思考解決方法', 'type': 'owl'},
            {'text': '想辦法找別人合作，借力使力', 'type': 'wolf'},
            {'text': '先不管，轉移注意力', 'type': 'peacock'}
        ]
    },
    {
        'question': '當你聽到一種新的理財工具時，你的第一反應是？',
        'options': [
            {'text': '我只選保本型商品', 'type': 'squirrel'},
            {'text': '有趣，先買一點試試看', 'type': 'cheetah'},
            {'text': '跟家人朋友一起討論', 'type': 'raccoon'},
            {'text': '要做功課，詳細分析才知道好不好', 'type': 'owl'},
            {'text': '會先問一些專業人士的意見', 'type': 'wolf'},
            {'text': '如果有大銀行推薦應該沒問題', 'type': 'peacock'}
        ]
    },
    {
        'question': '感覺經濟衰退時，你的應對策略是？',
        'options': [
            {'text': '減少消費，節省到極限', 'type': 'squirrel'},
            {'text': '多買樂透看會不會中頭獎', 'type': 'cheetah'},
            {'text': '多跟朋友聊聊看他們的情況', 'type': 'raccoon'},
            {'text': '重新計算自已的資產看看會不會有風險', 'type': 'owl'},
            {'text': '就等這個機會買法拍屋，以後一定賺', 'type': 'wolf'},
            {'text': '跟平常一樣，又不一定會發生，', 'type': 'peacock'}
        ]
    },
    {
        'question': '計畫出國旅行時，你優先考慮？',
        'options': [
            {'text': '預算最重要，超出太多就不考慮了', 'type': 'squirrel'},
            {'text': '就說走就走，機票買了再說！', 'type': 'cheetah'},
            {'text': '一定要問朋友推薦，有人去過才不踩雷', 'type': 'raccoon'},
            {'text': '詳細比較機票、住宿、行程，出國也要精打細算。', 'type': 'owl'},
            {'text': '旅行能不能順便開拓人脈或找到商機', 'type': 'wolf'},
            {'text': '高級飯店、頂級美食、網紅打卡地點不能少！', 'type': 'peacock'}
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
