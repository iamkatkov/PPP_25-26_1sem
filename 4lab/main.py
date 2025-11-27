import json

class BaseTask:
    def __init__(self, task_id, title, priority_value, priority_text, status):
        self.task_id = task_id
        self.title = title
        self.priority_value = priority_value     
        self.priority_text = priority_text       
        self.status = status

    def format(self):
        return f"[{self.task_id}] ({self.priority_text}, {self.status}) {self.title}"

class BugTask(BaseTask):
    PRIORITY_MAP = {
        "critical": 10,
        "high": 7,
        "medium": 5,
        "low": 2
    }

    @classmethod
    def parse(cls, line):
        parts = line.split(" ", 1)[1].split(";")
        if len(parts) != 4:
            raise ValueError("Неверный формат bug")

        task_id, title, severity, status = [p.strip() for p in parts]

        if severity not in cls.PRIORITY_MAP:
            raise ValueError("Неизвестный приоритет bug")

        priority_value = cls.PRIORITY_MAP[severity]
        priority_text = severity

        return cls(task_id, title, priority_value, priority_text, status)

class FeatureTask(BaseTask):
    @classmethod
    def parse(cls, line):
        json_str = line[len("feature "):].strip()
        try:
            data = json.loads(json_str)
        except Exception:
            raise ValueError("Ошибка разбора JSON feature")

        task_id = data["id"]
        title = data["title"]

        pr = data.get("story_points", 1)
        priority_value = pr
        priority_text = str(pr)

        status = data["status"]

        return cls(task_id, title, priority_value, priority_text, status)

class SupportTask(BaseTask):
    PRIORITY_MAP = {
        "critical": 10,
        "high": 7,
        "medium": 5,
        "low": 2
    }

    @classmethod
    def parse(cls, line):
        parts = line[len("support "):].split("|")
        if len(parts) != 4:
            raise ValueError("Неверный формат support")

        task_id, title, pr_text, status = [p.strip() for p in parts]

        if pr_text not in cls.PRIORITY_MAP:
            raise ValueError("Неизвестный приоритет support")

        priority_value = cls.PRIORITY_MAP[pr_text]
        priority_text = pr_text

        return cls(task_id, title, priority_value, priority_text, status)

PARSERS = {
    "bug": BugTask,
    "feature": FeatureTask,
    "support": SupportTask
}

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self, lines):
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            prefix = line.split(" ", 1)[0]
            if prefix not in PARSERS:
                print(f"Ошибка разбора задачи в строке {i}: неизвестный тип '{prefix}'")
                continue

            try:
                task = PARSERS[prefix].parse(line)
                self.tasks.append(task)
            except Exception as e:
                print(f"Ошибка разбора задачи в строке {i}: {e}")

    def command_list(self, status):
        result = [t for t in self.tasks if t.status == status]
        if not result:
            print("Нет задач")
            return
        for t in result:
            print(t.format())

    def command_top(self, n):
        result = sorted(self.tasks, key=lambda t: t.priority_value, reverse=True)
        for t in result[:n]:
            print(t.format())

    def command_search(self, text):
        result = [t for t in self.tasks if text.lower() in t.title.lower()]
        if not result:
            print("Задачи не найдены")
            return
        for t in result:
            print(t.format())

def interactive_loop(task_manager: TaskManager):
    print("Доступные команды:")
    print("list <status>")
    print("top <n>")
    print("search <text>")
    print("help")
    print("exit")

    while True:
        cmd = input("\n> ").strip()
        if not cmd:
            continue

        if cmd == "exit":
            print("Выход.")
            break

        if cmd == "help":
            print("Команды:")
            print("list <status>     — вывести задачи по статусу (open / closed / in_progress и т.д.)")
            print("top <n>           — вывести первые n задач с максимальным приоритетом")
            print("search <text>     — поиск в названии/описании")
            print("exit              — выход")
            continue

        parts = cmd.split(" ", 1)
        action = parts[0]

        if action == "list":
            if len(parts) < 2:
                print("Использование: list <status>")
                continue
            task_manager.command_list(parts[1].strip())

        elif action == "top":
            if len(parts) < 2 or not parts[1].isdigit():
                print("Использование: top <n>")
                continue
            task_manager.command_top(int(parts[1]))

        elif action == "search":
            if len(parts) < 2:
                print("Использование: search <text>")
                continue
            task_manager.command_search(parts[1])

        else:
            print("Неизвестная команда. Введите 'help'.")

if __name__ == "__main__":
    print("Загрузка исходных задач...")

    input_tasks = [
        "bug BUG-101;Неверный расчёт налога;critical;open",
        "feature {\"id\": \"F-202\", \"title\": \"Добавить тёмную тему\", \"story_points\": 5, \"status\": \"in_progress\"}",
        "support T-303|Проблемы со входом|high|open",
    ]

    tm = TaskManager()
    tm.load_tasks(input_tasks)

    print("Готово, задачи загружены.")
    interactive_loop(tm)
