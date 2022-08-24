"""A command-line interface version of the classic game IQ Tester"""

if __name__ == "__main__":
    from session import Session


    s = Session()
    s.header()
    s.instructions()
    keep_playing = True
    while keep_playing:
        keep_playing = s.main_menu()
