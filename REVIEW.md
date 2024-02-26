# Peer Review [Dashbuddy](https://github.com/CakeOfPain/dashbuddy)

Refernce Commit ID: [b2069b222897f848422aeefe3be303fcd791e6bd](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd)

## Kritik

- [Fehlerhaftes Typing](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/pluginManager.py#L12)
- [Rechtschreibung teilweise sehr verwirrend](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/plugins/kalender.py)
- Mischung von Deutsch und Englisch (gesamtes Projekt)
- Leerzeichen in Dateinamen (Wetterausgabe Test.py)
- Teilweise [Logging](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/plugins/timetable.py#L12-L13) (Sehr schön) und teilweise dann doch [`print`](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/pluginManager.py#L53-L57)
- `Docs` Ordner ist etwas verwirrend (vielleicht im README.md erklären)
- Code Formatting mit `black` / `ruff` für python, `prettier` für HTML, JS, CSS wäre schön gewesen
- Unused import [`datetime.date`](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/plugins/kalender.py#L1)

## Lob

- Gute Strukturierung des Projekts
- Auch ohne Doku und Kommentare relativ gut verständlich
- [Exception Handling](https://github.com/CakeOfPain/Dashbuddy/tree/b2069b222897f848422aeefe3be303fcd791e6bd/pluginManager.py#L53-L57)
- Verständliche Fehlernachrichten ↑
- Nutzung von verschieden Datentypen, unbekannten Modulen (API, xml, ...)
- Durchdachtes Projektmanagement
- Tolles README.md (Lisp is great) 🤣
- Verwendung von verschieden Operatoren, Kontrollstrukturen, Funktionen, Strukturen, ...

## Grading Criteria für die Gruppe

### Fachkompetenz (siehe [Grading Criteria](https://github.com/CakeOfPain/Dashbuddy/blob/main/grading-criteria.md) für Details)

- [x] Verwendung von verschiedenen Datentypen
- [x] E-/A-Operationen und Dateiverarbeitung
- [x] Operatoren
- [x] Kontrollstrukturen
- [x] Funktionen
- [x] Stringverarbeitung
- [x] Strukturierte Datentypen
