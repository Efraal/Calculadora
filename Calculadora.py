from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MainApp(App):
    def build(self):
        self.operators = ['/', '*', '+', '-']
        self.last_operator = None
        self.last_button = None
        self.last_period = None

        main_layout = BoxLayout(orientation = "vertical")

        self.solution = TextInput(
            text = '0', multiline = False, readonly = True, halign = "right", font_size = 55
        )
        main_layout.add_widget(self.solution)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['.', '0', 'C', '+'],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text = label,
                    pos_hint = {"center_x": .5, "center_y": .5},
                )
                button.bind(on_press = self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equal_button = Button(
            text='=', pos_hint={"center_x": .5, "center_y": .5}
        )
        equal_button.bind(on_press = self.on_solution)
        main_layout.add_widget(equal_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        self.last_period = self.period_check(current)

        if button_text == 'C':
            self.solution.text = '0'
        else:
            if current and (self.last_operator and button_text in self.operators):
                new_text = current[:-1]+button_text
                self.solution.text = new_text
                return
            elif button_text == '.' and self.last_period != -1:
                return
            elif current == '0':
                if button_text in self.operators:
                    return
                elif button_text == '0':
                    return
                elif button_text != '.':
                    new_text = button_text
                    self.solution.text = new_text
                else:
                    new_text = current + button_text
                    self.solution.text = new_text
            elif self.last_button == '=' and button_text not in self.operators and button_text != '.':
                new_text = button_text
                self.solution.text = new_text
            else:
                new_text = current + button_text
                self.solution.text = new_text


        self.last_button = button_text
        self.last_operator = self.last_button in self.operators

    def on_solution(self, instance):
        self.last_button = '='
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution

    def period_check(self, current):
        xso = current.rfind("+")
        xsu = current.rfind("-")
        xmu = current.rfind("*")
        xdi = current.rfind("/")
        check = [int(xso), int(xsu), int(xmu), int(xdi)]
        check = max(check)
        if check == -1:
            check = 0
        check = current.rfind(".", check)
        return check



if __name__ == '__main__':
    app = MainApp()
    app.run()
