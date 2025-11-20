# frontend/html_provider.py
from pathlib import Path
from string import Template

TEMPLATE_DIR = Path(__file__).resolve().parent / 'templates'


def _load_template(file_name: str) -> Template:
    """템플릿 파일을 읽어 Template 객체로 반환."""
    template_path = TEMPLATE_DIR / file_name
    with template_path.open(encoding='utf-8') as file:
        return Template(file.read())


def _get_preview_text(content: str, limit: int = 80) -> str:
    """간단한 내용 미리보기 텍스트."""
    return content[:limit] + ('…' if len(content) > limit else '')


def get_list_html(questions):
    total_questions = len(questions)
    answered_questions = sum(1 for q in questions if q.answers)
    pending_questions = total_questions - answered_questions

    if questions:
        rows = ""
        for q in questions:
            answer_count = len(q.answers)
            status_badge = (
                f'<span class="badge rounded-pill bg-success">답변 {answer_count}건</span>'
                if answer_count
                else '<span class="badge rounded-pill bg-warning text-dark">미답변</span>'
            )
            rows += f"""
            <tr>
                <td class="fw-semibold">{q.id}</td>
                <td>
                    <div class="d-flex flex-column">
                        <a class="question-link" href="/view/detail/{q.id}">{q.subject}</a>
                        <span class="text-muted small">{_get_preview_text(q.content)}</span>
                    </div>
                </td>
                <td>{q.create_date}</td>
                <td>{status_badge}</td>
            </tr>
            """
    else:
        rows = """
        <tr>
            <td colspan="4" class="text-center text-muted">등록된 질문이 없습니다. 아래 폼으로 첫 질문을 남겨보세요.</td>
        </tr>
        """

    template = _load_template('question_list.html')
    return template.substitute(
        stats_total=total_questions,
        stats_answered=answered_questions,
        stats_pending=pending_questions,
        question_rows=rows
    )


def get_detail_html(question):
    if question.answers:
        answers_html = ""
        for answer in question.answers:
            answers_html += f"""
            <div class="answer-card">
                <p class="mb-2">{answer.content}</p>
                <div class="badge bg-light text-dark text-uppercase small">{answer.create_date}</div>
            </div>
            """
    else:
        answers_html = """
        <div class="text-muted">아직 등록된 답변이 없습니다.</div>
        """

    template = _load_template('question_detail.html')
    return template.substitute(
        question_id=question.id,
        question_subject=question.subject,
        question_content=question.content,
        question_create_date=question.create_date,
        answer_count=len(question.answers),
        answers_html=answers_html
    )
