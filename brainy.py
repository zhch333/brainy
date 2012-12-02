#-------------------------------------------------------------------------------
# Name:        brainy
# Purpose:     Triviaquiz
#
# Author:      zhch - mail: zhch333 at gmail dot com
#
# Created:     24.11.2012
# Version No.: proto-3
# Changes:     1 data in list of dictionaries, 2 simpler classes, 3 explicite search and replace in legit_answer()
# History:     proto-2 {1 data in list of lists, 2 changes in legit_answer() by implicte reference}
# Copyright:   (c) zhch333 2012
# Licence:     CC-BY-SA http://creativecommons.org/licenses/by-sa/3.0/ch/
#-------------------------------------------------------------------------------
import csv
import random
import time
import difflib
import math
import sys
import os

os.system("title " + "brainy v.3 - das Quiz von Alex")

# global constants - configuration
Q_QUANTITY = 4      # number of questions per quiz-round - also the number of questions drawn from each set
FUZZY_UPPER = 0.90  # required level of similarity to accept an answer


def load_capitals(file_path_name):
    f = open(file_path_name, "r", newline="", encoding="utf-8")
    # encoding="windows-1252"
    new_read = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
    data = []
    data.extend(new_read)
    f.close()

    one_question = {"category":"","subcategory":"","question":"","answer":"","alternativ":"","hint_1":"","hint_2":"","date_time":"","count_known":"","count":"","cycle":""}
    set_capitals = []

    for data_line in data:
        one_question["category"] = data_line[0]
        one_question["subcategory"] = data_line[1]
        one_question["question"] = data_line[2]
        one_question["answer"] = data_line[3]
        one_question["alternativ"] = data_line[4]
        one_question["hint_1"] = data_line[5]
        one_question["hint_2"] = data_line[6]

        date = data_line[7] #  "(##, ##, ##, ##, ##)" - it's a string at first
        if date != "":
            date = "".join(c for c in date if c not in "()[]\'\"") # unwanted characters removed
            date = date.split(", ") # conversion into list
            one_question["date_time"] = [int(data_line) for data_line in date] # conversion of each element from string to int
        else:
            one_question["date_time"] = 5 * [0]

        one_question["count_known"] = int(data_line[8])
        one_question["count_false"] = int(data_line[9])
        one_question["count"] = int(data_line[10])
        one_question["box"] = int(data_line[11])
        one_question["cycle"] = 0

        set_capitals.append(dict(one_question))

    return set_capitals

def store_capitals(data, file_path_name):
    m_list = [x for x in range(0,13)]
    n_list = []
    for m in data:
        m_list[0] = m["category"]
        m_list[1] = m["subcategory"]
        m_list[2] = m["question"]
        m_list[3] = m["answer"]
        m_list[4] = m["alternativ"]
        m_list[5] = m["hint_1"]
        m_list[6] = m["hint_2"]
        m_list[7] = m["date_time"]
        m_list[8] = m["count_known"]
        m_list[9] = m["count_false"]
        m_list[10] = m["count"]
        m_list[11] = m["box"]
        m_list[12] = m["cycle"]

        n_list.append(list(m_list))

    g = open(file_path_name, "w", newline="", encoding="utf-8")
    new_writer = csv.writer(g, delimiter=",", quoting=csv.QUOTE_ALL)
    for row in n_list:
        new_writer.writerow(row)
    g.close()
    # stupid 'test' wheather or not it wrote somethin
    t = open(file_path_name,"r")
    test = t.read()
    t.close()

    if test != "":
        return True
    else:
        return False

def choose(orig_data):
    global Q_QUANTITY

    if len(orig_data) <  Q_QUANTITY:
        Q_QUANTITY = 3

    # sort out questions used in the preceeding round
    newquestions = []
    for g in orig_data:
        if g["cycle"] < quiz.Q_CYCLE:
            newquestions.append(dict(g))

    # sort questions according to their box-number (low box = needs more repetition)
    newquestions.sort(key = lambda x: x["box"])

    ready_questions = newquestions[0:13]

    # sort according to date and time
    ready_questions.sort(key = lambda x: (x["date_time"][0], x["date_time"][1], x["date_time"][2], x["date_time"][3], x["date_time"][4]))

    desk_c = ready_questions[0:Q_QUANTITY]

    # shuffle choosen questions
    random.shuffle(desk_c)

    return desk_c

