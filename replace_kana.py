import re

with open('concepts.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '<h4>居場所 <span style="font-size:0.75rem; font-weight:normal;">(いばしょ)</span></h4><span>Ibasho</span>': '<h4>居場所 <span style="font-size:0.75rem; font-weight:normal;">(Ibasho)</span></h4><span>いばしょ</span>',
    '<h4>出場 <span style="font-size:0.75rem; font-weight:normal;">(出番 / でばん)</span></h4><span>Deban</span>': '<h4>出場 <span style="font-size:0.75rem; font-weight:normal;">(出番 / Deban)</span></h4><span>でばん</span>',
    '<h4>微型公共化 <span style="font-size:0.75rem; font-weight:normal;">(住み開き)</span></h4><span>Sumibiraki</span>': '<h4>微型公共化 <span style="font-size:0.75rem; font-weight:normal;">(住み開き)</span></h4><span>すみびらき</span>',
    '<h4>恩送 <span style="font-size:0.75rem; font-weight:normal;">(恩返し)</span></h4><span>Pay it forward</span>': '<h4>恩送 <span style="font-size:0.75rem; font-weight:normal;">(恩返し)</span></h4><span>おんがえし</span>',
    '<h4>關係的故鄉 <span style="font-size:0.75rem; font-weight:normal;">(関係の故郷)</span></h4><span>Hometown</span>': '<h4>關係的故鄉 <span style="font-size:0.75rem; font-weight:normal;">(関係の故郷)</span></h4><span>かんけいのふるさと</span>',
    '<h4>軟著陸 <span style="font-size:0.75rem; font-weight:normal;">(ソフトランディング)</span></h4><span>Soft Landing</span>': '<h4>軟著陸 <span style="font-size:0.75rem; font-weight:normal;">(ソフトランディング)</span></h4><span>Soft Landing</span>',
    '<h4>消費者 <span style="font-size:0.75rem; font-weight:normal;">(消費者)</span></h4><span>Consumer</span>': '<h4>消費者 <span style="font-size:0.75rem; font-weight:normal;">(消費者)</span></h4><span>しょうひしゃ</span>',
    '<h4>甜甜圈 <span style="font-size:0.75rem; font-weight:normal;">(ドーナツ化)</span></h4><span>Donut Theory</span>': '<h4>甜甜圈 <span style="font-size:0.75rem; font-weight:normal;">(ドーナツ化)</span></h4><span>ドーナツか</span>',
    '<h4>自我決定 <span style="font-size:0.75rem; font-weight:normal;">(自己決定)</span></h4><span>Self-determination</span>': '<h4>自我決定 <span style="font-size:0.75rem; font-weight:normal;">(自己決定)</span></h4><span>じこけってい</span>',
    '<h4>AAR 模式 <span style="font-size:0.75rem; font-weight:normal;">(アクションリサーチ)</span></h4><span>Action Research</span>': '<h4>AAR 模式 <span style="font-size:0.75rem; font-weight:normal;">(アクションリサーチ)</span></h4><span>Action Research</span>',
    '<h4>PDCA 模式 <span style="font-size:0.75rem; font-weight:normal;">(PDCAサイクル)</span></h4><span>Plan-Do-Check-Act</span>': '<h4>PDCA 模式 <span style="font-size:0.75rem; font-weight:normal;">(PDCAサイクル)</span></h4><span>Plan-Do-Check-Act</span>',
    '<h4>老年期超越 <span style="font-size:0.75rem; font-weight:normal;">(老年的超越)</span></h4><span>Gerotranscendence</span>': '<h4>老年期超越 <span style="font-size:0.75rem; font-weight:normal;">(老年的超越)</span></h4><span>ろうねんてきちょうえつ</span>',
    '<h4>社會處方箋 <span style="font-size:0.75rem; font-weight:normal;">(社会的処方)</span></h4><span>Social Prescribing</span>': '<h4>社會處方箋 <span style="font-size:0.75rem; font-weight:normal;">(社会的処方)</span></h4><span>しゃかいてきしょほう</span>',
    '<h4>陪伴與留白 <span style="font-size:0.75rem; font-weight:normal;">(伴走と余白)</span></h4><span>Accompaniment</span>': '<h4>陪伴與留白 <span style="font-size:0.75rem; font-weight:normal;">(伴走と余白)</span></h4><span>ばんそうとよはく</span>',
    '<h4>動態拼圖 <span style="font-size:0.75rem; font-weight:normal;">(ジグソーパズル)</span></h4><span>Dynamic Puzzle</span>': '<h4>動態拼圖 <span style="font-size:0.75rem; font-weight:normal;">(ジグソーパズル)</span></h4><span>Dynamic Puzzle</span>',
    '<h4>創生 <span style="font-size:0.75rem; font-weight:normal;">(地方創生)</span></h4><span>Revitalization</span>': '<h4>創生 <span style="font-size:0.75rem; font-weight:normal;">(地方創生)</span></h4><span>ちほうそうせい</span>',
    '<h4>共感 <span style="font-size:0.75rem; font-weight:normal;">(コンパッション)</span></h4><span>Compassion</span>': '<h4>共感 <span style="font-size:0.75rem; font-weight:normal;">(コンパッション)</span></h4><span>Compassion</span>',
    '<h4>微型社會 <span style="font-size:0.75rem; font-weight:normal;">(ちいさな社会)</span></h4><span>Micro Society</span>': '<h4>微型社會 <span style="font-size:0.75rem; font-weight:normal;">(ちいさな社会)</span></h4><span>ちいさなしゃかい</span>',
    '<h4>學習的再定義 <span style="font-size:0.75rem; font-weight:normal;">(学びの再定義)</span></h4><span>Redefine Learning</span>': '<h4>學習的再定義 <span style="font-size:0.75rem; font-weight:normal;">(学びの再定義)</span></h4><span>まなびのさいていぎ</span>',
    '<h4>世代傳承性 <span style="font-size:0.75rem; font-weight:normal;">(世代継承性)</span></h4><span>Generativity</span>': '<h4>世代傳承性 <span style="font-size:0.75rem; font-weight:normal;">(世代継承性)</span></h4><span>せだいけいしょうせい</span>',
    '<h4>晶體智力 <span style="font-size:0.75rem; font-weight:normal;">(結晶性知能)</span></h4><span>Crystallized</span>': '<h4>晶體智力 <span style="font-size:0.75rem; font-weight:normal;">(結晶性知能)</span></h4><span>けっしょうせいちのう</span>',
    '<h4>實踐者 <span style="font-size:0.75rem; font-weight:normal;">(実践者)</span></h4><span>Doer</span>': '<h4>實踐者 <span style="font-size:0.75rem; font-weight:normal;">(実践者)</span></h4><span>じっせんしゃ</span>',
    '<h4>存在欲望 <span style="font-size:0.75rem; font-weight:normal;">(存在欲求)</span></h4><span>Desire to Exist</span>': '<h4>存在欲望 <span style="font-size:0.75rem; font-weight:normal;">(存在欲求)</span></h4><span>そんざいよっきゅう</span>',
    '<h4>圓形監獄 <span style="font-size:0.75rem; font-weight:normal;">(パノプティコン)</span></h4><span>Panopticon</span>': '<h4>圓形監獄 <span style="font-size:0.75rem; font-weight:normal;">(パノプティコン)</span></h4><span>Panopticon</span>',
    '<h4>規訓社會 <span style="font-size:0.75rem; font-weight:normal;">(規律訓練型社会)</span></h4><span>Disciplinary</span>': '<h4>規訓社會 <span style="font-size:0.75rem; font-weight:normal;">(規律訓練型社会)</span></h4><span>きりつくんれんがたしゃかい</span>',
    '<h4>匿名性社會 <span style="font-size:0.75rem; font-weight:normal;">(匿名性社会)</span></h4><span>Anonymous</span>': '<h4>匿名性社會 <span style="font-size:0.75rem; font-weight:normal;">(匿名性社会)</span></h4><span>とくめいせいしゃかい</span>',
    '<h4>回流教育 <span style="font-size:0.75rem; font-weight:normal;">(リカレント教育)</span></h4><span>Recurrent</span>': '<h4>回流教育 <span style="font-size:0.75rem; font-weight:normal;">(リカレント教育)</span></h4><span>リカレントきょういく</span>',
    '<h4>孤立與孤食 <span style="font-size:0.75rem; font-weight:normal;">(孤立と孤食)</span></h4><span>Isolation</span>': '<h4>孤立與孤食 <span style="font-size:0.75rem; font-weight:normal;">(孤立と孤食)</span></h4><span>こりつとこしょく</span>',
    '<h4>終身學習 <span style="font-size:0.75rem; font-weight:normal;">(生涯学習)</span></h4><span>Lifelong</span>': '<h4>終身學習 <span style="font-size:0.75rem; font-weight:normal;">(生涯学習)</span></h4><span>しょうがいがくしゅう</span>',
    '<h4 style="font-size:1rem; line-height:1.2;">捨棄故鄉的學力 <span style="font-size:0.65rem; font-weight:normal; display:block;">(ふるさとを捨てる学力)</span></h4>': '<h4 style="font-size:1rem; line-height:1.2;">捨棄故鄉的學力 <span style="font-size:0.65rem; font-weight:normal; display:block;">(ふるさとを捨てる学力)</span></h4><span>ふるさとをすてるがくりょく</span>'
}

for k, v in replacements.items():
    if k not in text:
        print(f"Missing: {k}")
    text = text.replace(k, v)

with open('concepts.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
