# [GRUPI NIMI] — [Eesti andmete maht, terviklikkus ja uuenemine Open Food Facts andmebaasis]

> **Juhend:** Asenda kõik nurksulgudes vormid oma sisuga enne esitamist. Kustuta see juhendrida.

## Äriküsimus

[Open Food Facts (https://world.openfoodfacts.org/) on avalik, vabatahtlike poolt täiendatav andmebaas, mis koondab rohkem kui nelja miljoni toidu pakendiandmeid 150 riigist. Projekti eesmärk on hinnata, kuivõrd esinduslik on Open Food Facts andmebaas Eesti puhul ning kas see oleks kasutatav rakenduste loomiseks ja teadustöö sisendina.]

**Mõõdikud:**

1. [Eestis müüdavate toodete koguarv andmebaasis ja lisanduvate toodete arv päevas]
2. [Toodete arv/osakaal tootekategooriate järgi]
3. [Andmete terviklikkus: toodete arv/osakaal, millel on olemas 1) energia ja peamiste toitainete sisaldus, 2) koostisosade nimekiri, 3) pakendi materjal, 4) kogus (netomass/ruumala vmt)]

## Arhitektuur

```mermaid
flowchart LR
    source[Andmeallikas] --> ingest[Sissevõtt]
    ingest --> staging[(staging)]
    staging --> transform[Transformatsioon]
    transform --> mart[(mart)]
    mart --> dashboard[Näidikulaud]
```

Täpsem kirjeldus: [`docs/arhitektuur.md`](docs/arhitektuur.md)

## Andmestik

| Allikas | Tüüp | Ajas muutuv? | Roll |
|---------|------|--------------|------|
| [Andmeallika nimi] | [API / fail / andmebaas] | Jah, [iga päevas] | Põhiandmevoog |
| [Eestis müüdavad tooted seisuga xx.05.2026] | [seed] | Ei, staatiline | Kõrvaltabel |

## Stack

| Komponent | Tööriist |
|-----------|---------|
| Sissevõtt | [Python] |
| Transformatsioon | [SQL / dbt? ] |
| Andmehoidla | [DuckDB] |
| Näidikulaud | [Superset] |
| Orkestreerimine | [cron / Airflow?] |

## Käivitamine

```bash
# 1. Klooni repo ja liigu kausta
git clone <repo-url>
cd <projekti-kaust>

# 2. Kopeeri keskkonnamuutujad
cp .env.example .env
# Muuda .env failis paroolid ja muud seaded vastavalt vajadusele

# 3. Käivita teenused
docker compose up -d --build

# 4. [Vabatahtlik: käivita sissevõtt käsitsi esimesel korral]
# docker compose exec pipeline python scripts/run_pipeline.py run-all
```

Airflow (kui kasutatakse): http://localhost:8080 (kasutaja: airflow / parool: airflow)
Näidikulaud: http://localhost:[PORT]

## Saladused ja konfiguratsioon

Kõik saladused (paroolid, API võtmed, andmebaasi URL-id) on `.env` failis. Repos on ainult `.env.example`, mis näitab vajalike muutujate struktuuri ilma tegelike väärtusteta. Päris `.env` faili ei tohi GitHubi panna - see on `.gitignore`-s.

Vajalikud muutujad:

| Muutuja | Tähendus | Näide |
|---------|----------|-------|
| `DB_PASSWORD` | PostgreSQL parool | (saladus) |
| `[teised]` | ... | ... |

## Andmevoog lühidalt

1. **Sissevõtt** — [Kirjelda, kuidas andmed allikast kätte saadakse]
2. **Laadimine** — Andmed laaditakse `staging` kihti
3. **Transformatsioon** — [Kirjelda peamised arvutused ja mudelid]
4. **Testimine** — [Mitu] andmekvaliteedi testi kontrollivad korrektsust
5. **Näidikulaud** — [Kirjelda lühidalt, mida näidikulaud näitab]

## Andmekvaliteedi testid

Projekt kontrollib järgmist:

1. [Test 1 - nt: kasutajate ID on unikaalne]
2. [Test 2 - nt: tellimuse summa pole null]
3. [Test 3 - nt: kuupäev jääb vahemikku 2020-2026]
[Lisa rohkem, kui sul on]

Testide tulemused: [kuhu salvestatakse / kuidas vaadata]

## Projekti struktuur

```
.
├── README.md
├── compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── arhitektuur.md      ← nädal 1 väljund
│   └── progress.md         ← nädal 2 väljund
└── ...                     ← ülejäänud projektifailid
```

## Kokkuvõte, puudused ja võimalikud edasiarendused

**Kokkuvõte:**
- [Loetle, mis on lõpule viidud, mis töötab hästi]

**Puudused:**
- [Loetle ausalt, mis jäi tegemata - see ei mõjuta hinnet negatiivselt, vaid aitab hinnata]

**Mis edasi:**
- [Mida tahaksid edasi teha, kui aega oleks rohkem]

## Meeskond

| Nimi | Roll |
|------|------|
| [Nimi 1] | [Roll] |
| [Nimi 2] | [Roll] |
| [Nimi 3] | [Roll] |
| [Nimi 4] | [Roll — vabatahtlik] |
