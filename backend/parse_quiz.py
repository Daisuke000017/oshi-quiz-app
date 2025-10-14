import re
import json

def parse_quiz_markdown(md_file_path):
    """
    【推しの子】究極クイズのMarkdownファイルをパースして、
    クイズデータを構造化して返す
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    quizzes = []
    current_part = None
    current_set = None
    current_quiz = None
    current_question = None

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # 第一部、第二部、第三部の検出
        if line.startswith('## **第'):
            if '初級編' in line:
                current_part = {'name': '初級編', 'difficulty': 'beginner', 'sets': []}
            elif '中級編' in line:
                current_part = {'name': '中級編', 'difficulty': 'intermediate', 'sets': []}
            elif '上級編' in line:
                current_part = {'name': '上級編', 'difficulty': 'advanced', 'sets': []}

        # セットの検出
        elif line.startswith('### **セット'):
            set_title = line.replace('###', '').replace('**', '').strip()
            set_title = re.sub(r'^セット\d+[:：]', '', set_title).strip()
            current_set = {
                'title': set_title,
                'questions': []
            }
            if current_part:
                current_part['sets'].append(current_set)

        # 問題の検出
        elif line.startswith('問題') and not line.startswith('問題文'):
            # 新しい問題の開始
            if current_question and current_set:
                current_set['questions'].append(current_question)

            current_question = {
                'question_text': '',
                'choices': [],
                'correct_answer': '',
                'explanation': ''
            }
            i += 1
            continue

        # 問題文の収集
        elif current_question is not None and not line.startswith(('A.', 'B.', 'C.', 'D.', '答え', '解説')):
            if line and current_question['question_text'] == '':
                current_question['question_text'] = line

        # 選択肢の検出
        elif line.startswith(('A.', 'B.', 'C.', 'D.')):
            choice_text = line[3:].strip()
            current_question['choices'].append(choice_text)

        # 正解の検出
        elif line.startswith('答え'):
            answer_match = re.search(r'[ABCD]\.', line)
            if answer_match:
                current_question['correct_answer'] = answer_match.group()[0]

        # 解説の検出
        elif line.startswith('解説'):
            explanation = line.replace('解説：', '').replace('解説:', '').strip()
            current_question['explanation'] = explanation

        # 引用文献セクションに到達したら終了
        elif '引用文献' in line:
            if current_question and current_set:
                current_set['questions'].append(current_question)
            break

        i += 1

    # 最後の問題を追加
    if current_question and current_set:
        current_set['questions'].append(current_question)

    # パートごとにクイズを整理
    all_parts = []

    # 初級編、中級編、上級編を探す
    for part_data in [current_part]:  # この実装では最後のパートのみ保持されているので改善が必要
        if part_data:
            all_parts.append(part_data)

    return all_parts

def extract_all_parts(md_file_path):
    """
    Markdownファイルから全てのパート（初級、中級、上級）を抽出
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = []

    # 第一部（初級編）を抽出
    beginner_match = re.search(r'## \*\*第一部：初級編.*?\n(.*?)(?=## \*\*第二部|$)', content, re.DOTALL)
    if beginner_match:
        parts.append({
            'name': '初級編',
            'difficulty': 'beginner',
            'content': beginner_match.group(1)
        })

    # 第二部（中級編）を抽出
    intermediate_match = re.search(r'## \*\*第二部：中級編.*?\n(.*?)(?=## \*\*第三部|$)', content, re.DOTALL)
    if intermediate_match:
        parts.append({
            'name': '中級編',
            'difficulty': 'intermediate',
            'content': intermediate_match.group(1)
        })

    # 第三部（上級編）を抽出
    advanced_match = re.search(r'## \*\*第三部：上級編.*?\n(.*?)(?=####|$)', content, re.DOTALL)
    if advanced_match:
        parts.append({
            'name': '上級編',
            'difficulty': 'mania',  # 上級なのでmaniaレベルに設定
            'content': advanced_match.group(1)
        })

    # 各パートから問題を抽出
    for part in parts:
        part['sets'] = parse_questions_from_content(part['content'])
        del part['content']

    return parts

def parse_questions_from_content(content):
    """
    コンテンツから問題を抽出
    """
    sets = []

    # セットを分割
    set_pattern = r'### \*\*セット\d+[：:](.*?)\*\*\n(.*?)(?=### \*\*セット|$)'
    set_matches = re.finditer(set_pattern, content, re.DOTALL)

    for set_match in set_matches:
        set_title = set_match.group(1).strip()
        set_content = set_match.group(2)

        questions = []

        # 問題を分割
        question_blocks = re.split(r'\n問題\d+\s*\n', set_content)

        for block in question_blocks:
            if not block.strip():
                continue

            question = parse_single_question(block)
            if question:
                questions.append(question)

        if questions:
            sets.append({
                'title': set_title,
                'questions': questions
            })

    return sets

def parse_single_question(block):
    """
    単一の問題ブロックをパース
    """
    lines = block.strip().split('\n')

    question_data = {
        'question_text': '',
        'choices': [],
        'correct_answer': '',
        'explanation': ''
    }

    mode = 'question'

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # 選択肢の検出
        if re.match(r'^[ABCD]\.', line):
            choice_text = line[3:].strip()
            question_data['choices'].append(choice_text)
            mode = 'choices'

        # 答えの検出
        elif line.startswith('答え'):
            answer_match = re.search(r'([ABCD])\.', line)
            if answer_match:
                question_data['correct_answer'] = answer_match.group(1)
            mode = 'answer'

        # 解説の検出
        elif line.startswith('解説'):
            explanation = re.sub(r'^解説[：:]\s*', '', line)
            question_data['explanation'] = explanation
            mode = 'explanation'

        # 問題文の収集
        elif mode == 'question':
            if question_data['question_text']:
                question_data['question_text'] += ' ' + line
            else:
                question_data['question_text'] = line

    # 問題文と選択肢が両方存在する場合のみ返す
    if question_data['question_text'] and len(question_data['choices']) >= 2:
        return question_data

    return None

if __name__ == '__main__':
    md_path = '/Users/daisukeinoue/APP開発/推しの子クイズ/【推しの子】究極クイズ（4択選択式）.md'
    parts = extract_all_parts(md_path)

    print(f"抽出されたパート数: {len(parts)}")

    for part in parts:
        print(f"\n{part['name']} (難易度: {part['difficulty']})")
        print(f"  セット数: {len(part['sets'])}")

        total_questions = sum(len(s['questions']) for s in part['sets'])
        print(f"  総問題数: {total_questions}")

        for i, quiz_set in enumerate(part['sets'], 1):
            print(f"    セット{i}: {quiz_set['title']} ({len(quiz_set['questions'])}問)")

    # JSONとして保存
    output_path = '/Users/daisukeinoue/APP開発/推しの子クイズ/oshi-quiz-deploy/backend/oshinoko_quiz_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parts, f, ensure_ascii=False, indent=2)

    print(f"\n問題データを {output_path} に保存しました")