def line(num):
    if num == 1:
        print(85 * "=")
    elif num == 2:
        print(85 * "-")

def getinput(line):
    question = line["question"]
    player_answer = ""
    while player_answer == "":
        if line["category"] == "Hauptstadt":
            if line["subcategory"] in ["Schweiz","Österreich","Deutschland"]:
                player_answer = str(input("Nr.%d\t(%s) Wie heisst die Hauptstadt %s?\n\n> " % (e_one.Q_NUMBER, line["subcategory"], question)))
            else:
                player_answer = str(input("Nr.%d\tWie heisst die Hauptstadt %s?\n\n> " % (e_one.Q_NUMBER, question)))

        elif line["category"] == "Konstante":
            player_answer = str(input("Nr.%d\t %s?\n\n>" % (e_one.Q_NUMBER, question)))
        elif line["category"] == "LiteraturAutor":
            player_answer = str(input("Nr.%d\tWer ist der Autor von '%s'?\n\n" % (e_one.Q_NUMBER, question)))
        else:
            print("Fragetyp noch nicht vorhanden!")
            break

        if player_answer == "":
            print("\tLeere Eingabe")
        else:
            return player_answer


# legit answers (non-empty, not !-orders) are here collected and prepared for the answercheck
# the function changes some parameters of the question - to prevent repetition
def legit_answer(player_answer, question_line, start_time):
    print()

    solution = question_line["answer"]
    alt_solution = question_line["alternativ"]
    check = answCheck(str(player_answer), solution, alt_solution, start_time)
    question_line["count"] += 1
    question_line["cycle"] = quiz.Q_CYCLE
    question_line["date_time"] = list(time.localtime()[0:5])

    tipp_nr = e_one.A_TIPP_NR + e_one.T_TIPP_NR
    if check == True and tipp_nr < 1:
        question_line["count_known"] += 1
        if question_line["box"] < 9:
            question_line["box"] += 1
    elif check == True:
        question_line["count_known"] += 1
    else:
        question_line["count_false"] += 1
        question_line["count_known"] -= 1
        question_line["box"] = 0

    # The new changes have to be written explicite into the database
    for one_dict in q_one.c_world:
        if one_dict["question"] == question_line["question"]:
            one_dict.update(question_line)
    for one_dict in q_one.c_deach:
        if one_dict["question"] == question_line["question"]:
            one_dict.update(question_line)
    for one_dict in q_one.c_const:
        if one_dict["question"] == question_line["question"]:
            one_dict.update(question_line)
    for one_dict in q_one.c_litera:
        if one_dict["question"] == question_line["question"]:
            one_dict.update(question_line)


    return True


# fuzzy-comparision of answer and solution with FUZZY_UPPER precision
# award points depending on time and congruence (fuzzy-matching)
def answCheck(p_answer, solution, alt_solution, start_time):
    ein = umlaut(p_answer.lower())
    out = umlaut(solution.lower())
    out_alt = umlaut(alt_solution.lower())

    comp1 = difflib.SequenceMatcher(None, ein, out).ratio()
    if alt_solution != "NULL":
        comp2 = difflib.SequenceMatcher(None, ein, out_alt).ratio()
    else:
        comp2 = 0

    # calculation of points (aka the karmic portioner...)
    # each timelimit gets its rank
    point_range = 0 # diesen Wert könnte von verschiedenen Fragetypen abhängen, um andere Punkteverteilungen bei anderen Fragen zu erreichen
    t_diff = round(time.time() - start_time)

    if  t_diff < 11:
        point_range = 1
    elif t_diff < 20:
        point_range = 2
    elif t_diff < 30:
        point_range = 2


    points = 0.0
    prz = round(comp1 * 100)
    global FUZZY_UPPER

    # correct answer: points depending on rank
    if comp1 == 1 or comp2 == 1:
        if point_range == 1:
            points = 2.0
        elif point_range == 2:
            points = 1.0
        else:
            points = 0.0

        # hypothetical earned points will be divided by two for each calling of "!a"
        points = round(points /2 ** e_one.A_TIPP_NR, 2)
        p_one.PLAYER_POINTS += points
        print("\t%s ist korrekt! (%d sek) +%.2f" % (p_answer.upper(), t_diff, points))
        print("\n")
        return True

    # accepable answers (fuzzy-matched): points depending on rank (but on a lower general level)
    elif (comp1 < 1 and comp1 > FUZZY_UPPER) or (comp2 < 1 and comp2 > FUZZY_UPPER):
        if point_range == 1:
            points = 1.0
        elif point_range == 2:
            points = 0.5
        else:
            points = 0.0

        # hypothetical earned points will be divided by two for each calling of "!a"
        points = round(points /2 ** e_one.A_TIPP_NR, 2)
        p_one.PLAYER_POINTS += points
        print("\tAntwort > %s < wird akzeptiert. (%d %%, %d sek) + %.2f" % (p_answer, prz, t_diff, points))
        if alt_solution != "NULL":
            print("\tKorrekt: %s - alternativ: %s" % (solution, alt_solution))
        else:
            print("\tKorrekt:", solution)
        print("\n")

        return True

    # wrong answers wont get player_points
    else:
        print("\tFalsch (%d %%).\tLösung: %s" % (prz, solution))
        print("\n")

        return False

