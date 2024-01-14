---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
summary: |-
    Hier kommt die Zusammenfassung hin
draft: false
# Die nächste Zeile anpassen, wenn das Thumbnail eingerichtet ist
# image: thumbnail.jpg
# Wenn ein Blog-beitrag auch eine Terminankündigung sein soll, hier eintragen:
# announcement:
#     date: 2023-11-11
#     # Optional kann man in der Terminerinnerung noch einen Kurztitel vergeben.
#     name: ""
---

Hier kommt der Text

<!-- Das ist ein einzelnes Bild: -->
<!-- {{< tsc/news/inline-float src="pokal.jpg" alt="Siegerpokal" width="800" height="801" >}} -->

