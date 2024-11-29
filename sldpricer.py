"""
Download sldsets.md as just a copy of scryfall's base sld set list - highlight the set names and images.

Switch to checklist format in scryfall and copy all that without the header in sldprices.md.

Download tcgplayer filtered csv for secret lair as sldtcg.csv.
"""
import pandas as pd


if __name__ == '__main__':
    sets = {}
    with open("sldsets.md", "r", encoding="utf-8") as f:
        name = ""
        s = []
        for line in f.readlines():
            if "•" in line:
                if name:
                    sets[name] = s
                name = line.split("•")[0]
                s = []
            else:
                line = line.strip()
                cardname = line.split("(")[0][:-1]
                try:
                    s.append((cardname[:len(cardname) // 2], line.split("#")[1].split(")")[0].replace("★", "").replace("Φ", "").replace("a", "").replace("b", "")))
                except:
                    pass

        if name != "OTHER CARDS":
            sets[name] = s

    rows = []
    with open("sldprices.md", "r", encoding="utf-8") as f:
        row = []
        for line in f.readlines():
            line = line.strip()
            if line == "SLD":
                if len(row):
                    rows.append(row)
                row = [line]
            else:
                if "€" in line in line:
                    continue
                row.append(line)
    
        if len(row):
            rows.append(row)

    tcg = pd.read_csv("sldtcg.csv")
    sealed = tcg[(tcg["Condition"] == "Unopened") & (~tcg.isna()["TCG Low Price With Shipping"])]

    for name, set in sets.items():
        cardprices = [next((v[-1] for v in rows if v[1] == item[1]), "0") for item in set]
        cardprice = sum([float(p.replace("✶ ", "")[1:].replace(",", "")) for p in cardprices if "$" in p])
        if cardprice == 0:
            continue

        setprice = sealed[sealed["Product Name"].str.contains(name)]["TCG Low Price With Shipping"].sum()

        if setprice and setprice < cardprice:
            print(f"{name}: {setprice:.2f} - {cardprice:.2f}")
