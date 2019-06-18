# Stacja Badawcza

## O Repozytorium

W tym repozytorium składowane będą **wszystkie** zasoby do projektu Stacji Badawczej Code For Green w VIII Liceum Ogólnokształcącym im. Adama Mickiewicza w Poznaniu.

To repozytorium jest **publiczne**, więc miejcie to na uwadze wysyłając cokolwiek.

## O Wysyłaniu Swoich Zmian

Żeby zachować spójność repozytorium i uniknąć możliwie jak najwięcej konfliktów proszę **nie edytować zawartości plików, w których pracuje ktoś inny**!

Jeśli chcecie coś testować, to **róbcie to w nowej gałęzi**.

***

## Poradnik z GitBash

### 1. Klonowanie Repozytorium

Robi się to tylko raz, na samym początku, aby stworzyć folder, do którego pobierzemy zawartość repozytorium, którym będziemy pracować i z którego będziemy wysyłać swoje zmiany.

```
cd <sciezka_folderu_do_ktorego_pobieramy>
git clone https://github.com/CodeForGreenLO8/stacja-badawcza
```

### 2. Commitowanie Wszystkich Zmian

```
git add .
git commit -m "<wiadomosc>"
```

### 3. Wysyłanie Zmian do Repozytorium Online

#### Po raz pierwszy

```
git push -u origin master
```

#### Każdy kolejny raz

```
git push
```

### 4. Bardzo Przydatne Komendy

#### Sprawdzanie aktualnego stanu repozytorium przed commitowaniem

```
git status
```

#### Historia wszystkich commitów na obecnej gałęzi

```
git log --oneline       (lub bez --oneline, wtedy dostajemy dużo więcej informacji)
```

### 5. Praca na Innej Gałęzi

Gałęzie to w praktyce "kopie" całego repozytorium, w której możemy się swobodnie poruszać (można commitować itp.) nie naruszając głównej gałęzi (master). Po zakończeniu pracy w danej gałęzi możemy przenieść swój postęp na gałąź master i usunąć tę dodatkową.

#### Tworzenie nowej gałęzi

```
git branch <nazwa_nowej_galezi>
```

#### Zmiana gałęzi w której jesteśmy

```
git checkout <nazwa_galezi>
```

#### Przenoszenie postępu z gałęzi dodatkowej do master

```
git checkout master
git merge <nazwa_dodatkowej_galezi>
```

#### Usuwanie gałęzi

```
git branch -d <nazwa_galezi>
```