# replace umlauts and some other characters
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
        if t[i] in ["é", "è"]:
            t[i] = "e"
        if t[i] in ["à","â"]:
            t[i] = "a"

    return "".join(t)

def hint_please(player_answer, question_line):
    answer = question_line["answer"]
    a = e_one.A_TIPP_NR
    t = e_one.T_TIPP_NR
    tipp_nr = e_one.A_TIPP_NR + e_one.T_TIPP_NR + 1

    if player_answer == "!a":
        if a < 2:
            hintable = [x for x in range(len(answer)) if str.isalnum(answer[x])]
            qty = math.ceil(len(hintable) * 3.5/8.0)
            if len(hintable) == 1:
                qty = 0
            while len(hintable) > qty:
                ch = random.randint(0, len(hintable)-1)
                n = hintable[ch]
                answer = answer[:n] + '.' + answer[n+1:]
                del hintable[ch]
            print("\tTipp %d: %s" % (tipp_nr, answer))
            print()
            e_one.A_TIPP_NR += 1
        elif a == 2:
            print("\tKeine weitern Tipps mehr! Letzte Warnung...\n")
            e_one.A_TIPP_NR += 1
        else:
            return True

    elif player_answer == "!t":
        if question_line["hint_1"] == "":
            print("\tKeine Tipps vorhanden (versuche !a)\n")
            e_one.T_TIPP_NR += 1
        elif t == 0:
            print("\tTipp %d: %s" % (tipp_nr, question_line["hint_1"]))
            e_one.T_TIPP_NR += 1
        elif t == 1:
            print("\tTipp %d: %s" % (tipp_nr, question_line["hint_2"]))
            print("\tKeine weiteren Tipps mehr... (versuche !a)\n")
            e_one.T_TIPP_NR += 1
        else:
            return True
    else:
        print("????")

    return False

def reminder():
    line(1)
    print("\tBefehle:")
    line(2)
    print("\t   !r = Die Spielregeln anzeigen\n")
    print("\t   !a = Automatischer Tipp - einige Buchstaben werden aufgedeckt\n\t\tJeder Aufruf halbiert die möglichen Punkte\n")
    print("\t   !t = Hinweise - max 2 pro Frage, oft kein Hinweis vorhanden\n\t\tKostet keine Punkte\n")
    print("\t   !p = Gewonnene Punkte werden angezeigt\n")
    print("\t   !s = Neustart - speichert alle Punkte und startet das\n\t\tProgramm neu\n")
    print("\t   !h = Diese Hilfe nochmals anzeigen\n")
    print("\t   !x = Exit - speichert und verlässt das Programm\n")
    line(1)

def rules():
    global FUZZY_UPPER
    a = round(FUZZY_UPPER * 100, 1)
    line(1)
    print("\tDie Spielregeln:")
    line(2)
    print("\t *  ", 68 * " ", "*")
    print("\t *  1. Eine korrekte Antwort gibt max. +2 Punkte\t\t\t  *")
    print("\t *  2. Eine 'akzeptierte' Antwort gibt max. +1 Punkt\t\t\t  *")
    print("\t *     'akzeptiert': Übereinstimmung von %.1f %% bis 99.5 %%\t\t  *" % (a))
    print("\t *  3. Nach einer gewissen Zeit vermindert sich die Maximalpunktzahl\t  *")
    print("\t *  4. Mit jedem Aufruf von '!a' halbieren sich die möglichen Punkte\t  *")
    print("\t *  ", 68 * " ", "*")
    print("\t *  ", 68 * " ", "*")

    line(1)

