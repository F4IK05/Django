import random

class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def colored_name(self):
        return f"{Color.BLUE}{self.name}{Color.RESET}"

    def attack(self, other):
        if not self:
            return f" - {self.colored_name()} is dead and cannot attack!"

        damage = random.randint(0, self.attack_power)

        return f" - {self.colored_name()} attacks!\n" + other.take_damage(damage)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return f" - {self.colored_name()} takes {Color.RED}{damage} damage{Color.RESET}! {self.colored_name()} has {Color.GREEN}{self.health} health{Color.RESET} left."
    
    def info(self):
        return f" - {self.colored_name()}: Health = {self.health}, Attack Power = {self.attack_power}"
    
    def __str__(self):
        return f" - {self.colored_name()} (HP: {self.health}, ATK: {self.attack_power})"
    
    def __add__(self, other):
        if isinstance(other, Character):
            return Team(self, other)
        elif isinstance(other, Team):
            return Team(self, *other.members)

        return NotImplemented

    def __lt__(self, other):
        return (self.health + self.attack_power) < (other.health + other.attack_power)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self.name == other.name and self.health == other.health and self.attack_power == other.attack_power
    
    def __len__(self):
        return self.health
    
    def __bool__(self):
        return self.health > 0
    

class Team:
    def __init__(self, *members):
        self.members = list(members)

    def attack(self, other_team):
        result = ""

        for attacker in self.members:
            if not attacker:
                continue

            alive_enemies = [e for e in other_team.members if e]
            if not alive_enemies:
                result += " - All enemies are dead!\n"
                break

            enemy = random.choice(alive_enemies)
            result += attacker.attack(enemy) + "\n"

        return result
    
    def __str__(self):
        return " - Team:\n" + "\n".join([member.name for member in self.members])


class Warrior(Character):
    def attack(self, other):
        if not self:
            return f" - {self.colored_name()} is {Color.RED}dead{Color.RESET}!"

        damage = random.randint(0, self.attack_power)

        if random.random() < 0.3:  # особенность: крит. удар
            damage *= 2
            return f" - {Color.RED}CRITICAL HIT!{Color.RESET} {self.colored_name()} deals {Color.RED}{damage} damage{Color.RESET}!\n" + other.take_damage(damage)
        
        return f" - {self.colored_name()} hits for {Color.RED}{damage} damage{Color.RESET}!\n" + other.take_damage(damage)
    

class Mage(Character):
    def attack(self, other):
        if not self:
            return f" - {self.colored_name()} is {Color.RED}dead{Color.RESET}!"

        damage = random.randint(self.attack_power // 2, self.attack_power * 2)  # особенность: большой, но нестабильный урон

        return f" - {self.colored_name()} casts a spell for {Color.RED}{damage} damage{Color.RESET}!\n" + other.take_damage(damage)


class Archer(Character):
    def attack(self, other):
        if not self:
            return f" - {self.colored_name()} is dead!"

        damage1 = random.randint(0, self.attack_power)
        
        if random.random() < 0.5:  # особенность: шанс второго выстрела
            damage2 = random.randint(0, self.attack_power)

            return f" - DOUBLE SHOT! {self.colored_name()} hits for {Color.RED}{damage1}{Color.RESET} and {Color.RED}{damage2} damage{Color.RESET}!\n" + other.take_damage(damage1 + damage2)

        return f" - {self.colored_name()} shoots for {Color.RED}{damage1} damage{Color.RESET}!\n" + other.take_damage(damage1)


class Game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def is_team_alive(self, team):
        return any(member for member in team.members)

    def play(self):
        round_num = 1

        while self.is_team_alive(self.team1) and self.is_team_alive(self.team2):
            print(f"\n--- Round {round_num} ---")

            print("  Team 1 attacks: ")
            print(self.team1.attack(self.team2))

            if not self.is_team_alive(self.team2):
                break

            print("  Team 2 attacks: ")
            print(self.team2.attack(self.team1))

            round_num += 1

        self.show_winner()

    def show_winner(self):
        if self.is_team_alive(self.team1):
            print("Team 1 wins!")
        else:
            print("Team 2 wins!")


w1 = Warrior("Thor", 100, 20)
m1 = Mage("Gandalf", 80, 25)

a1 = Archer("Legolas", 90, 15)
w2 = Warrior("Conan", 110, 18)

team1 = w1 + m1
team2 = a1 + w2

game = Game(team1, team2)

game.play()