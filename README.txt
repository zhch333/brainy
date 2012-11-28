Readme - brainy
    von zhch333

1. Was ist brainy?
2. Wie kann das Programm gestartet werden?
3. Weitere Pläne für brainy?
4. Ist brainy freie Software?
5. Welche Werkzeuge wurden zur Programmierung benutzt?


1. Was ist brainy?

    Brainy ist ein Triviaquiz. Es stellt Fragen aus verschiedenen Datenbankfiles
    (noch nicht direkt beigelegt: Siehe Download) und wertet die Antworten aus.
    Jeder Antwort wird ein Punktwert vergeben - je nach benötigter Zeit und nach
    Mass der Übereinstimmung von Antwort und Lösung (es ist ein Vergleich implementiert,
    der auch eine gewisse Unschärfe zulässt [Prozentual... also in Abhängigkeit der
    Wortlänge]).
    Inspiriert ist brainy durch Quizbots aus den IRC-Channels - Steuerbefehle lassen
    das erahnen (!a, !h, !t, etc.).

    Brainy dient hauptsächlich als kleines Hobbyprojekt und dokumentiert die
    Programmierversuche des Autors.


2. Wie kann brainy gestartet werden?

    Brainy ist in Python 3.3 geschrieben - in Windows-Systemen ist diese
    Programmiersprache nicht unbedingt vorhanden. Man kann sie aber problemlos (und
    gratis) aus dem Netz beziehen und installieren (keine weiteren Kenntnisse nötig).
    Offizieller Download hier: http://www.python.org/download/releases/3.3.0/

    Um Brainy spielen zu können braucht es Fragesammlungen. Momentan sind diese
    "hart" implementiert, d.h. die Dateinamen sind fix im Code eingebettet (die
    Dateipfade aber relativ zum Programm). Auch das Format der Fragen ist "Marke
    Eigenbau".
    Drei Datenbanken finden sich aber im 7z-Archiv (http://www.7-zip.org/) im
    Downloadbereich. Wenn man diese 1. herunterlädt, 2. entpackt und 3. ein Ordner
    ÜBER brainy.py speichert, dann ist brainy versuchsweise zu spielen!

    Baumdiagramm zur Illustration der benötigten Anordnung:
     
                     |-brainy.py
     |-Frage-Dateien-|
    -|


3. Weitere Pläne für brainy

    a) Neue Fragen (Vorhanden: Hauptstädte alle Länder der Welt & Hauptstädte der
       Kantone & Bundesländer der Schweiz, Österreichs und Deutschlands).
    b) Verbessertes Konzept & System zur Repetition (Karteikasten).
    c) Wechsel zur Speicherung in XML (ist doch einfacher als zuerst gedacht...).
    d) Möglichkeit eigenen Fragesammlungen zu integrieren.
    e) Evt. ganz basales GUI (easygui).


4. Ist brainy freie Software?

    Ja!
    Die Lizenz ist CC-BY-SA, http://creativecommons.org/licenses/by-sa/3.0/ch/


5. Welche Werkzeuge wurden zur Programmierung benutzt?

    Brainy habe ich mit dem Editor Pyscripter geschrieben. http://code.google.com/p/pyscripter/
    Zunehmend habe ich aber auch Gefallen an Notepad++ gefunden. http://notepad-plus-plus.org/