def quiz_start():
    line(1)
    print("\tNeues Quiz - neues Glück!")
    line(1)
    reminder()
##    time.sleep(2)
##    for sek in range(3,0,-1):
##        print(5 * "\t", sek)
##        time.sleep(1)
    line(2)
    print("\tRunde Nr. 1")
    line(2)

def select_topics():
    line(1)
    print("\tFragensammlungen:")
    line(2)
    print()
    print("\ta. Hauptstädte der Länder der Welt")
    print("\tb. Hauptstädte der Kantone/ Bundesländer der Schweiz,\n\t   Deutschlands und Österreichs")
    print("\tc. Wichtige Konstanten aus den Naturwissenschaften")
    print("\td. Literatur: Autoren und ihre Werke")
    print()
    print("\tAuswahl durch aneinanderreihen der gewünschten Optionen\n\t(z.B. a, bd oder abcd)")
    line(1)

    proceed = True
    while proceed == True:
        selection = input("Wahl : ")

        if "a" in selection:
            q_one.loadQuestions(1)
            proceed = False
        if "b" in selection:
            q_one.loadQuestions(2)
            proceed = False
        if "c" in selection:
            q_one.loadQuestions(3)
            proceed = False
        if "d" in selection:
            q_one.loadQuestions(4)
            proceed = False

def welcome():
    line(1)
    print("\tWillkommen zu BRAINY - Fehler bitte an Alex melden")
    line(1)
    p_one.p_name = input("Dein Name: ")
    print()

def special_orders(player_answer, question_line, start_time):
    if player_answer == "!t" or player_answer == "!a":
        switch = hint_please(player_answer, question_line)
        if switch == True:
            switch = legit_answer("", question_line, start_time)
        else:
            switch = False
    elif player_answer == "!p":
        line(1)
        print("\t%s hat %d Punkte" % (p_one.p_name, p_one.PLAYER_POINTS))
        line(2)
        print("\tAllzeit-Bestenliste:\n")
        for k, data_line in enumerate(p_one.p_best):
            print("\t",k+1,"\t%s mit %0.2f Punkten in %d Runden (%0.1f sec)" % (data_line["name"], data_line["points"], data_line["q_cycle"], data_line["duration"]))
        line(1)
        switch = False
    elif player_answer == "!h":
        reminder()
        switch = False
    elif player_answer == "!r":
        rules()
        switch = False

    elif player_answer == "!x" or player_answer == "!s":
        p_one.storePoints()
        q_one.storeQuestions()
        if player_answer == "!s":
            quiz.newgame()
        else:
            sys.exit("Byebye!")

    return switch


class Player(object):
    PLAYER_POINTS = 0
    p_name = ""
    p_best = []

    def storePoints(self):
        t_diff = round(time.time() - quiz.Q_TIME,2)
        entry = [self.p_name, (time.localtime()[0:5]), self.PLAYER_POINTS, e_one.Q_NUMBER, quiz.Q_CYCLE, t_diff]
        pnts = str(entry)+"\n"
        h = open("player_points.bry", "a")
        h.write(pnts)
        h.close

    def loadBest(self):
        t = open("player_points.bry", "r")
        new_read = csv.reader(t, delimiter=",", quoting=csv.QUOTE_ALL)
        data = []
        data.extend(new_read)
        t.close()

        one_best = {"name":"","date_time":"","points":"","q_number":"","q_cycle":"","duration":""}
        set_best = []
        date = []

        for line in data:
            one_best["name"] = "".join(c for c in line[0] if c not in "()[]\'\"")
            d_t = "".join(c for c in line[1:5] if c not in "()[]\'\"")
            one_best["date_time"] = d_t[2:]
            one_best["points"] = float(line[6])
            one_best["q_number"] = int(line[7])
            one_best["q_cycle"] = int(line[8])
            dura = "".join(c for c in line[9] if c not in "()[]\'\"")
            one_best["duration"] = float(dura[1:])
            set_best.append(dict(one_best))

        set_best.sort(key = lambda x: -x["points"])
        self.p_best = set_best[0:5]

