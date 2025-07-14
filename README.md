# secrets 🔐 / 🔓

This repo uses [`age`](https://github.com/FiloSottile/age) to encrypt .env files.

- Each `.env` file is encrypted individually.
- `.age-key.txt` is your private identity (ignored by git).
- Scripts included to encrypt and decrypt.

Use of this repo assumes an environment variable, (GITHUB_PROJECTS_DIR), has been setup to point to a directory of git repos

## Setup

First clone this secrets repo to your local directory of git repos

```sh
git clone https://github.com/spr12ian/secrets.git ${GITHUB_PROJECTS_DIR}/secrets
cd ${GITHUB_PROJECTS_DIR}/secrets
make setup
```

## Encrypt all .env files in $GITHUB_PROJECTS_DIR

```sh
make encrypt-all
```

## Decrypt all .env.age files to $GITHUB_PROJECTS_DIR repos

```sh
make encrypt-all
```

## View public key

```sh
grep -o 'age1[0-9a-z]*' .age-key.txt
   ```

## Encrypt an individual .env file

```sh
make encrypt FILE=Full path to .env file in project repo
```

## Decrypt a .env.age file to an individual repo .env file

```sh
make decrypt FILE=Full path to .env.age file in secrets repo
```
