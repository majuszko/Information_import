# Information_import

Skrypt napisany w języku Python, umożliwiający import informacji o działkach z rejestrów.
Napisana została funkcja odpowiadająca za parsowanie pliku XML, oraz przeszukiwanie pliku w celu znalezienia szukanych danych. W przypadku ich znalezienia, dopisuje ich wartość
do tablicy. Następnie z powstałe tablice wierszy i kolumn umieszczanie są w dataframie. W zależności od argumentu, który zostanie przekazany w dataframie umieszczane są albo
kolumny dla jednego formatu albo innego. Obecnie obsługiwane są formaty AAA oraz NAS.
Kod umożliwia sprawne dodanie kolejnych formatów danych, wystarczy dodać format do tablicy, oraz dopisać nazwy szukanych kolumn.

Skrypt został napisany przy użyciu Python 3.8, oraz następujących bibliotek:
 - argparse - do obsługi CLI
 - pandas 1.1.4 - do ułożenia danych w dataframie
 - xml.etree.ElementTree - do parsowania xml
 - Path - do pobrania ścieżki
 
Sposób uruchomienia:

python main.py [format danych] [nazwa pliku]

Przykłady:

python main.py aaa parcel_aaa.xml

python main.py nas parcel_nas.xml