class Questions(object):
    def __init__(self):
        self.q_register = [0,0,0,0]
        self.q_length = [0,0,0,0]
        self.c_world = []
        self.c_deach = []
        self.c_const = []
        self.c_litera = []
        self.sub_world = []
        self.sub_deach = []
        self.sub_const = []
        self.sub_litera = []
        self.desk = []

    def getQuestions(self):
        if self.q_register[0] == 1:
            self.sub_world = choose(self.c_world)
        if self.q_register[1] == 1:
            self.sub_deach = choose(self.c_deach)
        if self.q_register[2] == 1:
            if self.q_length[2] > 30 or quiz.Q_CYCLE % 3 == 0:
                self.sub_const = choose(self.c_const)
            else:
                self.sub_const = []
        if self.q_register[3] == 1:
            self.sub_litera = choose(self.c_litera)

        if quiz.Q_CYCLE % 3 == 0:
            self.desk = self.sub_world + self.sub_deach + self.sub_litera + self.sub_const
        else:
            self.desk = self.sub_world + self.sub_deach + self.sub_litera

        random.shuffle(self.desk)
        global Q_QUANTITY
        self.desk = self.desk[0:Q_QUANTITY]

        return self.desk

    def loadQuestions(self, selector):
        if selector == 1:
            self.c_world = load_capitals("quest_world.bry")
            random.shuffle(self.c_world)
            self.q_register[0] = 1
            self.q_length[0] = len(self.c_world)
        elif selector == 2:
            self.c_deach = load_capitals("quest_deach.bry")
            random.shuffle(self.c_deach)
            self.q_register[1] = 1
            self.q_length[1] = len(self.c_deach)
        elif selector == 3:
            self.c_const = load_capitals("quest_const.bry")
            random.shuffle(self.c_const)
            self.q_register[2] = 1
            self.q_length[2] = len(self.c_const)
        elif selector == 4:
            self.c_litera = load_capitals("quest_litera.bry")
            random.shuffle(self.c_litera)
            self.q_register[3] = 1
            self.q_length[3] = len(self.c_litera)
        else:
            print("Fehler bei: def loadQuestions() - in class Questions()")

    def storeQuestions(self):
        if q_one.q_register[0] == 1:
            store_capitals(self.c_world, "quest_world.bry")
        if q_one.q_register[1] == 1:
            store_capitals(self.c_deach, "quest_deach.bry")
        if q_one.q_register[2] == 1:
            store_capitals(self.c_const, "quest_const.bry")
        if q_one.q_register[3] == 1:
            store_capitals(self.c_litera, "quest_litera.bry")

class Enquirer(object):
    Q_NUMBER = 0
    T_TIPP_NR = 0
    A_TIPP_NR = 0
    START_T = 0

    def ask(self):
        question_desk = q_one.getQuestions()

        for question_line in question_desk:
            self.START_T = time.time()
            self.Q_NUMBER += 1
            self.T_TIPP_NR = 0
            self.A_TIPP_NR = 0

            switch = False
            while switch == False:
                player_answer = getinput(question_line)

                if player_answer in ["!t","!a","!h","!p","!s","!r","!x"]:
                    switch = special_orders(player_answer, question_line, self.START_T)

                else:
                    switch = legit_answer(player_answer, question_line, self.START_T)

class Quiz(object):
    Q_CYCLE = 0
    Q_TIME = time.time()
    proceed = True

    def first(self):
        welcome()
        select_topics()
        quiz_start()
        p_one.loadBest()

    def start(self):
        if self.Q_CYCLE == 0:
            self.Q_CYCLE = 1
            self.first()
            e_one.ask()

        while self.proceed:
            self.Q_CYCLE += 1
            line(2)
            print("\tRunde Nr. %d - %d Punkte" % (self.Q_CYCLE, p_one.PLAYER_POINTS))
            line(2)
            print()

            e_one.ask()
            q_one.storeQuestions()

    def newgame(self):
        print("Neustart...")
        time.sleep(2)
        python = sys.executable
        os.execl(python, python, * sys.argv)


quiz = Quiz()
p_one = Player()
e_one = Enquirer()
q_one = Questions()

quiz.start()
