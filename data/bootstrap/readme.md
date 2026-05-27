# Bootstrap dataset
Sisaldab OpenFoodFacts andmebaasi CSV väljavõttest filtreeritud Eesti andmeid Parquet-formaadis.

## Eesmärk
Võimaldab
- vältida suure faili (kogu andmebaasi) allalaadimist igakordsel käivitamisel ja
- testida andmetoru andmete värskendamise funktsionaalsust mitu päeva "vana" andmebaasi seisuga.

## Kasutamine
- commititakse GitHubi,
- EI ole source-of-truth,
- saab automaatselt uuesti genereerida
- produktsiooni töövoos pole vajalik, kuid kiirendab käivitamist, kui bootstrap on kuni 14 päeva vana