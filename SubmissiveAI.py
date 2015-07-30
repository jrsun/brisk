import Brisk
import time

POLL_TIME = 0.5 # seconds

class SubmissiveAI(Brisk.Brisk):
    
    def __init__(self):
        super(SubmissiveAI, self).__init__()
        print self.game_id

    def main(self):
        while True:
            while self.get_player_status(True)['current_turn'] is False:
                time.sleep(POLL_TIME)
            self.do_reinforce()
            self.do_attack()
            self.do_fortify() or self.end_turn()

    def do_reinforce(self):
        return False

    def do_attack(self):
        return False

    def do_fortify(self):
        return False

if __name__ == "__main__":
    s = SubmissiveAI()
    s.main()
