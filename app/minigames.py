import random


class MiniGame:
    """Mini-games for the Flask app."""

    @staticmethod
    def memory_game():
        """Generate a memory sequence game."""
        sequence = [random.randint(1, 4) for _ in range(5)]
        return {"game_type": "memory", "sequence": sequence, "user_sequence": []}

    @staticmethod
    def quick_math():
        """Generate a quick math challenge."""
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-", "*"])

        if operation == "+":
            answer = num1 + num2
        elif operation == "-":
            answer = num1 - num2
        else:
            answer = num1 * num2

        return {
            "game_type": "math",
            "problem": f"{num1} {operation} {num2}",
            "answer": answer,
        }

    @staticmethod
    def riddle():
        """Get a random riddle."""
        riddles = [
            {
                "riddle": "I have keys but no locks. What am I?",
                "answer": "piano",
            },
            {
                "riddle": "What has hands but can't clap?",
                "answer": "clock",
            },
            {
                "riddle": "I'm tall when I'm young and short when I'm old. What am I?",
                "answer": "candle",
            },
            {
                "riddle": "What can travel around the world while staying in a corner?",
                "answer": "stamp",
            },
            {
                "riddle": "The more you take, the more you leave behind. What am I?",
                "answer": "footsteps",
            },
        ]

        return {"game_type": "riddle", **random.choice(riddles)}

    @staticmethod
    def color_match():
        """Generate a color matching game."""
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        selected_color = random.choice(colors)
        options = random.sample(colors, 4)

        if selected_color not in options:
            options[0] = selected_color

        random.shuffle(options)

        return {
            "game_type": "color",
            "target_color": selected_color,
            "options": options,
        }
