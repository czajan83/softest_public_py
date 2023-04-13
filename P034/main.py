from datetime import datetime
from cv2_actions import actions


def main():
    print(datetime.now())
    actions.test_bad_pixels()
    print(datetime.now())
    actions.wait_for_cv2_windows()


if __name__ == "__main__":
    main()
