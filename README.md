# secrets

## 🔐 Encrypted .env Files

This repo stores encrypted `.env` files using [`age`](https://github.com/FiloSottile/age).

- Each `.env` file is encrypted individually.
- `.age-key.txt` is your private identity (ignored by git).
- Scripts included to encrypt and decrypt.

## Setup

1. Install [age](https://github.com/FiloSottile/age#installation)
2. Generate a key:

    ```sh
    age-keygen -o .age-key.txt
    ```

## View public key

```sh
grep -o 'age1[0-9a-z]*' .age-key.txt
   ```

## Encrypt an env file

```sh
./encrypt.sh repo1 ../repo1/.env
```

## Decrypt to a private repo

```sh
./decrypt.sh repo1 ../repo1/.env
```
