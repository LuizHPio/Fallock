from tests.vector2Tests import Vector2Tester


def main_thread():
    tester = Vector2Tester()
    print(f'Test 01 status: {"Success" if tester.test01() else "Failure"}')


if __name__ == "__main__":
    main_thread()
