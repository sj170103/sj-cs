import sys
from math import isfinite
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QSizePolicy

# 계산 로직 클래스: 숫자 입력, 연산자 처리, 결과 계산 담당
class CalculatorCore:
    def __init__(self):
        self.reset()

    # 상태 초기화
    def reset(self):
        self._current = '0'
        self._operand = None
        self._operator = None
        self._just_evaluated = False
        self._expression = ''

    # 숫자 입력 처리
    def input_digit(self, d):
        if self._just_evaluated:
            self._current, self._expression, self._just_evaluated = d, '', False
        elif self._current == '0':
            self._current = d
        else:
            self._current += d

    # 소수점 입력 처리
    def input_decimal(self):
        if self._just_evaluated:
            self._current, self._expression, self._just_evaluated = '0.', '', False
        elif '.' not in self._current:
            self._current += '.'

    # 부호 반전
    def negative_positive(self):
        if self._current.startswith('-'):
            self._current = self._current[1:]
        elif self._current != '0':
            self._current = '-' + self._current

    # 퍼센트 처리
    def percent(self):
        try:
            self._current = self._format(float(self._current) / 100)
        except:
            self._current = 'Error'

    # 연산자 설정 및 처리
    def set_operator(self, op):
        if self._just_evaluated:
            self._operand = float(self._current)
            self._just_evaluated = False
        elif self._operator:
            self._calculate()
        else:
            self._operand = float(self._current)

        if self._expression and self._expression[-1] in '+-×÷':
            self._expression = self._expression[:-1]
        else:
            self._expression = self._format(self._operand)

        self._operator = op
        symbol = {'+': '+', '-': '-', '*': '×', '/': '÷'}[op]
        self._expression += symbol
        self._current = '0'

    # = 버튼 처리
    def equal(self):
        if self._operator:
            self._calculate()
            self._operator = None
            self._expression = ''
            self._just_evaluated = True

    # 출력할 문자열 반환
    def display(self):
        return self._expression + self._current if self._expression else self._current

    # 사칙연산 수행
    def _calculate(self):
        try:
            a = self._operand
            b = float(self._current)
            if self._operator == '+':
                r = a + b
            elif self._operator == '-':
                r = a - b
            elif self._operator == '*':
                r = a * b
            elif self._operator == '/':
                if b == 0:
                    raise ZeroDivisionError
                r = a / b
            else:
                return

            if not isfinite(r):
                raise OverflowError

            self._operand = r
            self._current = self._format(r)
        except ZeroDivisionError:
            self._current, self._operand = 'Divide by 0', None
        except OverflowError:
            self._current, self._operand = 'Overflow', None
        except:
            self._current, self._operand = 'Error', None

    # 결과 포맷 (소수점 6자리 반올림, 불필요한 0 제거)
    def _format(self, v):
        return format(round(v, 6), '.6f').rstrip('0').rstrip('.') or '0'

# UI 클래스: 버튼 및 화면 구성
class Calculator(QWidget):
    # 버튼 스타일 미리 지정
    BTN_STYLES = {
        'num': "background:#505050; color:white; font-size:24px; border-radius:30px;",
        'op':  "background:#FF9500; color:white; font-size:24px; border-radius:30px;",
        'fn':  "background:#D4D4D2; color:black; font-size:24px; border-radius:30px;",
    }

    def __init__(self):
        super().__init__()
        self.core = CalculatorCore()
        self._init_ui()

    # UI 초기 설정
    def _init_ui(self):
        self.setWindowTitle('계산기')
        self.setFixedSize(320, 480)
        self.setStyleSheet("background-color: #000;")

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("background-color: black; color: white; border: none;")
        self.display.setFont(QFont("Arial", 32))
        self.display.setFixedHeight(80)

        # 버튼 레이아웃
        grid = QGridLayout()
        grid.setSpacing(10)

        buttons = [
            ('AC','fn'), ('+/-','fn'), ('%','fn'), ('÷','op'),
            ('7','num'),('8','num'),('9','num'),('×','op'),
            ('4','num'),('5','num'),('6','num'),('-','op'),
            ('1','num'),('2','num'),('3','num'),('+','op'),
            ('0','num'),('.', 'num'), ('=','op')
        ]

        # 버튼 생성 및 배치
        r, c = 0, 0
        for text, style in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(self.BTN_STYLES[style])
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFixedHeight(60)

            # 버튼 기능 연결
            if text.isdigit():
                handler = partial(self.core.input_digit, text)
            elif text == '.':
                handler = self.core.input_decimal
            elif text in ['+', '-', '×', '÷']:
                op_map = {'×': '*', '÷': '/', '+': '+', '-': '-'}
                handler = partial(self.core.set_operator, op_map[text])
            elif text == '=':
                handler = self.core.equal
            else:
                handler = {
                    'AC': self.core.reset,
                    '+/-': self.core.negative_positive,
                    '%': self.core.percent
                }[text]

            btn.clicked.connect(lambda _, h=handler: (h(), self._update()))

            if text == '0':
                grid.addWidget(btn, 5, 0, 1, 2)
                c = 2
                continue
            elif text == '.':
                grid.addWidget(btn, 5, 2)
                continue
            elif text == '=':
                grid.addWidget(btn, 5, 3)
                continue

            grid.addWidget(btn, r + 1, c)
            c += 1
            if c > 3:
                r += 1
                c = 0

        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        self.setLayout(layout)
        self._update()

    # 화면 업데이트
    def _update(self):
        self.display.setText(self.core.display())
        self._adjust_font()

    # 텍스트 길이에 따라 폰트 크기 조절
    def _adjust_font(self):
        text = self.display.text()
        font = QFont("Arial")
        width = self.display.width() - 20
        size = 32
        while size >= 10:
            font.setPointSize(size)
            if QFontMetrics(font).horizontalAdvance(text) <= width:
                break
            size -= 1
        self.display.setFont(font)

# 실행 함수
def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
