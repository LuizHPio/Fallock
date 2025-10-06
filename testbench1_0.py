from tests.vector2Tests import Vector2Tester


def main_thread():
    tester = Vector2Tester()
    print(f'Test 01 status: {tester.test01()}')


if __name__ == "__main__":
    main_thread()
