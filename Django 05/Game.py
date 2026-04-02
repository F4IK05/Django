import random

class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other):
        damage = random.randint(0, self.attack_power)
        other.take_damage(damage)

        return f"{self.name} attacks {other.name} for {damage} damage! {other.name} has {other.health} health left."
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return f"{self.name} takes {damage} damage! {self.name} has {self.health} health left."
    
    def info(self):
        return f"{self.name}: Health = {self.health}, Attack Power = {self.attack_power}"
    
    def __str__(self):
        return f"{self.name} (HP: {self.health}, ATK: {self.attack_power})"
    
    def __add__(self, other):
        return Team(self, other)
    
    def __lt__(self, other):
        return self.attack_power < other.attack_power

    def __eq__(self, other):
        return (self.name == other.name and self.health == other.health and self.attack_power == other.attack_power)
    
    def __len__(self):
        return self.health
    
    def __bool__(self):
        return self.health > 0
    

class Team:
    def __init__(self, *members):
        self.members = list(members)

    def attack(self, other_team):
        result = ""

        for i in range(len(self.members)):
            attacker = self.members[i]

            if not attacker:
                continue

            for enemy in other_team.members:
                if enemy:
                    result += attacker.attack(enemy) + "\n"
                    break

        return result
    
    def __str__(self):
        return "Team:\n" + "\n".join([member.name for member in self.members])


class Warrior(Character):
    def attack(self, other):
        damage = random.randint(0, self.attack_power)

        if random.random() < 0.3:  # особенность: крит. удар
            damage *= 2
            return f"CRITICAL HIT! {self.name} deals {damage} damage!\n" + other.take_damage(damage)
        
        return f"{self.name} hits for {damage} damage!\n" + other.take_damage(damage)
    

class Mage(Character):
    def attack(self, other):
        damage = random.randint(self.attack_power // 2, self.attack_power * 2)  # особенность: большой, но нестабильный урон

        return f"{self.name} casts a spell for {damage} damage!\n" + other.take_damage(damage)
    
class Archer(Character):
    def attack(self, other):
        damage1 = random.randint(0, self.attack_power)
        
        if random.random() < 0.5:  # особенность: шанс второго выстрела
            damage2 = random.randint(0, self.attack_power)

            return f"DOUBLE SHOT! {self.name} hits for {damage1} and {damage2} damage!\n" + other.take_damage(damage1 + damage2)

        return f"{self.name} shoots for {damage1} damage!\n" + other.take_damage(damage1)
