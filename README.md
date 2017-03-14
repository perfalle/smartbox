# smartbox
Moderne IT-Lösungen kommen heutzutage oft ohne Cloud nicht mehr aus.
Das bringt ja auch viele Vorteile wie Plattformunabhängigkeit von webbasierten Diensten und der ständigen Verfügbarkeit der eigenen Daten.

Dass man bei der Nutzung von Google- Facebook- oder Amazon-Diensten die Nutzungsrechte der eigenen Daten abtritt und zulässt, dass persönliche Informationen auf US-Servern verarbeitet werden, wird dabei einfach in Kauf genommen.

Einen Grund dafür könnte darin liegen, dass es so einfach ist diese Dienste zu nutzen.
Dabei gibt es etliche Projekte die diese Dienste unter die eigene Kontrolle bringen könnten:
* Owncloud für den Datenaustausch und den Onlinekalender
* Ein XMPP Server als ersatz für einen zentralisierten Instant Messenger
* Ein Mediaserver statt (oder zusätzlich zu) Netflix oder Spotify
* Ein Gnusocial oder Diaspora Pod für die eigene Familie/Freunde

Allen gemeinsam: Man muss einen Server mit diesen Diensten aufsetzen und administrieren.
Das ist zwar kein Hexenwerk, dennoch für den Nicht-Nerd nicht zumutbar.

Smartbox ist ein Versuch einen bewusst klein gehaltenen Anwendungsfall so einfach zu abstrahieren, dass keine IT-Kenntnisse nötig sind um es zu benutzen. Mit smartbox soll es möglich sein Dienste, wie die oben genannten zu installieren, ohne sich über weitere Konfiguration oder gegenseitige Störung mehrerer Dienste auf einem Server Gedanken machen zu müssen.

Der kleine Anwendungsfall bezieht sich in erster Linie auf die Skalierbarkeit von Diensten. Während es beim Einsatz von Containern im kommerziellen Bereich oft darum geht einen Dienst auf mehrere Rechner oder Rechenzentren zu verteilen und um diverse Probleme die das mitsich zieht, wird ein Dienst auf der Smartbox immer nur auf einem physikalischen Gerät laufen.

Dennoch sollen Funktionen wie das automatische Einrichten eines dynDNS oder zeroconf Hostnames, das automatisierte Beziehen eines SSL Zertifikats (z.B: LetsEncrypt) sowie Backup-Strategien durch ein paar Klicks in der Weboberfläche möglich sein.

Um das zu realisieren setzt smartbox auf die Container-Engine rkt, mit der es möglich ist sowohl appc images als auch docker images auszuführen.
