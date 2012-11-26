from os import system
system("title " + "brainy - das Quiz von Alex")
import random
import difflib
import math
import time
import sys
import csv

FUZZY_UPPER = 0.94

def line(num):
    if num == 1:
        print(85 * "=")
    elif num == 2:
        print(85 * "-")

def help():
    line(1)
    print("\tBefehle:")
    line(2)
    print("\t   !a = Automatischer Tipp - einige Buchstaben werden aufgedeckt\n\t   Jeder Aufruf halbiert die möglichen Punkte")
    print("\t   !t = Hinweise - max 2 pro Frage, oft kein Hinweis vorhanden\n\t   Kostet keine Punkte")
    print("\t   !p = Gewonnene Punkte werden angezeigt\n")
    print("\t   !h = Diese Hilfe nochmals anzeigen\n")
    print("\t   !x = Exit - speichert und verlässt das Spiel\n")
    line(1)

def dataHS():
    f = open("questionsHS.csv", "r", encoding="windows-1252")
    new_red = csv.reader(f, delimiter=";", quoting=csv.QUOTE_ALL)
    data = []
    data.extend(new_red)
    f.close()

    setHS = []
    for i in data:
        tuple_complete = False
        kategorie = i[0]
        date = i[1] #  "(##, ##, ##, ##, ##)" - ein String
        if date != "":
            date = "".join(c for c in date if c not in "()[]\'\"") # unerwünschte Zeichen werden entfernt
            date = date.split(", ") # Konversion zur Liste
            date = [int(i) for i in date] # Konversion der Elemente von String zu Int
        else:
            date = 5 * [0]
        count_total = int(i[2])
        question = i[3]
        answer = i[4]
        alternativ = i[5]
        tipp1 = i[6]
        tipp2 = i[7]
        count = int(i[8])
        cycle = 0
        tuple_complete = True

        if tuple_complete:
           tuple = [kategorie, date, count_total, question, answer, alternativ, tipp1, tipp2, count, cycle]
           setHS.append(tuple)
    return setHS

def storeHS(data, m=False):
    g = open("questionsHS.csv", "w", newline="", encoding="windows-1252")
    neuwriter = csv.writer(g, delimiter=";", quoting=csv.QUOTE_ALL)
    for row in data:
        neuwriter.writerow(row)
    g.close()
    t = open("questionsHS.csv","r")
    test = t.read()
    t.close()
    if test != "":
        return True
    else:
        return False

def choose(orig, number):
    # Eben gerade gespielte Fragen werden aussortiert
    orig.sort(key = lambda x: -x[8])
    l = len(orig)
    ready = []
    for g in orig: # Kritische Stelle
        if g[8] < 1:
            ready += [g]
    for h in range(len(ready),l):
        if orig[h][8] > 0:
            orig[h][8] -= 1

    # Selten gestellte Fragen bekommen hohe Priorität - Häufige werden nach Hinten sortiert
    # Die gewünschte Anzahl Fragen wird abgetrennt
    ready.sort(key = lambda x: x[2])
    ready = ready[0:25]

    # Nach Datum und Zeit geordnete Vorauswahl
    ready.sort(key = lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4]))
    k = ready[0:number]

    # Die ausgewählten Fragen werden gemischt
    random.shuffle(k)
    return k

# Ersetzt die Umlaute und Punkte in Antworten und Lösungen
def umlaut(text):
    t = list(text.lower())
    for i in range(0,len(text)):
        if t[i] == "ä":
            t[i] = "ae"
        if t[i] == "ö":
            t[i] = "oe"
        if t[i] == "ü":
            t[i] = "ue"
##        if t[i] == ".":
##            t[i] = ""
        if t[i] == "é":
            t[i] = "e"

    return "".join(t)

# Fuzzy Vergleich der Antwort mit der Lösung - bei FUZZY_UPPER Übereinstimmung o.K.
def answCheck(user, data, alt):
    a1 = user
    l1 = data
    aU = a1.lower()
    a2 = umlaut(aU)
    lU = l1.lower()
    l2 = umlaut(lU)
    alt2 = umlaut(alt.lower())

    comp1 = difflib.SequenceMatcher(None, a2, l2).ratio()
    if alt != "NULL":
        comp2 = difflib.SequenceMatcher(None, a2, alt2).ratio()
    else:
        comp2 = 0

    p_range = 0
    td = zt.get_diff()
    if  td < 11:
        p_range = 1
    elif td < 20:
        p_range = 2
    elif td < 30:
        p_range = 2
    points = 0
    prz = round(comp1 * 100)

    if comp1 == 1 or comp2 == 1:
        if p_range == 1:
            points = 2
        elif p_range == 2:
            points = 1
        else:
            points = 0

        print("\t", aU.upper(), "ist korrekt! (", zt.get_diff(), "sek) +", points)
        moi.addPoints(2)
        print("\n\n")
        return "alpha"

    elif comp1 < 1 and comp1 > FUZZY_UPPER:
        if p_range == 1:
            points = 1
        elif p_range == 2:
            points = 0.5
        else:
            points = 0
        print("\tAntwort", a1, "wird akzeptiert (", prz, "%) +", points)
        if alt != "NULL":
            print("\tKorrekt:", l1, ", Alternativ:", alt)
        else:
            print("\tKorrekt:", l1)
        print("\n\n")
        return "beta"

    elif comp2 < 1 and comp2 > FUZZY_UPPER:
        if p_range == 1:
            points = 1
        elif p_range == 2:
            points = 0.5
        else:
            points = 0
        print("\tAntwort", a1, "wird akzeptiert (", prz, "%) +", points)
        print("\tKorrekt:", alt, ", Alternativ:", l1)
        print("\n\n")
        return "beta"
    else:
        print("\tFalsch (", prz, "%) Lösung:", l1, "\n")
        print("\n\n")
        return "gamma"


