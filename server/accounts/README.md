# Dokumentacja API aplikacji Accounts

## Spis treści

1. [Wprowadzenie](#wprowadzenie)
2. [Uwagi wstępne](#uwagi-wstępne)
3. [Endpointy API](#endpointy-api)
   - [1. Rejestracja użytkownika](#1-rejestracja-użytkownika)
   - [2. Logowanie użytkownika](#2-logowanie-użytkownika)
   - [3. Zmiana hasła](#3-zmiana-hasła)
   - [4. Wylogowanie użytkownika](#4-wylogowanie-użytkownika)
   - [5. Aktualizacja profilu użytkownika](#5-aktualizacja-profilu-użytkownika)
   - [6. Pobranie danych użytkownika](#6-pobranie-danych-użytkownika)
4. [Autoryzacja](#autoryzacja)
5. [Obsługa błędów](#obsługa-błędów)
6. [Testowanie za pomocą Postmana](#testowanie-za-pomocą-postmana)

---

## Wprowadzenie

API aplikacji **Accounts** umożliwia zarządzanie użytkownikami w Twojej aplikacji Django. Udostępnia endpointy do rejestracji, logowania, zmiany hasła, wylogowywania, aktualizacji profilu oraz pobierania danych użytkownika.

---

## Uwagi wstępne

- Wszystkie endpointy API są poprzedzone prefiksem `/api/`.
- Dane są przesyłane i zwracane w formacie **JSON**.
- Pola hasła są **zaszyfrowane** po stronie serwera.
- **Token uwierzytelniający jest przechowywany w ciasteczku HTTP-only** ustawianym podczas logowania.
- W przypadku endpointów wymagających autoryzacji, uwierzytelnianie odbywa się poprzez token przechowywany w ciasteczku `auth_token`.

---

## Endpointy API

### 1. Rejestracja użytkownika

**URL:** `/api/register/`  
**Metoda HTTP:** `POST`  
**Opis:** Rejestruje nowego użytkownika w systemie.

#### Nagłówki żądania:

- `Content-Type: application/json`

#### Body żądania:

```json
{
  "login": "nowy_login",
  "password": "haslo123",
  "password2": "haslo123",
  "name": "Jan",
  "surname": "Kowalski"
}
```

**Opis pól:**

- `login` *(string, wymagane)*: Unikalny login użytkownika.
- `password` *(string, wymagane)*: Hasło użytkownika.
- `password2` *(string, wymagane)*: Potwierdzenie hasła.
- `name` *(string, wymagane)*: Imię użytkownika.
- `surname` *(string, wymagane)*: Nazwisko użytkownika.

#### Przykładowa odpowiedź:

- **Status HTTP:** `201 Created`

```json
{
  "login": "nowy_login",
  "name": "Jan",
  "surname": "Kowalski"
}
```

#### Możliwe błędy:

- **400 Bad Request:** Błędne dane wejściowe (np. hasła nie są identyczne).

---

### 2. Logowanie użytkownika

**URL:** `/api/login/`  
**Metoda HTTP:** `POST`  
**Opis:** Uwierzytelnia użytkownika i ustawia token uwierzytelniający w ciasteczku HTTP-only.

#### Nagłówki żądania:

- `Content-Type: application/json`

#### Body żądania:

```json
{
  "login": "nowy_login",
  "password": "haslo123"
}
```

**Opis pól:**

- `login` *(string, wymagane)*: Login użytkownika.
- `password` *(string, wymagane)*: Hasło użytkownika.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "user_id": 1,
  "login": "nowy_login",
  "name": "Jan",
  "surname": "Kowalski"
}
```

**Uwaga:** Token uwierzytelniający jest ustawiany w ciasteczku `auth_token` z flagą `HttpOnly`, co oznacza, że nie jest dostępny przez JavaScript.

#### Możliwe błędy:

- **400 Bad Request:** Nieprawidłowe dane uwierzytelniające.

---

### 3. Zmiana hasła

**URL:** `/api/change_password/`  
**Metoda HTTP:** `POST`  
**Opis:** Pozwala zalogowanemu użytkownikowi zmienić hasło.

#### Nagłówki żądania:

- `Content-Type: application/json`
- **Ciasteczko uwierzytelniające**: Musi być wysyłane automatycznie przez klienta (np. przeglądarkę lub narzędzie do testowania API).

#### Body żądania:

```json
{
  "old_password": "haslo123",
  "new_password": "nowe_haslo",
  "new_password2": "nowe_haslo"
}
```

**Opis pól:**

- `old_password` *(string, wymagane)*: Aktualne hasło użytkownika.
- `new_password` *(string, wymagane)*: Nowe hasło.
- `new_password2` *(string, wymagane)*: Potwierdzenie nowego hasła.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "detail": "Hasło zostało zmienione."
}
```

#### Możliwe błędy:

- **400 Bad Request:**
  - Stare hasło jest nieprawidłowe.
  - Nowe hasła nie są identyczne.
- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający w ciasteczku.

---

### 4. Wylogowanie użytkownika

**URL:** `/api/logout/`  
**Metoda HTTP:** `POST`  
**Opis:** Wylogowuje użytkownika, usuwając jego token uwierzytelniający i ciasteczko `auth_token`.

#### Nagłówki żądania:

- `Content-Type: application/json`
- **Ciasteczko uwierzytelniające**: Musi być wysyłane automatycznie przez klienta.

#### Body żądania:

- Brak. Nie wysyłaj żadnych danych w ciele żądania.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "detail": "Pomyślnie wylogowano."
}
```

#### Możliwe błędy:

- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający w ciasteczku.

---

### 5. Aktualizacja profilu użytkownika

**URL:** `/api/update_profile/`  
**Metoda HTTP:** `PUT`  
**Opis:** Pozwala zalogowanemu użytkownikowi zaktualizować login, imię i nazwisko.

#### Nagłówki żądania:

- `Content-Type: application/json`
- **Ciasteczko uwierzytelniające**: Musi być wysyłane automatycznie przez klienta.

#### Body żądania:

```json
{
  "login": "nowy_login_uzytkownika",
  "name": "NoweImię",
  "surname": "NoweNazwisko"
}
```

**Opis pól:**

- `login` *(string, opcjonalne)*: Nowy login użytkownika.
- `name` *(string, opcjonalne)*: Nowe imię użytkownika.
- `surname` *(string, opcjonalne)*: Nowe nazwisko użytkownika.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "detail": "Profil został zaktualizowany."
}
```

#### Możliwe błędy:

- **400 Bad Request:**
  - Login jest już zajęty przez innego użytkownika.
- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający w ciasteczku.

---

### 6. Pobranie danych użytkownika

**URL:** `/api/user/`  
**Metoda HTTP:** `GET`  
**Opis:** Zwraca dane zalogowanego użytkownika.

#### Nagłówki żądania:

- `Content-Type: application/json`
- **Ciasteczko uwierzytelniające**: Musi być wysyłane automatycznie przez klienta.

#### Body żądania:

- Brak. Żądanie nie wymaga żadnych danych w ciele.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "id": 1,
  "login": "nowy_login",
  "name": "Jan",
  "surname": "Kowalski"
}
```

#### Możliwe błędy:

- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający w ciasteczku.

---

## Autoryzacja

- **Token uwierzytelniający jest przechowywany w ciasteczku `auth_token`** ustawianym podczas logowania.
- Klient (np. przeglądarka lub aplikacja) powinien automatycznie wysyłać ciasteczko `auth_token` z każdym żądaniem do endpointów wymagających uwierzytelnienia.
- Token jest otrzymywany podczas logowania i przechowywany po stronie klienta w ciasteczku HTTP-only, co zwiększa bezpieczeństwo.

---

## Obsługa błędów

- API zwraca standardowe kody statusu HTTP w odpowiedzi na żądania.
- W przypadku błędów odpowiedź zawiera szczegóły w formacie JSON.

**Przykład błędu 400 Bad Request:**

```json
{
  "detail": "Brak tokenu uwierzytelniającego."
}
```

**Przykład błędu 401 Unauthorized:**

```json
{
  "detail": "Nieautoryzowany dostęp."
}
```

---

## Testowanie za pomocą Postmana

**Uwaga:** Aby poprawnie testować endpointy korzystające z ciasteczek, upewnij się, że Postman jest skonfigurowany do ich obsługi.

1. **Rejestracja użytkownika:**

   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/register/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "login": "nowy_login",
       "password": "haslo123",
       "password2": "haslo123",
       "name": "Jan",
       "surname": "Kowalski"
     }
     ```

2. **Logowanie użytkownika:**

   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/login/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "login": "nowy_login",
       "password": "haslo123"
     }
     ```

   - **Uwagi:**
     - Po zalogowaniu token uwierzytelniający zostanie ustawiony w ciasteczku `auth_token`.

3. **Zmiana hasła:**

   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/change_password/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "old_password": "haslo123",
       "new_password": "nowe_haslo",
       "new_password2": "nowe_haslo"
     }
     ```

   - **Uwagi:**
     - Upewnij się, że ciasteczko `auth_token` jest wysyłane z żądaniem (Postman powinien to robić automatycznie po zalogowaniu).

4. **Wylogowanie użytkownika:**

   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/logout/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**
     - Brak.

   - **Uwagi:**
     - Ciasteczko `auth_token` zostanie usunięte po wylogowaniu.

5. **Aktualizacja profilu użytkownika:**

   - **Metoda:** `PUT`
   - **URL:** `http://127.0.0.1:8000/api/update_profile/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "login": "nowy_login_uzytkownika",
       "name": "NoweImię",
       "surname": "NoweNazwisko"
     }
     ```

   - **Uwagi:**
     - Upewnij się, że ciasteczko `auth_token` jest wysyłane z żądaniem.
     - Możesz wysłać tylko te pola, które chcesz zaktualizować.
     - Jeśli próbujesz zmienić login na taki, który już istnieje, otrzymasz błąd.

6. **Pobranie danych użytkownika:**

   - **Metoda:** `GET`
   - **URL:** `http://127.0.0.1:8000/api/user/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**
     - Brak.

   - **Uwagi:**
     - Upewnij się, że ciasteczko `auth_token` jest wysyłane z żądaniem.