# Dokumentacja 

## Wprowadzenie
Nasz projekt to API oparte na Flask do przesyłania, szyfrowania, pobierania i deszyfrowania plików. Wykorzystuje framework Flask do obsługi żądań HTTP oraz bibliotekę cryptography do szyfrowania i deszyfrowania plików przy użyciu algorytmu szyfrowania klucza symetrycznego Fernet.

### Konfiguracja i instalacja
Wymagania:
Python 3.6 lub nowszy
Flask
cryptography
Postman (do sprawdzania endpointów API korzystaliśmy właśnie z Postmana)


Dokumentacja dla API szyfrowania i deszyfrowania plików w Flask
Wprowadzenie
Projekt to API oparte na Flask do przesyłania, szyfrowania, pobierania i deszyfrowania plików. Wykorzystuje framework Flask do obsługi żądań HTTP oraz bibliotekę cryptography do szyfrowania i deszyfrowania plików przy użyciu algorytmu szyfrowania klucza symetrycznego Fernet.

Konfiguracja i instalacja
Wymagania wstępne
Python 3.6 lub nowszy
Flask
cryptography

## Endpointy API
### 1. Przesłanie pliku /upload (POST)
Endpoint: /upload
Metoda: POST
Parametry: file (multipart/form-data)
Wynik: pomyślna odpowiedź - JSON z komunikatem o sukcesie lub odpowiedź błędu - JSON z komunikatem o błędzie i kodem statusu

### 2. Pobranie Pliku /download/<nazwa-pliku> (GET)
Endpoint: /download/<nazwa-pliku>
Metoda: GET
Parametr: nazwa-pliku (string)
Wynik: pomyślna odpowiedź - pobranie pliku odszyfrowanego pliku lub dpowiedź błędu - JSON z komunikatem o błędzie i kodem statusu

## Szyfrowanie i deszyfrowanie plików
Pliki przesyłane na serwer są szyfrowane przy użyciu algorytmu szyfrowania symetrycznego Fernet.
Szyfrowane pliki są przechowywane pod nazwą pliku z prefiksem 'encrypted_' oraz zakodowaną w base64 wersją oryginalnej nazwy pliku.
W przypadku żądania pobrania pliku, jest on deszyfrowywany i przesyłany do klienta.
Deszyfrowane pliki są tymczasowo przechowywane na serwerze i usuwane po pobraniu.

## Zarządzanie kluczem
Klucz używany do szyfrowania i deszyfrowania jest przechowywany w pliku o nazwie 'secret.key'.
Jeśli plik klucza istnieje, wczytywany jest istniejący klucz; w przeciwnym razie generowany jest nowy klucz i zapisywany do pliku.

## Logi
Logi serwera są rejestrowane w pliku 'app.log' za pomocą modułu logging w Pythonie.

## Instrukcja

Uruchom Postman i utwórz nowe żądanie POST pod adresem http://127.0.0.1:5000/upload.
Wybierz opcję form-data.
Dodaj klucz o nazwie 'file' i dołącz plik, który chcesz przesłać.
Wyślij żądanie.

Utwórz nowe żądanie GET pod adresem http://127.0.0.1:5000/download/<nazwa-pliku>.
Zastąp <nazwa-pliku> rzeczywistą nazwą pliku do pobrania.
Wyślij żądanie, a plik zostanie pobrany w formie zdeszyfrowanej.

## Podsumowanie

To API umożliwia przesyłanie i pobieranie plików z zastosowaniem szyfrowania symetrycznego. Algorytm Fernet gwarantuje poufność danych podczas transmisji i przechowywania. Projekt na zaliczenie przedmiotu Wstęp do algorytmów wykonali Przemysław Orzechowski i Szymon Kuś.