def inputCheck(i):
    a = neu.quest_number
    b = i[3]
    answ = ""
    while answ == "":
        answ = str(input("Nr.%d\tWie heisst die Hauptstadt %s?\n\n> " % (a, b)))
        if answ == "":
            print("\tLeere Eingabe")
        else:
            return answ

def legitAnswer(answ, line, q_cycle):
    print()
    solution = line[4]
    alternativ = line[5]
    check = answCheck(answ, solution, alternativ)
    line[8] += 1
    line[9] = q_cycle
    line[1] = list(time.localtime()[0:5])
    if check == "alpha" or check == "beta":
        line[2] += 1

    return check

def tippMan(tippNR, line):
    if tippNR < 2:
        print("\tTipp", tippNR + 1, ": ", line[6+tippNR])
        return tippNR + 1
    else:
        print("\tKeine weiteren Tipps mehr... (versuche !a)")
        return tippNR + 1

def tippGeber(ans): # Der tippGeber wurde von Quizclown übernommen
	hintable = [x for x in range(len(ans)) if str.isalnum(ans[x])]

	qty = math.ceil(len(hintable) * 3.5/8.0)

	if len(hintable) == 1:
		qty = 0

	while len(hintable) > qty:
		ch = random.randint(0, len(hintable)-1)
		n = hintable[ch]
		ans = ans[:n] + '.' + ans[n+1:]
		del hintable[ch]

	print("\t" + ans)

class Player(object):
    def __init__(self, points=0):
        self.points = points
    def addPoints(self, points):
        self.points += points
    def getPoints(self):
        return self.points
    def storePoints(self):
        pnts = str(self.points)+"\n"
        h = open("player_points.csv", "a")
        h.write(pnts)
        h.close

class Time_Tipp(object):
    def __init__(self, answer="", s_quest=time.time()):
        self.s_quest = s_quest
        self.answer = answer
    def set_s_quest(self):
        self.s_quest = time.time()
    def get_diff(self):
        diff = round(time.time() - self.s_quest)
        return diff
    def tippAuto(self, tippNR, answer):
        if tippNR < 5:
            tippGeber(answer)
            return tippNR + 1
        else:
            print("\tKeine weiteren Tipps mehr...")
            return tippNR + 1


class Q_Capitals(object):
    def __init__(self, desk=[]):
        self.capitals = dataHS()
        self.desk = desk
    def getCapitals(self):
        return self.capitals
    def storeCapitals(self):
        if storeHS(self.capitals) == True:
            return True
        else:
            return False
    def deskCapitals(self, quantity):
        if len(self.capitals) > quantity:
            self.desk = choose(self.capitals, quantity)
            return self.desk
        else:
            self.desk = choose(self.capitals, quantity)
            return self.desk
    def askCapitals(self, quantity, q_cycle):
        question = self.deskCapitals(quantity)
        for line in question:
            zt.set_s_quest()
            neu.quest_number += 1
            check = "delta"
            tippNR = 0
            while check == "delta":
                answ = inputCheck(line)
                if answ == "!t":
                    tippNR = tippMan(tippNR, line)
                    check = "delta"
                elif answ == "!p":
                    print("\tPunkte: ", moi.getPoints())
                    check = "delta"
                elif answ == "!a":
                    tippNR = zt.tippAuto(tippNR, line[4])
                    if tippNR == 7:
                        check = legitAnswer("", line, q_cycle)
                elif answ == "!h":
                    help()
                    check = "delta"
                elif answ == "!x":
                    if cap.storeCapitals() == True:
                        moi.storePoints()
                        print("\tGespeichert!")
                    else:
                        print("????")
                    sys.exit("Byebye!")
                else:
                    check = legitAnswer(answ, line, q_cycle)


class Quiz(object):
    def __init__(self, proceed=True, quiz_cycle=0, quest_number=0):
        self.proceed = proceed
        self.quiz_cycle = quiz_cycle
        self.quest_number = quest_number
        self.std_size = 3
        self.cycle_size = 2
    def startQuiz(self):
        if cap.capitals == []:
            sys.exit("Error: Hauptstadt DB ist leer!")
        while self.proceed == True:
            line(2)
            print("\tFragerunde Nr.", self.quiz_cycle+1)
            line(2)
            print()
            cap.askCapitals(self.std_size, self.quiz_cycle)
            self.quiz_cycle += 1
            if self.quiz_cycle % self.cycle_size == 0:
                line(1)
                print("\tPunkte-Zwischenstand: ", moi.getPoints())
                line(1)
                cap.storeCapitals()
        else:
            if cap.storeCapitals() == False:
                print("\tSpeicherfehler...")
            print("Byebye!")

neu = Quiz()
cap = Q_Capitals()
zt = Time_Tipp()
moi = Player()
line(1)
print("\tNeues Quiz - neues Glück!")
help()


neu.startQuiz()

