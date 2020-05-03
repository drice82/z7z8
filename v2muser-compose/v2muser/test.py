#!/usr/bin/python3

import time

def main():
    while True:
        print(time.asctime(time.localtime(time.time())))
        time.sleep(300)


if __name__ == "__main__":
    main()

