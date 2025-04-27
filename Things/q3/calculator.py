import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QSizePolicy


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """계산기 UI를 초기화하는 함수"""
        self.setWindowTitle('Calculator')  # 창 제목 설정
        self.setFixedSize(300, 400)  # 창 크기 고정

        # 디스플레이 (결과 표시창) 설정
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 직접 입력 불가능, 출력 전용
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 가로 확장 가능, 세로 고정
        self.display.setFixedHeight(50)  # 디스플레이 높이 고정

        # 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 4)  # 디스플레이를 첫 번째 줄에 4칸 차지하도록 배치

        # 버튼 목록 (텍스트, 행, 열[, rowspan, colspan])
        buttons = [
            ('AC', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('\u00F7', 1, 3),  # ÷
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('\u00D7', 2, 3),    # ×
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        # 버튼 생성 및 레이아웃에 추가
        for b in buttons:
            if len(b) == 3:
                text, row, col = b
                rowspan, colspan = 1, 1  # 기본 rowspan, colspan은 1
            else:
                text, row, col, rowspan, colspan = b  # 4개짜리 설정 (특히 0번 버튼)

            button = QPushButton(text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 버튼 크기 늘어나게
            button.clicked.connect(self.on_button_click)  # 버튼 클릭 시 이벤트 연결
            grid.addWidget(button, row, col, rowspan, colspan)  # 버튼을 그리드에 추가

        self.setLayout(grid)  # 전체 레이아웃 설정

    def on_button_click(self):
        """버튼 클릭 시 호출되는 이벤트 핸들러"""
        sender = self.sender()
        text = sender.text()

        if text == 'AC':
            # AC 버튼: 모든 입력 지우기
            self.display.clear()

        elif text == '+/-':
            # +/- 버튼: 현재 숫자의 부호 변경
            current_text = self.display.text()
            if current_text:
                if current_text.startswith('-'):
                    self.display.setText(current_text[1:])  # - 있으면 제거
                else:
                    self.display.setText('-' + current_text)  # 없으면 - 추가

        elif text == '%':
            # % 버튼: 현재 숫자를 100으로 나누기
            current_text = self.display.text()
            if current_text:
                try:
                    value = float(current_text) / 100
                    self.display.setText(str(value))
                except ValueError:
                    self.display.setText('Error')

        elif text == '=':
            # = 버튼: 계산 수행
            try:
                expression = self.display.text()
                # ÷, × 기호를 Python 연산자로 변환
                expression = expression.replace('\u00F7', '/').replace('\u00D7', '*')
                result = eval(expression)  # 문자열 계산
                self.display.setText(str(result))
            except Exception:
                self.display.setText('Error')  # 계산 오류 시 Error 출력

        else:
            # 숫자, 연산자 버튼: 디스플레이에 이어 붙이기
            current_text = self.display.text()
            self.display.setText(current_text + text)


def main():
    """프로그램 진입점"""
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())  # 앱 실행


if __name__ == '__main__':
    main()
