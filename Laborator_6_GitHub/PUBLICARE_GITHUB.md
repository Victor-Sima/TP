# Pașii rămași pentru publicare

Depozitele locale și commit-urile sunt pregătite. Pentru a finaliza laboratorul, autentifică-te în GitHub și creează două depozite **Publice**, fără a adăuga fișiere la creare:

- `exercitiu-git`
- `exercitiu-2`

Din PowerShell rulează comenzile următoare, înlocuind `USERNAME_GITHUB` cu username-ul tău GitHub:

```powershell
cd "$env:USERPROFILE\Desktop\Laborator_6_GitHub\exercitiu-git"
git remote add origin https://github.com/USERNAME_GITHUB/exercitiu-git.git
git push -u origin main

cd "$env:USERPROFILE\Desktop\Laborator_6_GitHub\exercitiu-2"
git remote add origin https://github.com/USERNAME_GITHUB/exercitiu-2.git
git push -u origin main
```

Apoi:

1. Completează grupa, username-ul și linkurile în `raport/L6_TP_Sima_Victor_GRUPA.md`.
2. Copiază raportul în folderul `Laborator_6_GitHub` din depozitul privat `TP_Nume_Prenume_Grupa` și trimite-l prin commit + push.
3. Trimite e-mailul cerut la `cristian.gonceari@isa.utm.md`, cu subiectul `L6_TP_Nume_Prenume_Grupa`, linkul depozitului privat și codul ultimului commit.

Nu publica parole, token-uri sau alte date sensibile.
