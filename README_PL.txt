Aplikacja służy do sterowania SmartTV marki Panasonic w sieci lokalnej oraz do kontrolowania jasności i kontrastu monitora obsługującego technologię DDC-CI.
Należy upewnić się, że w monitorze włączona jest obsługa DDC-CI.
Do sterowania jasnością wbudowanego wyświetlacza służy biblioteka screen-brightness-control (https://pypi.org/project/screen-brightness-control/) nie zastosowana tutaj.


Zastosowane biblioteki Python poza biblioteką standardową:

	Flask		https://pypi.org/project/Flask/
	monitorcontrol 	https://pypi.org/project/monitorcontrol/
	panasonic-viera https://pypi.org/project/panasonic-viera/
	tinytuya	https://pypi.org/project/tinytuya/

Podstrony:

	/remote - służy do sterowania telewizorem. Na tej podstronie znajduje się obraz oryginalnego pilota Panasonic, a kliknięcie w poszczególny przycisk na obrazku wywołuje tą funkcję na telewizorze.
	Pozostałe podstrony dla podstrony /remote służą jedynie do wykonania danej czynności, a następnie przekierowaniu do podstrony /remote.

	/display - Służy do sterowania kontrastem, janością wyświetlacza jak również włączenia, wyłączenia i zmiany wyjścia wyświetlacza.
	Wybór wyjść to jedynie VGA (D-Sub) oraz DVI, lecz biblioteka nie ogranicza się jedynie do tych wyjść.
	Monitor musi obługiwać standard DDC-CI oraz w ustawieniach monitora powinna taka opcja został włączona by móc korzystać z tej funkcji.
	Podstrony /display:
		/nightmode - zmiana jasności na 0% oraz kontrastu na 50%, a następnie przekierowanie na podstronę /display
		/normal - zmiana jasności na 100% oraz kontrastu na 50%, a następnie przekierowanie na podstronę /display
		/screen_on - włączenie wyświetlacza
		/screen_off - wyłączenie wyświetlacza. Może spowodować pojawienie się błędów w konsoli oraz wyświetlenie błędu Internal Server error w przeglądarce internetowej.
		/vga - zmiana wyjścia wyświetlacza na VGA (D-Sub)
		/dvi - zmiana wyjścia wyświetlacza na DVI
		
	/tv_status - NIE UŻYWAĆ! Biblioteka sama w sobie nie zawiera komend pozwalających na wysłanie zapytania do telewizora czy jest on włączony czy w stanie spoczynku.
	W celu sprawdzenia stanu telewizora wywoływana jest funkcja w zależności od ustawionego aktualnie poziomu głośności; a jest nią "zwiększ głośność" lub "zmniejsz głośność" i sprawdzenie stanu przez i po wykonaniu tej funkcji.
	Podczas sprawdzania stanu telewizora na wyświetlaczu telewizora wyświetli się pasek głośności.
	Telewizor w trybie spoczynku nie reaguje na komendę zwiększenia/zmniejszenia głośności i wartość ta nie zmieni się.

	/outlet_status - Wyświetla na ekranie stan inteligentnego gniazdka (ON lub OFF)
	/outlet_toggle - zmienia stan gniazdka z włączonego na wyłączony i odwrotnie jak również wyświetla na ekranie stosowną informację ON->OFF lub OFF->ON

	/chiaki - służy do wygenerowania nazwy użytkownika zakodowanej w base64 potrzebnej w programie Chiaki (alternatywa dla programu PS Remote Play).
		Program (zarówno Chiaki) jak i PS Remote Play służy do gry zdalnej na konsoli Playstation 4 i Playstation 5 zarówno w sieci lokalnej jak i sieci Internet.
	

Znane błędy:
	- Po wyłączeniu wyświetlacza strona wyświetla błąd Internal Server Error zaś w konsoli wyświetlają się błędy.
	- W przypadku gdy którakolwiek z bibliotek napotka problem mogą pojawić się błędy w konsoli oraz wyświetić się błąd "Internal Server Error" w przeglądarce internetowej.
	Należało dodać obsługę wyjątków.


Zasada działania:
	Aplikacja do poprawnego działania wymaga interpretera Python oraz bibliotek Flask, monitorcontrol, panasonic-viera oraz tinytuya.
	W sieci lokalnej zostały przypisane adresy IP do telewizora (192.168.0.7) oraz inteligentnego gniazdka (192.168.0.12).
	Dzięki aplikacji możliwe jest sterowanie telewizorem marki Panasonic, gniazdkiem inteligentnym oraz wyświetlaczem komputera.
	Aby mieć dostęp do zasobów aplikacji spoza sieci lokalnej należy posiadać zewnętrzny numer IP oraz przekierować stosowne porty.