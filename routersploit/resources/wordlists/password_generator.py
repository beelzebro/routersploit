class PasswordGenerator:
    CHARS_COUNT = 76
    characters = "eaorinsl1t2mdcy0bhgup3k945768fjwvzxSEARMTBNOLICDPHJqKGYUFWV!X@Z*.#&Q−_$/?';[+"

    length = 0

    counter = 0

    next_pos = 0

    times_called = 0

    passwords = []

    next_password = []

    def __init__(self, length):
        self.length = length
        for i in range(length):
            self.next_password.append(0)

    def new_passwords(self):
        self.passwords = []
        self.counter = 0
        if self.times_called == 0:
            self.append_password()
            self.times_called += 1

        self.next_pos = self.iterate_through_passwords(self.next_pos)

        while not self.every_pos_is_max() and self.next_pos != -1 and self.counter < 8:
            self.next_pos = self.iterate_through_passwords(self.next_pos)
        else:
            if self.counter == 8:
                return self.passwords
            else:
                return False

    def append_password(self):
        actual_password = ""
        for char in self.next_password:
            actual_password += self.characters[char]

        self.passwords.append(actual_password)
        print(actual_password)
        self.counter += 1

    def every_pos_is_max(self):
        for char in self.next_password:
            if char < self.CHARS_COUNT:
                return False

        return True

    def first_not_max_char_after_pos(self, pos):
        for i in range(pos + 1, self.length):
            if self.next_password[i] < self.CHARS_COUNT:
                return i

        return 0

    def reset_positions(self, start):
        for i in range(start, self.length):
            self.next_password[i] = 0

    def iterate_through_passwords(self, pos):
        first_not_max_char = self.first_not_max_char_after_pos(pos)

        if pos == (self.length - 1):
            self.next_password[pos] += 1
            self.append_password()
            return pos - 1
        elif first_not_max_char == 0 and self.next_password[pos] == self.CHARS_COUNT:
            return pos - 1
        elif first_not_max_char == 0 and pos == 0:
            self.next_password[pos] += 1
            self.reset_positions(pos + 1)
            self.append_password()
            return pos + 1
        elif first_not_max_char == 0:
            self.next_password[pos] += 1
            self.reset_positions(pos + 1)
            self.append_password()
            return pos - 1

        if not self.every_pos_is_max():
            return pos + 1

        return -1
