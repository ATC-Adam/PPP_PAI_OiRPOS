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
4. [Autoryzacja](#autoryzacja)
5. [Obsługa błędów](#obsługa-błędów)
6. [Testowanie za pomocą Postmana](#testowanie-za-pomocą-postmana)

---

## Wprowadzenie

API aplikacji **Accounts** umożliwia zarządzanie użytkownikami w Twojej aplikacji Django. Udostępnia endpointy do rejestracji, logowania, zmiany hasła, wylogowywania oraz aktualizacji profilu użytkowników.

---

## Uwagi wstępne

- Wszystkie endpointy API są poprzedzone prefiksem `/api/`.
- Dane są przesyłane i zwracane w formacie **JSON**.
- Pola hasła są **zaszyfrowane** po stronie serwera.
- W przypadku endpointów wymagających autoryzacji, należy przesyłać token uwierzytelniający w nagłówku `Authorization`, **z wyjątkiem endpointu wylogowania, który oczekuje tokenu w ciele żądania**.

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
**Opis:** Uwierzytelnia użytkownika i zwraca token uwierzytelniający.

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
  "token": "twój_token",
  "user_id": 1,
  "login": "nowy_login",
  "name": "Jan",
  "surname": "Kowalski"
}
```

#### Możliwe błędy:

- **400 Bad Request:** Nieprawidłowe dane uwierzytelniające.

---

### 3. Zmiana hasła

**URL:** `/api/change_password/`  
**Metoda HTTP:** `POST`  
**Opis:** Pozwala zalogowanemu użytkownikowi zmienić hasło.

#### Nagłówki żądania:

- `Content-Type: application/json`
- `Authorization: Token twój_token`

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
- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający.

---

### 4. Wylogowanie użytkownika

**URL:** `/api/logout/`  
**Metoda HTTP:** `POST`  
**Opis:** Wylogowuje użytkownika, usuwając jego token uwierzytelniający.

#### Nagłówki żądania:

- `Content-Type: application/json`

#### Body żądania:

```json
{
  "auth_token": "twój_token"
}
```

**Opis pól:**

- `auth_token` *(string, wymagane)*: Token uwierzytelniający użytkownika.

#### Przykładowa odpowiedź:

- **Status HTTP:** `200 OK`

```json
{
  "detail": "Pomyślnie wylogowano."
}
```

#### Możliwe błędy:

- **400 Bad Request:**
  - Brak tokenu uwierzytelniającego.
  - Nieprawidłowy token.

---

### 5. Aktualizacja profilu użytkownika

**URL:** `/api/update_profile/`  
**Metoda HTTP:** `PUT`  
**Opis:** Pozwala zalogowanemu użytkownikowi zaktualizować login, imię i nazwisko.

#### Nagłówki żądania:

- `Content-Type: application/json`
- `Authorization: Token twój_token`

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
- **401 Unauthorized:** Brak lub nieprawidłowy token uwierzytelniający.

---

## Autoryzacja

- **Token uwierzytelniający** należy przesyłać w nagłówku `Authorization` w następującym formacie, **z wyjątkiem endpointu wylogowania, który oczekuje tokenu w ciele żądania**:

```
Authorization: Token twój_token
```

- Token jest otrzymywany podczas logowania i powinien być przechowywany bezpiecznie po stronie klienta.

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

3. **Zmiana hasła:**
   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/change_password/`
   - **Nagłówki:**
     - `Content-Type: application/json`
     - `Authorization: Token twój_token`
   - **Body:**

     ```json
     {
       "old_password": "haslo123",
       "new_password": "nowe_haslo",
       "new_password2": "nowe_haslo"
     }
     ```

4. **Wylogowanie użytkownika:**
   - **Metoda:** `POST`
   - **URL:** `http://127.0.0.1:8000/api/logout/`
   - **Nagłówki:**
     - `Content-Type: application/json`
   - **Body:**

     ```json
     {
       "auth_token": "twój_token"
     }
     ```

5. **Aktualizacja profilu użytkownika:**
   - **Metoda:** `PUT`
   - **URL:** `http://127.0.0.1:8000/api/update_profile/`
   - **Nagłówki:**
     - `Content-Type: application/json`
     - `Authorization: Token twój_token`
   - **Body:**

     ```json
     {
       "login": "nowy_login_uzytkownika",
       "name": "NoweImię",
       "surname": "NoweNazwisko"
     }
     ```

   - **Uwagi:**
     - Możesz wysłać tylko te pola, które chcesz zaktualizować.
     - Jeśli próbujesz zmienić login na taki, który już istnieje, otrzymasz błąd.

---

**Uwaga:** Pamiętaj o zastąpieniu `twój_token` faktycznym tokenem uwierzytelniającym otrzymanym podczas logowania. Zadbaj o bezpieczne przechowywanie tokenów i haseł.

---