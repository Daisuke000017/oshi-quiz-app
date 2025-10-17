"""
軽量版シードデータ - 無料インスタンス用
推しの子クイズ（30問）
"""
import sys
import os

# Flaskアプリのコンテキストをインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.user import db, User
from src.models.quiz import Quiz, Question, Choice, OshiTag
from datetime import datetime

def seed_data():
    """軽量版シードデータを投入（30問）"""

    # ユーザーを作成
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        db.session.add(admin)
        db.session.commit()

    # 推しの子タグを作成
    oshinoko_tag = OshiTag.query.filter_by(name='推しの子').first()
    if not oshinoko_tag:
        oshinoko_tag = OshiTag(
            name='推しの子',
            category='anime',
            description='アニメ・漫画『【推しの子】』'
        )
        db.session.add(oshinoko_tag)
        db.session.commit()

    # クイズ1: 初級編（10問）
    quiz1 = Quiz(
        creator_id=admin.id,
        title='【推しの子】初級クイズ',
        description='主要キャラクターと物語の基本に関するクイズ',
        oshi_tag_id=oshinoko_tag.id,
        difficulty='beginner',
        is_public=True
    )
    db.session.add(quiz1)
    db.session.flush()

    # クイズ1の問題
    questions_quiz1 = [
        {
            'question_text': '伝説のアイドル・星野アイが所属していたアイドルグループの名前は？',
            'choices': ['A小町', 'B小町', '苺プロダクション', '劇団ララライ'],
            'correct_index': 1,
            'explanation': '星野アイが不動のセンターとして活躍していたアイドルグループが「B小町」です。'
        },
        {
            'question_text': '主人公アクアの前世の職業は？',
            'choices': ['産婦人科医', '映画監督', 'プロデューサー', '小児科医'],
            'correct_index': 0,
            'explanation': 'アクアの前世は、地方の病院に勤務する産婦人科医・雨宮吾郎です。'
        },
        {
            'question_text': 'アクアの双子の妹の名前は？',
            'choices': ['星野アイ', '星野ルビー', '黒川あかね', '有馬かな'],
            'correct_index': 1,
            'explanation': 'アクアの双子の妹は星野ルビーです。'
        },
        {
            'question_text': '星野アイが所属していた芸能事務所は？',
            'choices': ['苺プロダクション', 'ベリープロ', 'スターライト', 'ララライ事務所'],
            'correct_index': 0,
            'explanation': '星野アイは苺プロダクションに所属していました。'
        },
        {
            'question_text': 'アクアの本名は？',
            'choices': ['雨宮吾郎', '星野アクアマリン', '黒川涼', '五反田泰志'],
            'correct_index': 1,
            'explanation': 'アクアの本名は星野アクアマリンです。'
        },
        {
            'question_text': '新生B小町のセンターを務めるのは誰？',
            'choices': ['有馬かな', '星野ルビー', '黒川あかね', 'MEMちょ'],
            'correct_index': 1,
            'explanation': '新生B小町のセンターは星野ルビーです。'
        },
        {
            'question_text': 'アクアが最初に出演した映画のジャンルは？',
            'choices': ['恋愛映画', 'ホラー映画', 'アクション映画', 'コメディ映画'],
            'correct_index': 1,
            'explanation': 'アクアが最初に出演したのはホラー映画です。'
        },
        {
            'question_text': '有馬かなの職業は？',
            'choices': ['アイドル', '女優', 'YouTuber', '歌手'],
            'correct_index': 1,
            'explanation': '有馬かなは元天才子役の女優です。'
        },
        {
            'question_text': 'MEMちょの職業は？',
            'choices': ['アイドル', 'YouTuber', '女優', 'モデル'],
            'correct_index': 1,
            'explanation': 'MEMちょはYouTuberです。'
        },
        {
            'question_text': '物語の舞台となる主な場所は？',
            'choices': ['大阪', '東京', '名古屋', '福岡'],
            'correct_index': 1,
            'explanation': '物語の舞台は主に東京です。'
        }
    ]

    for i, q_data in enumerate(questions_quiz1):
        question = Question(
            quiz_id=quiz1.id,
            question_text=q_data['question_text'],
            question_type='multiple_choice',
            order_index=i,
            explanation=q_data['explanation']
        )
        db.session.add(question)
        db.session.flush()

        for j, choice_text in enumerate(q_data['choices']):
            choice = Choice(
                question_id=question.id,
                choice_text=choice_text,
                is_correct=(j == q_data['correct_index']),
                order_index=j
            )
            db.session.add(choice)

    # クイズ2: 中級編（10問）
    quiz2 = Quiz(
        creator_id=admin.id,
        title='【推しの子】中級クイズ',
        description='恋愛リアリティショーと舞台編のクイズ',
        oshi_tag_id=oshinoko_tag.id,
        difficulty='intermediate',
        is_public=True
    )
    db.session.add(quiz2)
    db.session.flush()

    # クイズ2の問題
    questions_quiz2 = [
        {
            'question_text': 'アクアが参加した恋愛リアリティショーの名前は？',
            'choices': ['今夜、本気で恋します', '恋の駆け引き', 'ラブ・ゲーム', '真剣恋愛'],
            'correct_index': 0,
            'explanation': 'アクアが参加した恋愛リアリティショーは「今夜、本気で恋します（今ガチ）」です。'
        },
        {
            'question_text': '今ガチで黒川あかねが演じた役柄は？',
            'choices': ['優等生', '悪役', '天然キャラ', '星野アイ'],
            'correct_index': 3,
            'explanation': '黒川あかねは星野アイを完璧に演じました。'
        },
        {
            'question_text': '2.5次元舞台で上演された作品は？',
            'choices': ['銀河鉄道の夜', '東京ブレイド', 'ロミオとジュリエット', '星空のメモリア'],
            'correct_index': 1,
            'explanation': '2.5次元舞台で上演されたのは「東京ブレイド」です。'
        },
        {
            'question_text': '東京ブレイドでアクアが演じた役は？',
            'choices': ['主人公', '悪役', '脇役の刀鍛冶', 'ヒロイン'],
            'correct_index': 2,
            'explanation': 'アクアは脇役の刀鍛冶を演じました。'
        },
        {
            'question_text': '黒川あかねの特技は？',
            'choices': ['歌', 'ダンス', '演技分析', '料理'],
            'correct_index': 2,
            'explanation': '黒川あかねの特技は観察眼と演技分析です。'
        },
        {
            'question_text': '有馬かながアクアを「あくあく」と呼ぶ理由は？',
            'choices': ['本名から', '幼馴染だから', '子役時代の共演から', '趣味が同じ'],
            'correct_index': 2,
            'explanation': '有馬かなとアクアは子役時代に共演しており、その時から「あくあく」と呼んでいます。'
        },
        {
            'question_text': 'ルビーがアイドルを目指すきっかけとなった人物は？',
            'choices': ['星野アイ', '有馬かな', 'MEMちょ', 'さりな'],
            'correct_index': 0,
            'explanation': 'ルビーは母・星野アイに憧れてアイドルを目指しました。'
        },
        {
            'question_text': '苺プロダクションの社長は誰？',
            'choices': ['鏑木勝也', '斎藤ミヤコ', '鷲見ゆき', '五反田泰志'],
            'correct_index': 1,
            'explanation': '苺プロダクションの社長は斎藤ミヤコです。'
        },
        {
            'question_text': 'アクアの復讐の対象となっている人物は？',
            'choices': ['五反田泰志', 'カミキヒカル', '鏑木勝也', '上原清十郎'],
            'correct_index': 1,
            'explanation': 'アクアの復讐の対象はカミキヒカルです。'
        },
        {
            'question_text': '新生B小町のメンバー数は？',
            'choices': ['3人', '4人', '5人', '6人'],
            'correct_index': 0,
            'explanation': '新生B小町はルビー、かな、MEMちょの3人です。'
        }
    ]

    for i, q_data in enumerate(questions_quiz2):
        question = Question(
            quiz_id=quiz2.id,
            question_text=q_data['question_text'],
            question_type='multiple_choice',
            order_index=i,
            explanation=q_data['explanation']
        )
        db.session.add(question)
        db.session.flush()

        for j, choice_text in enumerate(q_data['choices']):
            choice = Choice(
                question_id=question.id,
                choice_text=choice_text,
                is_correct=(j == q_data['correct_index']),
                order_index=j
            )
            db.session.add(choice)

    # クイズ3: 上級編（10問）
    quiz3 = Quiz(
        creator_id=admin.id,
        title='【推しの子】上級クイズ',
        description='伏線と考察に関する上級者向けクイズ',
        oshi_tag_id=oshinoko_tag.id,
        difficulty='advanced',
        is_public=True
    )
    db.session.add(quiz3)
    db.session.flush()

    # クイズ3の問題
    questions_quiz3 = [
        {
            'question_text': '星野アイの「嘘」とは何を指す？',
            'choices': ['本当の気持ちを隠すこと', '子供がいること', '引退すること', '病気のこと'],
            'correct_index': 0,
            'explanation': '星野アイの「嘘」は、本当の気持ちを隠して演じることを指します。'
        },
        {
            'question_text': 'アクアの星の目が黒くなる条件は？',
            'choices': ['怒ったとき', '復讐心が薄れたとき', '嘘をついたとき', '悲しいとき'],
            'correct_index': 1,
            'explanation': 'アクアの星の目は復讐心が薄れると黒くなります。'
        },
        {
            'question_text': 'ゴロー先生が殺害された場所は？',
            'choices': ['病院', '海辺', '山', '街中'],
            'correct_index': 2,
            'explanation': 'ゴロー先生は山で殺害されました。'
        },
        {
            'question_text': '原作の連載雑誌は？',
            'choices': ['週刊少年ジャンプ', '週刊ヤングジャンプ', '月刊コミックジーン', 'ビッグコミックスピリッツ'],
            'correct_index': 1,
            'explanation': '【推しの子】は週刊ヤングジャンプで連載されています。'
        },
        {
            'question_text': 'アニメのOP主題歌を歌っているアーティストは？',
            'choices': ['YOASOBI', 'Ado', 'LiSA', 'Aimer'],
            'correct_index': 0,
            'explanation': 'アニメのOP主題歌「アイドル」はYOASOBIが歌っています。'
        },
        {
            'question_text': '原作者の赤坂アカの前作品は？',
            'choices': ['かぐや様は告らせたい', '五等分の花嫁', 'ぼっち・ざ・ろっく', '僕のヒーローアカデミア'],
            'correct_index': 0,
            'explanation': '赤坂アカの前作品は「かぐや様は告らせたい」です。'
        },
        {
            'question_text': '作画担当の横槍メンゴの前作品は？',
            'choices': ['クズの本懐', '五等分の花嫁', 'ドメスティックな彼女', '君に届け'],
            'correct_index': 0,
            'explanation': '横槍メンゴの前作品は「クズの本懐」です。'
        },
        {
            'question_text': 'アニメ制作会社は？',
            'choices': ['京都アニメーション', '動画工房', 'ufotable', 'A-1 Pictures'],
            'correct_index': 1,
            'explanation': 'アニメは動画工房が制作しています。'
        },
        {
            'question_text': '星野アイの声優は？',
            'choices': ['高橋李依', '雨宮天', '早見沙織', '水瀬いのり'],
            'correct_index': 1,
            'explanation': '星野アイの声優は雨宮天さんです。'
        },
        {
            'question_text': 'アクアの声優は？',
            'choices': ['梶裕貴', '大塚剛央', '内山昂輝', '花江夏樹'],
            'correct_index': 1,
            'explanation': 'アクアの声優は大塚剛央さんです。'
        }
    ]

    for i, q_data in enumerate(questions_quiz3):
        question = Question(
            quiz_id=quiz3.id,
            question_text=q_data['question_text'],
            question_type='multiple_choice',
            order_index=i,
            explanation=q_data['explanation']
        )
        db.session.add(question)
        db.session.flush()

        for j, choice_text in enumerate(q_data['choices']):
            choice = Choice(
                question_id=question.id,
                choice_text=choice_text,
                is_correct=(j == q_data['correct_index']),
                order_index=j
            )
            db.session.add(choice)

    db.session.commit()
    print('✅ 軽量版シードデータの投入が完了しました（30問）')
    print(f'クイズ数: 3')
    print(f'問題数: 30')

if __name__ == '__main__':
    from src.main import app
    with app.app_context():
        seed_data()
